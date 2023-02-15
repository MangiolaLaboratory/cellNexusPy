import itertools
import os
import shutil
import sys
from pathlib import Path
from typing import Iterable, Literal

import anndata as ad
import duckdb
import pandas as pd
import requests
from appdirs import user_cache_dir
from tqdm import tqdm

REMOTE_URL = "https://swift.rc.nectar.org.au/v1/AUTH_06d6e008e3e642da99d806ba3ea629c5"
ASSAY_URL= '{}/harmonised-human-atlas-anndata'.format(REMOTE_URL)
METADATA_URL = '{}/metadata-sqlite/metadata.parquet'.format(REMOTE_URL)

assay_map = {'counts': 'original', 'cpm': 'cpm'}

def _get_default_cache_dir() -> Path:
	return Path(user_cache_dir("CuratedAtlasQueryPy"))

# helper function to download file over http/https
def _sync_remote_file(full_url: str, output_file: Path):
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
def get_metadata(parquet_url: str=METADATA_URL, cache_dir: os.PathLike[str] = _get_default_cache_dir()) -> tuple[duckdb.DuckDBPyConnection, duckdb.DuckDBPyRelation]:
	parquet_local = Path(cache_dir) / "metadata.parquet"
	_sync_remote_file(parquet_url, parquet_local)
	conn = duckdb.connect()
	return conn, conn.from_parquet(str(parquet_local))

def sync_assay_files(url: str = ASSAY_URL, cache_dir: Path = _get_default_cache_dir(), subdirs: Iterable[str] = [], files: Iterable[str] = []):
	for subdir in subdirs:
		for file in files:
			url = f"{url}/{subdir}/{file}"
			output_filepath = cache_dir / subdir / file

			if not output_filepath.exists():
				_sync_remote_file(url, output_filepath)
			
			yield subdir, output_filepath
	
def get_anndata(
	data: duckdb.DuckDBPyRelation,
	assays: Iterable[Literal["counts", "cpm"]] = ["counts", "cpm"],
	cache_directory: Path = _get_default_cache_dir(),
	repository: str = ASSAY_URL,
	features: Iterable[str] = [],
)->  ad.AnnData:

	# error checking
	assert set(assays).issubset(set(assay_map.keys()))
	assert isinstance(cache_directory, Path), 'cache_directory must be a Path'
	assert isinstance(features, (str, list, tuple)), 'features must be a string, list of strings, or tuple of strings'

	assays = set(assays)
	cache_directory.mkdir(exist_ok=True, parents=True)

	# all the files to retrieve for query
	files_to_read: pd.Series[str] = data.project("file_id_db").distinct().fetchdf()["file_id_db"].str.cat([".h5ad"])
	cells: pd.Series[str] = data.project('".cell"').distinct().fetchdf()[".cell"]

	# mapping requested assay to subdirectory name
	subdirs = [assay_map[a] for a in assays]

	synced = sync_assay_files(url=repository, cache_dir=cache_directory ,subdirs=subdirs, files=files_to_read)
	ad_per_assay: dict[str, ad.AnnData] = {}
	for assay_name, files in itertools.groupby(synced, key=lambda x: x[0]):
		paths = (tup[1] for tup in files)
		ads = (ad.read_h5ad(path, backed="r")[cells] for path in paths)
		ad_per_assay[assay_name] = ad.concat(ads, index_unique="-")

	ann = ad_per_assay["original"]
	ann.layers["cpm"] = ad_per_assay["cpm"].X
	ann.obs = data.fetchdf()
	return ann