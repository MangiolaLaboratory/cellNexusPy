import tempfile, os, sys, tqdm, time, itertools, sqlalchemy
import anndata as ad
import pandas as pd
try:
	from sqlalchemy import URL
except:
	from sqlalchemy.engine import URL

REMOTE_URL = "https://swift.rc.nectar.org.au/v1/AUTH_06d6e008e3e642da99d806ba3ea629c5"
ASSAY_URL= '{}/harmonised-human-atlas'.format(REMOTE_URL)
METADATASQLITE_URL = '{}/metadata-sqlite/metadata.tar.xz'.format(REMOTE_URL)
METADATADB_URL = URL.create("mysql+pymysql", \
	username='public_access', \
	password='password', \
	host='7f7wu64bnzu.db.cloud.edu.au', \
	database='metadata')

assay_map = {'counts': 'original', 'cpm': 'cpm'}

#using tmpdir as cachedir for the time being
def get_default_cache_dir():
	return os.path.join(tempfile.gettempdir(),"hca_harmonised")

def show_progress(block_num, block_size, total_size):
	prog = round(block_num * block_size / total_size * 100, 2)
	print('Download progress: {prog:3.1f}%'.format(prog=prog), \
		end="\r", \
		file=sys.stderr)

# helper function to download file over http/https
def sync_remote_file(full_url, output_file):
	if not os.path.isfile(output_file):
		output_dir = os.path.dirname(output_file)
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)
		print("Downloading {url} to {outfile}".format(url=full_url, outfile=output_file), file=sys.stderr)

		try:
			import urllib.request
			r = urllib.request.urlopen(full_url)
			urllib.request.urlretrieve(full_url, output_file, show_progress)

		except Exception as e:
			if os.path.isfile(output_file): 
				os.remove(output_file)
			sys.exit("File {url} could not be downloaded.\n{e}".format(url=full_url, e=e))

# function to get metadata
def get_metadata(sqlite_url=METADATASQLITE_URL, \
	cache_dir = get_default_cache_dir()):

	import tarfile

	sqlite_tarxz_path = os.path.join(cache_dir, "metadata.tar.xz")
	sqlite_path = os.path.join(cache_dir, "metadata.sqlite")
	if not os.path.isfile(sqlite_path):
		sync_remote_file(sqlite_url, sqlite_tarxz_path)
		try:
			with tarfile.open(sqlite_tarxz_path) as f:
				print("\nExtracting database...", file=sys.stderr)
				f.extractall(cache_dir)
		except Exception as e:
			print("Failed to download/extract database\n")
			print(e)
			if os.isfile(sqlite_tarxz_path):
				os.remove(sqlite_tarxz_path)
			if os.isfile(sqlite_path):
				os.remove(sqlite_path)
		os.remove(sqlite_tarxz_path)

	eng = sqlalchemy.create_engine('sqlite:///{}'.format(sqlite_path))

	# get metadata table to return to user
	md = sqlalchemy.MetaData()
	mdtab = sqlalchemy.Table("metadata", md, autoload_with=eng)
	mdtab = md.tables['metadata']

	return eng, mdtab

def _get_metadata_mysql(connection_url=METADATADB_URL, \
	cache_dir = get_default_cache_dir()):

	eng = sqlalchemy.create_engine(connection_url)
	md = sqlalchemy.MetaData()
	mdtab = sqlalchemy.Table("metadata", md, autoload_with=eng)
	mdtab = md.tables['metadata']

	return eng, mdtab

def sync_assay_files(url = ASSAY_URL, cache_dir = get_default_cache_dir(), subdirs = [], files = []):

	urls = ["{baseurl}/{subdir}/{samplefile}".format(baseurl=url, subdir=sdir, samplefile=ifile) 
		for sdir, ifile in itertools.product(subdirs, files)]
	
	output_filepaths = [os.path.join(cache_dir, sdir, ifile) 
		for sdir, ifile in itertools.product(subdirs, files)]

	for urli,fpathi in zip(urls,output_filepaths): 
		if os.path.isfile(fpathi):
			continue
		else:
			sync_remote_file(urli, fpathi)
	
	return output_filepaths
	
# used as a function for reduce further down
# f2[0] is the h5ad path and f2[1] is the features array.
def read_data(ar, f2):
	if f2[1] == []:
		if ar:
			return ad.concat([ar, ad.read(f2[0])], index_unique='-')
		else:
			return ad.read(f2[0])
	else:
		if ar:
			return ad.concat([ar, ad.read(f2[0])[:,f2[1]]], index_unique='-')
		else:
			return ad.read(f2[0])[:, f2[1]] 


def get_SingleCellExperiment(
	data = pd.DataFrame(),
	assays = ["counts", "cpm"],
	cache_directory = get_default_cache_dir(),
	repository = ASSAY_URL,
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

    # need the reduce function
	import functools
	
	# all the files to retrieve for query
	files_to_read = ['{}.h5ad'.format(sample) for sample in data['file_id_db'].unique()]

	# mapping requested assay to subdirectory name
	subdirs = [assay_map[a] for a in assays]

	sync_assay_files(url=repository, cache_dir=cache_directory ,subdirs=subdirs, files=files_to_read)

	# "outer" product of subdirectories and filenames
	files2pull = [os.path.join(cache_directory,s,f) for s,f in itertools.product(subdirs, files_to_read)]

	# concat backed data "hack" https://discourse.scverse.org/t/concat-anndata-objects-on-disk/400/2
	# might be released in future versions https://github.com/scverse/anndata/issues/793
	if not silent:
		files2pull = tqdm.tqdm(files2pull, desc="Reading sample files", ncols=80, unit='files')
    
    # this step uses heaps of mem depending on the size of the file(s) being concat'ed
	pulled_data = functools.reduce( \
		read_data, \
        zip(files2pull, itertools.repeat(features)), \
        None)

	return pulled_data

if __name__=="__main__":

	eng, metadatatab = get_metadata(cache_dir='/vast/projects/human_cell_atlas_py')

	# q = sqlalchemy.select('*').where( \
	# 	metadatatab.c.ethnicity=="African", \
	# 	metadatatab.c.assay.like('%10x%'), \
	# 	metadatatab.c.tissue == "lung parenchyma", \
	# 	metadatatab.c.cell_type.like('%CD4%'))
	#q = sqlalchemy.select([metadatatab.c.file_id_db, metadatatab.c.assay, metadatatab.c.tissue, metadatatab.c.cell_type]).where(\
	#		(metadatatab.c.assay.like('%{}%'.format('10x'))) & \
	#		(metadatatab.c.tissue=="lung parenchyma") & \
	#		(metadatatab.c.cell_type.like('%{}%'.format('CD4'))))
	q = sqlalchemy.select(metadatatab.c['.cell','file_id_db','disease','file_id','tissue_harmonised']).where(metadatatab.c.cell_type_harmonised=='nk')


	with eng.connect() as con:
		df = pd.DataFrame(con.execute(q))	
	eng.dispose()
	print(df)

	z = get_SingleCellExperiment(df, repository='file:///vast/projects/human_cell_atlas_py/anndata', features=['NCAM1'], assays=['cpm'], cache_directory='/vast/projects/human_cell_atlas_py/anndata')
	print(z)
