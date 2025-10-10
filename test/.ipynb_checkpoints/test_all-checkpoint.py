import pytest
from cellnexuspy import get_metadata, get_anndata

def test_single_cell():
    con, table = get_metadata()
    table = table.filter("""
        empty_droplet = 'false'
        AND alive = 'true'
        AND "scDblFinder.class" != 'doublet'
        AND feature_count >= 5000
    """)
    
    query = table.filter("""
        self_reported_ethnicity = 'African'
        AND assay LIKE '%10%'
        AND tissue = 'lung parenchyma'
        AND cell_type LIKE '%CD4%'
        AND feature_count >= 5000
    """)

    adata = get_anndata(query.limit(10), assay ="counts")
    assert(adata.X.shape[0] == 10)
    assert(len(query) == 1780)
    assert(any(adata.obs.columns == "file_id_cellNexus_single_cell"))

def test_pseudobulk():
    con, table = get_metadata()
    table = table.filter("""
        empty_droplet = 'false'
        AND alive = 'true'
        AND "scDblFinder.class" != 'doublet'
        AND feature_count >= 5000
    """)
    
    query = table.filter("""
        self_reported_ethnicity = 'African'
        AND assay LIKE '%10%'
        AND tissue = 'lung parenchyma'
        AND cell_type LIKE '%CD4%'
        AND feature_count >= 5000
    """)

    adata = get_anndata(query.limit(10), aggregation = "pseudobulk")
    assert(adata.X.shape[0] == 7)
    assert(len(query) == 1780)
    assert(any(adata.obs.columns == "file_id_cellNexus_pseudobulk"))

def test_metacell():
    con, table = get_metadata()
    table = table.filter("""
        empty_droplet = 'false'
        AND alive = 'true'
        AND "scDblFinder.class" != 'doublet'
        AND feature_count >= 5000
    """)
    
    query = table.filter("""
        self_reported_ethnicity = 'African'
        AND assay LIKE '%10%'
        AND tissue = 'lung parenchyma'
        AND cell_type LIKE '%CD4%'
        AND feature_count >= 5000
    """)

    adata = get_anndata(query.limit(10), aggregation = "metacell_2")
    assert(adata.X.shape[0] == 10)
    assert(len(query) == 1780)
    assert(any(adata.obs.columns == "file_id_cellNexus_metacell"))