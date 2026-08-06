import itertools
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Iterable, Literal

import anndata as ad
import numpy as np
import scipy.sparse as sp
import duckdb
import pandas as pd
import requests
from appdirs import user_cache_dir
from tqdm import tqdm

REMOTE_URL = "https://object-store.rc.nectar.org.au/v1/AUTH_06d6e008e3e642da99d806ba3ea629c5"
ASSAY_URL = "{}/cellNexus-anndata".format(REMOTE_URL)
METADATA_URL = "{}/cellNexus-metadata/cellnexus_metadata.2.3.0.parquet".format(REMOTE_URL)
SAMPLE_DATABASE_URL = "{}/cellNexus-metadata/cellnexus_sample_metadata.2.3.0.parquet".format(REMOTE_URL)
CENSUS_METADATA_URL = "{}/cellNexus-metadata/census_cell_metadata.2.3.0.parquet".format(REMOTE_URL)
CENSUS_SAMPLE_METADATA_URL = "{}/cellNexus-metadata/census_sample_metadata.2.3.0.parquet".format(REMOTE_URL)
MIN_EXPECTED_SIZE = 5000000

assay_map = {"counts": "counts", "cpm": "cpm", "sct": "sct"}

duckdb.DuckDBPyRelation.get_anndata = lambda self, **kwargs: get_anndata(self, **kwargs)
duckdb.DuckDBPyRelation.get_pseudobulk = lambda self, **kwargs: get_pseudobulk(self, **kwargs)


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
            
def get_metadata_url(filename: str) -> str:
    r""" Helper function to construct the full URL for a given metadata filename. This allows users to easily access different metadata files by providing just the filename.
    Args:
        filename (str): The name of the metadata file (e.g., "cellNexus_lr_signaling_pathway_strength_DEMO.parquet").
    Returns:
        str: The full URL for the metadata file.
    """
    return "{}/cellNexus-metadata/{}".format(REMOTE_URL, filename)

def get_cell_communication_strength(
    parquet_url: str = "{}/cellNexus-metadata/cellNexus_lr_signaling_pathway_strength_DEMO.parquet".format(REMOTE_URL),
    cache_dir: os.PathLike[str] = _get_default_cache_dir(),
) -> tuple[duckdb.DuckDBPyConnection, duckdb.DuckDBPyRelation]:
    r"""
    Downloads a parquet file with cell communication strength data into a cache folder. This file is automatically imported into DuckDB for filtering and manipulation.
    Args:
         parquet_url (str): Provides the capability of using a customized URL for local server parquet files.
         cache_dir (str): Path to the folder to locate the parquet file.
     Returns:
         A tuple containing a DuckDB connection and a DuckDB relation with the cell communication strength data.
     Example:
         >>> conn, metadata = get_cell_communication_strength(parquet_url=get_metadata_url("cellNexus_lr_signaling_pathway_strength_DEMO.parquet"))
         >>> metadata.filter("source_cell_type = 'T cell' AND target_cell_type = 'B cell'").fetchdf()
         source_cell_type target_cell_type signaling_pathway strength
    """
    return get_metadata(parquet_url=parquet_url, cache_dir=cache_dir)

# function to get metadata
def get_metadata(
    parquet_url: str = METADATA_URL,
    cache_dir: os.PathLike[str] = _get_default_cache_dir(),
) -> tuple[duckdb.DuckDBPyConnection, duckdb.DuckDBPyRelation]:
    r""" Downloads a parquet file with the Human Cell Atlas metadata into a cache 
    folder. This file is automatically imported into DuckDB for filtering and manipulation.

    Args:
        parquet_url (str): Provides the capability of using a customized URL for 
                           local server parquet files.
        cache_dir (str): Path to the folder to locate the parquet file.
    Returns:
        A tuple containing a DuckDB connection and a DuckDB relation with the metadata.
    Example:
        >>> conn, metadata = get_metadata()
    """


    
    parquet_local = Path(cache_dir) / parquet_url.split("/")[-1]

    if not parquet_local.exists() or not is_parquet_valid(parquet_local):
        print("File is missing or corrupted. Re-downloading...")
        parquet_local.unlink(missing_ok=True)  # Delete the corrupted file
        _sync_remote_file(parquet_url, parquet_local)  # Re-download
    
    _sync_remote_file(parquet_url, parquet_local)
    conn = duckdb.connect()
    return conn, conn.from_parquet(str(parquet_local))

