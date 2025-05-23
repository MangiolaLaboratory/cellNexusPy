import itertools
import os
import shutil
import sys
from pathlib import Path
from typing import Iterable, Literal

import anndata as ad
import scipy.sparse as sp
import duckdb
import pandas as pd
import requests
from appdirs import user_cache_dir
from tqdm import tqdm

REMOTE_URL = "https://object-store.rc.nectar.org.au/v1/AUTH_06d6e008e3e642da99d806ba3ea629c5"
ASSAY_URL = "{}/cellNexus-anndata".format(REMOTE_URL)
METADATA_URL = "{}/cellNexus-metadata/metadata.1.0.10.parquet".format(REMOTE_URL)
MIN_EXPECTED_SIZE = 5000000

assay_map = {"counts": "counts", "cpm": "cpm"}

def is_parquet_valid(parquet_file):
    try:
        conn = duckdb.connect()
        conn.from_parquet(str(parquet_file))  # Try reading
        return True  # File is valid
    except Exception as e:
        print(f"Parquet file is corrupt: {e}")
        return False  # File is corrupt
        
def _get_default_cache_dir() -> Path:
    return Path(user_cache_dir("cellNexusPy"))


# helper function to download file over http/https
def _sync_remote_file(full_url: str, output_file: Path):
    if not output_file.exists():
        output_dir = output_file.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Downloading {full_url} to {output_file}", file=sys.stderr)
        req = requests.get(full_url, stream=True, allow_redirects=True)
        req.raise_for_status()
        pbar = tqdm(total=int(req.headers.get("Content-Length", 0)))
        with pbar.wrapattr(req.raw, "read") as src, output_file.open("wb") as dest:
            shutil.copyfileobj(src, dest)


# function to get metadata
def get_metadata(
    parquet_url: str = METADATA_URL,
    cache_dir: os.PathLike[str] = _get_default_cache_dir(),
) -> tuple[duckdb.DuckDBPyConnection, duckdb.DuckDBPyRelation]:
    parquet_local = Path(cache_dir) / parquet_url.split("/")[-1]

    if not parquet_local.exists() or not is_parquet_valid(parquet_local):
        print("File is missing or corrupted. Re-downloading...")
        parquet_local.unlink(missing_ok=True)  # Delete the corrupted file
        _sync_remote_file(parquet_url, parquet_local)  # Re-download
    
    _sync_remote_file(parquet_url, parquet_local)
    conn = duckdb.connect()
    return conn, conn.from_parquet(str(parquet_local))

def sync_assay_files(
    url: str = ASSAY_URL,
    cache_dir: Path = _get_default_cache_dir(),
    subdirs: Iterable[str] = [],
    atlases: Iterable[str] = [],
    files: Iterable[str] = [],
):
    for atlas in atlases:
        for subdir in subdirs:
            for file in files:
                sub_url = f"{url}/{atlas}/{subdir}/{file}"
                output_filepath = cache_dir / atlas / subdir / file

                if not output_filepath.exists() or os.path.getsize(output_filepath) < MIN_EXPECTED_SIZE:
                    _sync_remote_file(sub_url, output_filepath)

                yield subdir, output_filepath


def get_anndata(
    data: duckdb.DuckDBPyRelation,
    assays: Iterable[Literal["counts", "cpm"]] = ["counts", "cpm"],
    aggregation: Iterable[Literal["single_cell", "pseudobulk", "metacell"]] = ["single_cell", "pseudobulk", "metacell"],
    cache_directory: Path = _get_default_cache_dir(),
    repository: str = ASSAY_URL,
    features: Iterable[str] = slice(None, None, None),
) -> ad.AnnData:
    # error checking
    assert set(assays).issubset(set(assay_map.keys()))
    assert isinstance(cache_directory, Path), "cache_directory must be a Path"
    
    assays = set(assays)
    cache_directory.mkdir(exist_ok=True, parents=True)
    
        # all the files to retrieve for query
    if str(aggregation[0])=="metacell":
        aggregation = ["single_cell"] 
        data.filter("metacell_2 IS NOT NULL")
    
    files_to_read = (
        data.project("file_id_cellNexus_"+str(aggregation[0])).distinct().fetchdf()["file_id_cellNexus_"+str(aggregation[0])]
    )
    cells = data.project('"cell_id"').distinct().fetchdf()["cell_id"]
    atlases = data.project('"atlas_id"').distinct().fetchdf()["atlas_id"]
        # mapping requested assay to subdirectory name
    subdirs = [assay_map[a] for a in assays]                                                                                                                         
    
    synced = sync_assay_files(
        url=repository, cache_dir=cache_directory, atlases=atlases, subdirs=subdirs, files=files_to_read
    )
    
    ad_per_assay: dict[str, ad.AnnData] = {}
        # Concatenate files per assay
    for assay_name, files in itertools.groupby(synced, key=lambda x: x[0]):
        ads = [ad.read_h5ad(file[1]) for file in files]
        ad_per_assay[assay_name] = ad.concat(ads, index_unique="-")
    
    main_assay_key = (
        "counts" if "counts" in ad_per_assay else next(iter(ad_per_assay.keys()))
    )
    
    ann = ad_per_assay.pop(main_assay_key)
        # Attach the additional assays
    for key, anndata in ad_per_assay.items():
        ann.layers[key] = anndata.X
    return ann
