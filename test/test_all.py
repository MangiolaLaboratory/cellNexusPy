from curated_atlas_query_py import *

def test_get_sce():
    con, table = get_metadata(cache_dir='/vast/projects/cellxgene_curated/')
    sce = get_SingleCellExperiment(table.limit(1))
    print(sce)