def join_census_table(
    conn: duckdb.DuckDBPyConnection,
    metadata: duckdb.DuckDBPyRelation,
    parquet_url: str = CENSUS_METADATA_URL,
    cache_dir: os.PathLike[str] = _get_default_cache_dir(),
    join_keys: list[str] = ["sample_id", "dataset_id", "observation_joinid"]
) -> duckdb.DuckDBPyRelation:
    r""" Joins the census cell metadata table with the main metadata table on the specified keys.
    Args:
        conn (duckdb.DuckDBPyConnection): An active DuckDB connection.
        metadata (duckdb.DuckDBPyRelation): The main metadata relation to join with the census table.
        parquet_url (str): URL to the census cell metadata parquet file.
        cache_dir (str): Path to the folder to locate the parquet file.
        join_keys (list[str]): List of column names to use as keys for the join operation.
    Returns:
        A DuckDB relation resulting from the left join of the main metadata with the census cell metadata on the specified keys.
    Example:
        >>> conn, metadata = get_metadata()
        >>> joined_metadata = join_census_table(conn, metadata)
    """
    parquet_local = Path(cache_dir) / parquet_url.split("/")[-1]

    if not parquet_local.exists() or not is_parquet_valid(parquet_local):
        print("File is missing or corrupted. Re-downloading...")
        parquet_local.unlink(missing_ok=True)  # Delete the corrupted file
        _sync_remote_file(parquet_url, parquet_local)  # Re-download
    
    _sync_remote_file(parquet_url, parquet_local)
    
    conn.from_parquet(str(parquet_local))
    
    census_table = conn.from_parquet(str(parquet_local))
    condition = " AND ".join(f"metadata.{k} = census_table.{k}" for k in join_keys)
    
    return metadata.set_alias("metadata").join(census_table.set_alias("census_table"), condition, how="left")

def keep_quality_cells(
    table: duckdb.DuckDBPyRelation,
    empty_droplet_col: str = "empty_droplet",
    alive_col: str = "alive",
    doublet_col: str = "scDblFinder.class"
) -> duckdb.DuckDBPyRelation:
    r""" Filters the metadata table to keep only high-quality cells based on the specified columns for empty droplets, alive status, and doublet classification.
    Args:
        table (duckdb.DuckDBPyRelation): The metadata relation to filter.
        empty_droplet_col (str): The name of the column indicating whether a cell is an empty droplet.
        alive_col (str): The name of the column indicating whether a cell is alive.
        doublet_col (str): The name of the column indicating the doublet classification of a cell.
    Returns:
        A DuckDB relation filtered to include only high-quality cells that are not empty droplets, are alive, and are not classified as doublets.
    Example:
        >>> conn, metadata = get_metadata()
        >>> filtered_metadata = keep_quality_cells(metadata)
    """
    table = table.filter(f"""
                         "{empty_droplet_col}" == false AND
                         "{alive_col}" == true AND
                         "{doublet_col}" != 'doublet'
                        """)
    
    return table

def sync_assay_files(
    url: str = ASSAY_URL,
    cache_dir: Path = _get_default_cache_dir(),
    subdir: str = "",
    atlas: str = "",
    cell_aggregation: str = "",
    files: Iterable[str] = [],
):
    for file in files:
        if cell_aggregation == "single_cell":
            sub_url = f"{url}/{atlas}/{subdir}/{file}"
        else:
            sub_url = f"{url}/{atlas}/{cell_aggregation}/{subdir}/{file}"
        output_filepath = cache_dir / atlas / cell_aggregation / subdir / file

        if not output_filepath.exists() or os.path.getsize(output_filepath) < MIN_EXPECTED_SIZE:
            _sync_remote_file(sub_url, output_filepath)

        yield subdir, output_filepath
        
