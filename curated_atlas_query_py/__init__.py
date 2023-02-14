import itertools
import os
import shutil
import sys
import tempfile
from pathlib import Path
from appdirs import user_cache_dir
import requests
import duckdb
from typing import Any, Iterable, Literal
import functools
import numpy as np
from numpy.typing import NDArray
import operator

import anndata as ad
import pandas as pd
from tqdm import tqdm

REMOTE_URL = "https://swift.rc.nectar.org.au/v1/AUTH_06d6e008e3e642da99d806ba3ea629c5"
ASSAY_URL= '{}/harmonised-human-atlas-anndata'.format(REMOTE_URL)
METADATA_URL = '{}/metadata-sqlite/metadata.parquet'.format(REMOTE_URL)

assay_map = {'counts': 'original', 'cpm': 'cpm'}

def get_default_cache_dir() -> Path:
	return Path(user_cache_dir("CuratedAtlasQueryPy"))

# helper function to download file over http/https
def sync_remote_file(full_url: str, output_file: Path):
	if not output_file.exists():
		output_dir = output_file.parent
		output_dir.mkdir(exist_ok=True)
		print(f"Downloading {full_url} to {output_file}", file=sys.stderr)
		req = requests.get(full_url, stream=True, allow_redirects=True)
		req.raise_for_status()
		pbar = tqdm(total=int(req.headers.get('Content-Length', 0)))
		with pbar.wrapattr(req.raw, "read") as src, output_file.open("wb") as dest:
			shutil.copyfileobj(src, dest)

# function to get metadata
def get_metadata(parquet_url: str=METADATA_URL, cache_dir: os.PathLike[str] = get_default_cache_dir()) -> tuple[duckdb.DuckDBPyConnection, duckdb.DuckDBPyRelation]:
	parquet_local = Path(cache_dir) / "metadata.parquet"
	sync_remote_file(parquet_url, parquet_local)
	conn = duckdb.connect()
	return conn, conn.from_parquet(str(parquet_local))

def sync_assay_files(url: str = ASSAY_URL, cache_dir: Path = get_default_cache_dir(), subdirs: Iterable[str] = [], files: Iterable[str] = []):
	for subdir in subdirs:
		for file in files:
			url = f"{url}/{subdir}/{file}"
			output_filepath = cache_dir / subdir / file

			if not output_filepath.exists():
				sync_remote_file(url, output_filepath)
			
			yield subdir, output_filepath
	
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
	data: duckdb.DuckDBPyRelation,
	assays: Iterable[Literal["counts", "cpm"]] = ["counts", "cpm"],
	cache_directory: Path = get_default_cache_dir(),
	repository: str = ASSAY_URL,
	features: Iterable[str] = [],
	silent: bool = False
):

	# error checking
	assert set(assays).issubset(set(assay_map.keys()))
	assert isinstance(cache_directory, Path), 'cache_directory must be a Path'
	assert isinstance(features, (str, list, tuple)), 'features must be a string, list of strings, or tuple of strings'

	assays = set(assays)
	cache_directory.mkdir(exist_ok=True, parents=True)

	# all the files to retrieve for query
	files_to_read: pd.Series[str] = data.project("file_id_db").distinct().fetchdf()["file_id_db"].str.cat([".h5ad"])

	# mapping requested assay to subdirectory name
	subdirs = [assay_map[a] for a in assays]

	synced = sync_assay_files(url=repository, cache_dir=cache_directory ,subdirs=subdirs, files=files_to_read)

	layers = {}
	for assay_name, files in itertools.groupby(synced, key=lambda x: x[0]):
		paths = (tup[1] for tup in files)
		layers[assay_name] = ad.concat(ad.read_h5ad(path) for path in paths).X
	ann = ad.AnnData(X=layers.pop("original"), layers=layers, obs=data.fetchdf())
	return ann


	# "outer" product of subdirectories and filenames
	files2pull = (os.path.join(cache_directory,s,f) for s,f in itertools.product(subdirs, files_to_read))

	return ad.concat(files2pull)

	# concat backed data "hack" https://discourse.scverse.org/t/concat-anndata-objects-on-disk/400/2
	# might be released in future versions https://github.com/scverse/anndata/issues/793
	# if not silent:
	# 	files2pull = tqdm.tqdm(files2pull, desc="Reading sample files", ncols=80, unit='files')
    
    # this step uses heaps of mem depending on the size of the file(s) being concat'ed
	pulled_data = functools.reduce( \
		read_data, \
        zip(files2pull, itertools.repeat(features)), \
        None)

	return pulled_data