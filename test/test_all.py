import pytest
from cellnexuspy import get_metadata, get_anndata, get_pseudobulk, keep_quality_cells, get_cell_communication_strength, SAMPLE_DATABASE_URL

def test_single_cell_counts():
    con, table = get_metadata(cloud_metadata = SAMPLE_DATABASE_URL)
    table = keep_quality_cells(table)

    adata = get_anndata(table.limit(10), assays = "counts")
    assert(adata.layers["counts"].shape[0] == 10)
    assert(len(table) == 45427)
    assert(any(adata.obs.columns == "file_id_cellNexus_single_cell"))

def test_single_cell_cpm():
    con, table = get_metadata(cloud_metadata = SAMPLE_DATABASE_URL)
    table = keep_quality_cells(table)

    adata = get_anndata(table.limit(10), assays = "cpm")
    assert(adata.layers["cpm"].shape[0] == 10)
    assert(adata.layers["cpm"].shape[1] == 33145)
    assert(any(adata.obs.columns == "file_id_cellNexus_single_cell"))

def test_single_cell_sct():
    con, table = get_metadata(cloud_metadata = SAMPLE_DATABASE_URL)
    table = keep_quality_cells(table)

    adata = get_anndata(table.limit(10), assays = "sct")
    assert(adata.layers["sct"].shape[0] == 10)
    assert(adata.layers["sct"].shape[1] == 33145)
    assert(any(adata.obs.columns == "file_id_cellNexus_single_cell"))

def test_pseudobulk():
    con, table = get_metadata(cloud_metadata = SAMPLE_DATABASE_URL)
    table = keep_quality_cells(table)

    adata = get_pseudobulk(table.limit(10))
    assert(adata.layers["counts"].shape[0] == 4)
    assert(len(table) == 45427)
    assert(any(adata.obs.columns == "file_id_cellNexus_pseudobulk"))

def test_cell_communication_strength():
    con, table = get_cell_communication_strength(cloud_metadata = "cellNexus_lr_signaling_pathway_strength_DEMO.parquet")
    assert(len(table) == 6)
    assert("sample_id" in table.columns)
    assert("source" in table.columns)
    assert("annotation" in table.columns)