def filter_pseudobulk(file, data):
    cells = data.filter("file_id_cellNexus_pseudobulk ="  + "'"+str(file).split("/")[-1]+"'").fetchdf()
    cell_ids = cells["sample_id"].astype(str) + "___" + cells["cell_type_unified_ensemble"].astype(str)
    anndata = ad.read_h5ad(file)
    ann = anndata[cell_ids.unique()].copy()

    columns_to_remove = ["cell_id", "cell_type", "file_id_cellNexus_single_cell",
                         "cell_type_ontology_term_id",
                         "observation_joinid", "ensemble_joinid",
                         "nFeature_expressed_in_sample", "nCount_RNA", "data_driven_ensemble", "cell_type_unified",
                         "empty_droplet", "observation_originalid", "alive", "scDblFinder.class", "is_immune"]
    subdata = cells.drop(columns=[col for col in columns_to_remove if col in cells])
    pattern = '|'.join(re.escape(s) for s in ["metacell","azimuth","monaco","blueprint","subsets_","high_"])

    # Find matching columns and drop them
    cols_to_drop = subdata.columns[subdata.columns.str.contains(pattern, case=False, regex=True)]
    subdata = subdata.drop(columns=cols_to_drop)
    subdata = subdata.drop_duplicates(subset=["sample_id", "cell_type_unified_ensemble"], keep='last')
    subdata.index = subdata["sample_id"]+"___"+subdata["cell_type_unified_ensemble"]

    ann.obs = subdata.reindex(ann.obs.index)
    return ann

def filter_metacell(file, data):
    df = data.filter("file_id_cellNexus_single_cell ="  + "'"+str(file).split("/")[-1]+"'").fetchdf()
    df["file_id_cellNexus_metacell"] = df["file_id_cellNexus_single_cell"].astype(str)
    filt_ad = ad.read_h5ad(file)
    
    columns = ["sample_id","metacell_2","metacell_id","dataset_id", "assay", "assay_ontology_term_id", 
        "development_stage", "development_stage_ontology_term_id", "disease", "disease_ontology_term_id", 
        "donor_id", "experiment___", "explorer_url", "feature_count", "is_primary_data", 
        "organism", "organism_ontology_term_id", "published_at", "raw_data_location", 
        "revised_at", "sample_heuristic", "schema_version", "self_reported_ethnicity", 
        "self_reported_ethnicity_ontology_term_id", "sex", "sex_ontology_term_id", "tissue", 
        "tissue_ontology_term_id", "tissue_type", "title", "tombstone", "url", "age_days", 
        "tissue_groups", "atlas_id", "sample_chunk", "file_id_cellNexus_single_cell", 
        "file_id_cellNexus_metacell", "dir_prefix"]
    filt_ad.obs = filt_ad.obs[[c for c in columns if c in filt_ad.obs.columns]].drop_duplicates()

    return filt_ad


def filter_single_cell(file, data):
    cells = data.filter("file_id_cellNexus_single_cell ="  + "'"+str(file).split("/")[-1]+"'").fetchdf()
    cells["cell_id"] = cells["cell_id"].astype(int).astype(str)
    anndata = ad.read_h5ad(file)
    anndata.obs.index = anndata.obs.index.astype(str)
    cells = cells[cells["cell_id"].isin(anndata.obs.index)]
    cell_ids = cells["cell_id"].astype(int).astype(str)

    anndata = anndata[cell_ids].copy()
    anndata.obs = cells
    anndata.obs.index = anndata.obs["cell_id"]

    return anndata
    
def _anndata_constructor(
    data: duckdb.DuckDBPyRelation | pd.DataFrame,
    assays: str = "counts",
    cell_aggregation: str = "single_cell",
    cache_directory: Path = _get_default_cache_dir(),
    features: Iterable = slice(None, None, None)
) -> ad.AnnData:
    
    # error checking
    assays_list = [assays] if isinstance(assays, str) else assays
    assert all(a in assay_map for a in assays_list), f"assays must be one or more of {list(assay_map.keys())}"
    assert isinstance(cache_directory, Path), "cache_directory must be a Path"
    
    if isinstance(data, pd.DataFrame):
        data = duckdb.from_df(data)
    
    cache_directory.mkdir(exist_ok=True, parents=True)

    if cell_aggregation != "single_cell" and cell_aggregation != "pseudobulk": data = data.filter(cell_aggregation + " IS NOT NULL")
    
    if cell_aggregation == "pseudobulk":
        files_to_read = (
            data.project("file_id_cellNexus_pseudobulk").distinct().fetchdf()["file_id_cellNexus_pseudobulk"]
        )
    else:
        files_to_read = (
            data.project("file_id_cellNexus_single_cell").distinct().fetchdf()["file_id_cellNexus_single_cell"]
        )
    
    atlas = data.project('"atlas_id"').distinct().fetchdf()["atlas_id"][0]                                                                                                                      
    
    result = None
    for assay in assays_list:
        synced = sync_assay_files(
            url=ASSAY_URL, cache_dir=cache_directory, atlas=atlas, subdir=assay, cell_aggregation=cell_aggregation, files=files_to_read
        )

        if cell_aggregation == "pseudobulk":
            for _, files in itertools.groupby(synced, key=lambda x: x[0]):
                ads = [filter_pseudobulk(file[1], data) for file in files]
        elif cell_aggregation == "metacell_2":
            for _, files in itertools.groupby(synced, key=lambda x: x[0]):
                ads = [filter_metacell(file[1], data) for file in files]
        else:
            for _, files in itertools.groupby(synced, key=lambda x: x[0]):
                ads = [filter_single_cell(file[1], data) for file in files]

        concatenated = ad.concat(ads, index_unique="_")

        if result is None:
            result = concatenated
            result.layers[assay] = result.X.copy()
        else:
            result.layers[assay] = concatenated[result.obs_names, :].X.copy()

    return result[:, features]

