from curated_atlas_query_py import *

def test_get_counts():
    con, table = get_metadata(cache_dir='/vast/projects/cellxgene_curated/')
    sce = get_anndata(table.limit(1))
    print(sce)

def test_get_cpm():
    con, table = get_metadata(cache_dir='/vast/projects/cellxgene_curated/')
    sce = get_anndata(table.limit(1), assays=["cpm"])
    print(sce)
