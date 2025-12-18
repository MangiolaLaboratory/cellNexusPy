from cellnexuspy import get_metadata, get_anndata

conn, table = get_metadata()

table = table.filter("""
    empty_droplet = 'false'
    AND alive = 'true'
    AND "scDblFinder.class" != 'doublet'
    AND feature_count >= 5000
""")

query = table.filter("""
    cell_type_unified_ensemble = 'cd14 mono'
""")

adata = get_anndata(query, assay = 'cpm')

adata.obs.index.name = None
adata.obs["run_from_cell_id"] = adata.obs["run_from_cell_id"].fillna("NA").astype(str)
adata.obs["suspension_type"] = adata.obs["suspension_type"].fillna("NA").astype(str)
adata.obs["x_approximate_distribution"] = adata.obs["x_approximate_distribution"].fillna("NA").astype(str)

adata.write_h5ad("whole_parquet.h5ad")
