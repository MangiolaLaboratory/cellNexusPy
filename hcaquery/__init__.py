#import anndata as ad
#from scipy.sparse import csr_matrix
import tempfile
import os
import anndata as ad
import pandas as pd
import tqdm
import time
import itertools
import sqlalchemy

REMOTE_URL = "https://cloudstor.aarnet.edu.au/plus/s/nrQ8q1OBS0sjtxv/download" #?path=%2Foriginal%2F000ae9ae99f825c20ccd93a4b1548719&files=se.rds"
assay_map = {'counts': 'splitted_DB2_anndata', 'cpm': 'splitted_DB2_anndata_scaled'} #{'counts': 'original', 'cpm': 'cpm'}

#???
def as_sparse_DelayedMatrix():
	pass

#???
def get_seurat():
	pass

#using tmpdir as cachedir for the time being
def get_default_cache_dir():
	return os.path.join(tempfile.gettempdir(),"hca_harmonised")

def show_progress(block_num, block_size, total_size):
	print('Download progress: {prog:3.1f}%'.format(prog=round(block_num * block_size / total_size *100, 2)), end="\r")

# helper function to download file over http/https
def sync_remote_file(full_url, output_file):
	if not os.path.isfile(output_file):
		output_dir = os.path.dirname(output_file)
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)
		print("Downloading {url} to {outfile}".format(url=full_url, outfile=output_file))

		#TODO: produce warning if file isn't found (but don't stop)
		try:
			import urllib.request
			r = urllib.request.urlopen(full_url)
			urllib.request.urlretrieve(full_url, output_file, show_progress)

		except Exception as e:
			print("File {url} could not be downloaded.".format(url=full_url))
			print(e)
			os.remove(output_file)

# function to get metadata
def get_metadata(repository="https://harmonised-human-atlas.s3.amazonaws.com/metadata.sqlite", 
	cache_directory = get_default_cache_dir()):
	
	import sqlalchemy 

	sqlite_path = os.path.join(cache_directory, "metadata.sqlite")
	sync_remote_file(
		repository,
		sqlite_path)
	#con = sqlite3.connect(sqlite_path, uri=True)
	eng = sqlalchemy.create_engine('sqlite:///{}'.format(sqlite_path))

	# get metadata table to return to user
	md = sqlalchemy.MetaData()
	mdtab = sqlalchemy.Table("metadata", md, autoload_with=eng)
	#md = sqlalchemy.MetaData(bind=eng)
	#sqlalchemy.MetaData.reflect(md)
	mdtab = md.tables['metadata']

	return eng, mdtab

def sync_assay_files(url = REMOTE_URL, cache_dir = get_default_cache_dir(), subdirs = [], files = []):

	urls = ["{baseurl}?path=%2F{subdir}%2F{assay}&files={filename}".format(baseurl=url, subdir=sdir, assay=ifile, filename=filename) 
		for sdir, ifile, filename in itertools.product(subdirs, files, ["assays.h5", "se.rds"])]
	
	output_filepaths = [os.path.join(cache_dir, sdir, ifile, filename) 
		for sdir, ifile, filename in itertools.product(subdirs, files, ["assays.h5", "se.rds"])]

	for urli,fpathi in zip(urls,output_filepaths): 
		if os.path.isfile(fpathi):
			continue
		else:
			sync_remote_file(urli, fpathi)
	
	return output_filepaths

# temporary until we have a whole set of anndata
# used as a function for map further down
def read_data(x):
	try:
		data = ad.read(x).copy()
	except:
		data = None

	yield data

def get_SingleCellExperiment(
	data = pd.DataFrame(),
	assays = ["counts", "cpm"],
	cache_directory = get_default_cache_dir(),
	repository = REMOTE_URL,
	features = None
):

	# error checking
	assert any(x in assays for x in assay_map.keys()), 'assays must be a vector containing "counts" and/or "cpm"'

	assert isinstance(cache_directory, str), 'cache_directory must be a string'

	assert isinstance(features, str) or features == None, 'features must be a string'

	assays = set(assays)

	if not os.path.exists(cache_directory):
		os.makedirs(cache_directory)
	
	# all the files to retrieve for query
	files_to_read = data['file_id_db'].unique()

	# mapping requested assay to subdirectory name
	subdirs = [assay_map[a] for a in assays]

	# "outer" product of subdirectories and filenames
	files2pull = [os.path.join(cache_directory,s,f) for s,f in itertools.product(subdirs, files_to_read)]

	# concat backed data "hack" https://discourse.scverse.org/t/concat-anndata-objects-on-disk/400/2
	# might be released in future versions https://github.com/scverse/anndata/issues/793
	pulled_data = list(zip(*map(read_data,tqdm.tqdm(files2pull))))[0]

	# stripping None's instead of exception handling because anndata dataset is incomplete
	pulled_data = [x for x in pulled_data if not isinstance(x, type(None))]
	
	# temporary combine solution - original R code adds file_id_db as another column (I think)
	pulled_data = ad.concat(pulled_data, index_unique='-')

	return pulled_data

if __name__=="__main__":

	eng, metadatatab = get_metadata(cache_directory='/vast/scratch/users/yang.e/tmp/')
	#df = pd.read_sql_query("SELECT * FROM metadata WHERE ethnicity='African' AND assay LIKE '%10x%' AND tissue='lung parenchyma' AND cell_type LIKE '%CD4%';", con)
	#df = pd.read_sql("SELECT * FROM metadata WHERE ethnicity='African';", eng)
	q = sqlalchemy.select(metadatatab).where(metadatatab.c.ethnicity=='African')
	with eng.connect() as con:
		df = pd.DataFrame(con.execute(q))
	eng.dispose()
	print(df)
	z = get_SingleCellExperiment(df, cache_directory='/vast/projects/RCP/human_cell_atlas')
	print(z)
	#df['file_id_db'].unique()
	#print(sync_assay_files(files=df['file_id_db'].unique(), subdirs=['original', 'cpm']))