def get_anndata(
    data: duckdb.DuckDBPyRelation | pd.DataFrame,
    assays: Literal["counts", "cpm", "sct"] = "counts",
    cache_directory: Path = _get_default_cache_dir(),
    features: Iterable = slice(None, None, None)
):
    r""" Main function to get the :obj:`AnnData` object with the single cell data and the metadata.

    Args:
        data (duckdb.DuckDBPyRelation | pd.DataFrame): Metadata filtered with information of experiments of interest.
        assays (str): Type of gene expression data `counts` (raw), `cpm` (normalized), or `sct` (sctransform normalized).
        cache_directory (str): Path to the folder to locate the parquet file.
        features (Iterable): List of Ensembl ids to subset the :obj:`AnnData` object to the
                             specific genes of interest.
    Returns:
        An :obj:`AnnData` object containing the single cell data and the metadata.
    Example:
        >>> conn, metadata = get_metadata()
        >>> filtered_metadata = keep_quality_cells(metadata)
        >>> adata = get_anndata(filtered_metadata, assays="cpm", features=['ENSG00000134644'])
    """
    return _anndata_constructor(data, assays=assays, cell_aggregation="single_cell", cache_directory=_get_default_cache_dir(), features=features)

def get_pseudobulk(
    data: duckdb.DuckDBPyRelation | pd.DataFrame,
    assays: Literal["counts", "cpm", "sct"] = "counts",
    cache_directory: Path = _get_default_cache_dir(),
    features: Iterable = slice(None, None, None)
):
    r""" Main function to get the :obj:`AnnData` object with the pseudobulk data and the metadata.

    Args:
        data (duckdb.DuckDBPyRelation | pd.DataFrame): Metadata filtered with information of experiments of interest.
        assays (str): Type of gene expression data `counts` (raw), `cpm` (normalized), or `sct` (sctransform normalized).
        cache_directory (str): Path to the folder to locate the parquet file.
        features (Iterable): List of Ensembl ids to subset the :obj:`AnnData` object to the
                             specific genes of interest.
    Returns:
        An :obj:`AnnData` object containing the pseudobulk data and the metadata.
    Example:
        >>> conn, metadata = get_metadata()
        >>> filtered_metadata = keep_quality_cells(metadata)
        >>> pseudobulk_adata = get_pseudobulk(filtered_metadata, assays="cpm", features=['ENSG00000134644'])
    """
    return _anndata_constructor(data, assays=assays, cell_aggregation="pseudobulk", cache_directory=_get_default_cache_dir(), features=features)

"""
def get_metacell(
    data: duckdb.DuckDBPyRelation,
    cell_aggregation: str = "metacell_2",
    assays: Literal["counts", "cpm"] = "counts",
    cache_directory: Path = _get_default_cache_dir(),
    features: Iterable = slice(None, None, None)
):
    r Main function to get the :obj:`AnnData` object with the metacell data and the metadata.

    Args:
        data (duckdb.DuckDBPyRelation | pd.DataFrame): Metadata filtered with information of experiments of interest.
        assays (str): Type of gene expression data `counts` (raw) or `cpm` (normalized).
        cell_aggregation (str): Type of cell aggregation to be used: `pseudobulk` or `metacell`.
        cache_directory (str): Path to the folder to locate the parquet file.
        features (Iterable): List of Ensembl ids to subset the :obj:`AnnData` object to the
                             specific genes of interest.
    
    return _get_anndata(data, assays=assays, cell_aggregation=cell_aggregation, cache_directory=cache_directory, features=features)
"""