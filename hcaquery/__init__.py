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

REMOTE_URL = "https://swift.rc.nectar.org.au/v1/AUTH_06d6e008e3e642da99d806ba3ea629c5/harmonised-human-atlas" #?path=%2Foriginal%2F000ae9ae99f825c20ccd93a4b1548719&files=se.rds"
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

	sqlite_path = os.path.join(cache_directory, "metadata.sqlite")

	sync_remote_file(
		repository,
		sqlite_path)

	eng = sqlalchemy.create_engine('sqlite:///{}'.format(sqlite_path))

	# get metadata table to return to user
	md = sqlalchemy.MetaData()
	mdtab = sqlalchemy.Table("metadata", md, autoload_with=eng)
	mdtab = md.tables['metadata']

	return eng, mdtab

def sync_assay_files(url = REMOTE_URL, cache_dir = get_default_cache_dir(), subdirs = [], files = []):

	urls = ["{baseurl}/{subdir}/{sample}/{filename}".format(baseurl=url, subdir=sdir, sample=ifile, filename=filename) 
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
def read_data(x, features=[]):
	try:
		if features==[]:
			data_view = ad.read(x)
		else:
			data_view = ad.read(x)[:,features]
		data = data_view.copy()
		data_view.file.close()
	except FileNotFoundError:
		print("Sample file {sf} not found! This probably means it was not downloaded correctly.".format(sf=x))

	yield data

def get_SingleCellExperiment(
	data = pd.DataFrame(),
	assays = ["counts", "cpm"],
	cache_directory = get_default_cache_dir(),
	repository = REMOTE_URL,
	features = [],
	silent = False
):

	# error checking
	assert any(x in assays for x in assay_map.keys()), 'assays must be a vector containing "counts" and/or "cpm"'

	assert isinstance(cache_directory, str), 'cache_directory must be a string'

	assert isinstance(features, (str, list, tuple)), 'features must be a string, list of strings, or tuple of strings'

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
	if not silent:
		files2pull = tqdm.tqdm(files2pull, desc="Reading sample files", ncols=80, unit='files')
	pulled_data = list(zip(*map(read_data,files2pull,itertools.repeat(features))))[0]
	
	# temporary combine solution - original R code adds file_id_db as another column (I think)
	if not silent:
		print("Concatenating files...")
	pulled_data = ad.concat(pulled_data, index_unique='-')

	return pulled_data

if __name__=="__main__":

	#eng, metadatatab = get_metadata(cache_directory='/vast/scratch/users/yang.e/tmp')
	sync_assay_files(cache_dir='/vast/scratch/users/yang.e/tmp/dummy-hca', subdirs=['original','cpm'], files=['18b89f46a7bd507ac85033d3e21c56d6','18ce8f08b718573c04d26094071e1e69'])
	#df = pd.read_sql("SELECT * FROM metadata WHERE ethnicity='African';", eng)
	#q = sqlalchemy.select(metadatatab).where(metadatatab.c.ethnicity=='African')
	#q = sqlalchemy.select(metadatatab).where(\
	#	(metadatatab.c.ethnicity=="African") & \
	#	(metadatatab.c.assay.like('%{}%'.format('10x'))) & \
	#	(metadatatab.c.tissue=="lung parenchyma") & \
	#	(metadatatab.c.cell_type.like('%{}%'.format('CD4'))))
	#q = sqlalchemy.select([metadatatab.c.file_id_db, metadatatab.c.assay, metadatatab.c.tissue, metadatatab.c.cell_type]).where(\
	#		(metadatatab.c.assay.like('%{}%'.format('10x'))) & \
	#		(metadatatab.c.tissue=="lung parenchyma") & \
	#		(metadatatab.c.cell_type.like('%{}%'.format('CD4'))))

	#with eng.connect() as con:
	#	df = pd.DataFrame(con.execute(q))
	#eng.dispose()
	#print(df)
	#z = get_SingleCellExperiment(df, cache_directory='/vast/projects/human_cell_atlas_py',('))
	#z = get_SingleCellExperiment(df, cache_directory='/vast/projects/human_cell_atlas_py')
	#print(z)
