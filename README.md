<img src="inst/logo.png" width="120px" height="139px">

# CuratedAtlasQueryPy


CuratedAtlasQuery is a query interface that allow the programmatic exploration and retrival o the harmonised, curated and reannotated CELLxGENE single-cell human cell atlas. Data can be retrieved at cell, sample, or dataset levels based on filtering criteria.

## Query interface

### Import the package
```python
import curatedatlasquerypy
import pandas as pd
import sqlalchemy
```

### Connect to the metadata database
```python
# Use the cache_dir argument to point to the WEHI central data store.
eng, mdtab = curatedatlasquerypy.get_metadata(cache_dir='/vast/projects/cellxgene_curated')
print(mdtab.columns)


```

    ReadOnlyColumnCollection(metadata..cell, metadata.sample_id_db, metadata..sample, ..., metadata.cell_annotation_blueprint_singler, metadata.n_cell_type_in_tissue, metadata.n_tissue_in_cell_type)

### Explore the tissue
SQLAlchemy core syntax can be used to form and execute the query


```python
q = sqlalchemy.select(mdtab.c.tissue, mdtab.c.file_id).distinct()
with eng.connect() as conn:
    mddf = pd.DataFrame(conn.execute(q))
    
mddf
```


```
                 tissue                               file_id
0        adipose tissue  343f46f2-7cdd-4da8-bc7f-50a18b2c0e8e
1        adipose tissue  5cb7ccfc-41d5-4613-82ce-e6d1888a0228
2        adipose tissue  700695a4-b3cc-4352-9c6c-25bf054d016b
3        adipose tissue  76afd5a3-7458-4d77-b6e9-f47c059047e3
4        adipose tissue  e40591e7-0e5a-4bef-9b60-7015abe5b17f
..                  ...                                   ...
886         vasculature  76afd5a3-7458-4d77-b6e9-f47c059047e3
887      vault of skull  e40591e7-0e5a-4bef-9b60-7015abe5b17f
888        venous blood  a84321f2-5b06-4274-8f96-e1876340600e
889  vermiform appendix  e40591e7-0e5a-4bef-9b60-7015abe5b17f
890        zone of skin  c48402e4-e7db-4c82-a9e9-51e285e5165c

[891 rows x 2 columns]
```

### Querying using raw SQL
For those who prefer writing raw SQL over SQLalchemy, you can use pandas `read_sql_query()` instead of SQLAlchemy.


```python
eng, mdtab = curatedatlasquerypy.get_metadata()

with eng.connect() as conn:
    query = sqlalchemy.text("SELECT * FROM metadata \
                            WHERE ethnicity='African' \
                                AND assay LIKE '%10x%' \
                                AND tissue='lung parenchyma' \
                                AND cell_type LIKE '%CD4%'")
    mddf = pd.read_sql_query(query, conn)
    
eng.dispose()
mddf
```

## Download single-cell RNA sequencing counts

### Query raw counts
```python
# forming the query
q = sqlalchemy.select('*').where( \
                                 mdtab.c.ethnicity == "African", \
                                 mdtab.c.assay.like('%10x%'), \
                                 mdtab.c.tissue == "lung parenchyma", \
                                 mdtab.c.cell_type.like('%CD4%') \
                                )
# executing query                                
with eng.connect() as conn:
    mddf = pd.DataFrame(conn.execute(q))

# obtaining raw counts
res = curatedatlasquerypy.get_SingleCellExperiment(mddf, \
                                                   assays = ['counts'], \
                                                   cache_directory='/vast/projects/cellxgene_curated/anndata' \
                                                  )
res
```
```
AnnData object with n_obs × n_vars = 21285 × 60661
```
### Query counts scaled per million
```python
# forming the query
q = sqlalchemy.select('*').where( \
                                 mdtab.c.ethnicity == "African", \
                                 mdtab.c.assay.like('%10x%'), \
                                 mdtab.c.tissue == "lung parenchyma", \
                                 mdtab.c.cell_type.like('%CD4%') \
                                )
# executing query                                
with eng.connect() as conn:
    mddf = pd.DataFrame(conn.execute(q))

# obtaining scaled counts
res = curatedatlasquerypy.get_SingleCellExperiment(mddf, \
                                                   assays = ['cpm'], \
                                                   cache_directory='/vast/projects/cellxgene_curated/anndata' \
                                                  )
res
```
```
AnnData object with n_obs × n_vars = 21285 × 60661
```

### Extract only a subset of genes
```python
# forming the query
q = sqlalchemy.select('*').where( \
                                 mdtab.c.ethnicity == "African", \
                                 mdtab.c.assay.like('%10x%'), \
                                 mdtab.c.tissue == "lung parenchyma", \
                                 mdtab.c.cell_type.like('%CD4%') \
                                )
# executing query                                
with eng.connect() as conn:
    mddf = pd.DataFrame(conn.execute(q))

# obtaining scaled counts
res = curatedatlasquerypy.get_SingleCellExperiment(mddf, \
                                                   assays = ['cpm'], \
                                                   features = ['PUM1'], \
                                                   cache_directory='/vast/projects/cellxgene_curated/anndata' \
                                                  )
                                                  
res
```
```
AnnData object with n_obs × n_vars = 21285 × 1
```

## Cell metadata
Dataset-specific columns (definitions available at cellxgene.cziscience.com)

`cell_count`, `collection_id`, `created_at.x`, `created_at.y`, `dataset_deployments`, `dataset_id`, `file_id`, `filename`, `filetype`, `is_primary_data.y`, `is_valid`, `linked_genesets`, `mean_genes_per_cell`, `name`, `published`, `published_at`, `revised_at`, `revision`, `s3_uri`, `schema_version`, `tombstone`, `updated_at.x`, `updated_at.y`, `user_submitted`, `x_normalization`

Sample-specific columns (definitions available at cellxgene.cziscience.com)

`.sample`, `.sample_name`, `age_days`, `assay`, `assay_ontology_term_id`, `development_stage`, `development_stage_ontology_term_id`, `ethnicity`, `ethnicity_ontology_term_id`, `experiment___`, `organism`, `organism_ontology_term_id`, `sample_placeholder`, `sex`, `sex_ontology_term_id`, `tissue`, `tissue_harmonised`, `tissue_ontology_term_id`, `disease`, `disease_ontology_term_id`, `is_primary_data.x`

Cell-specific columns (definitions available at cellxgene.cziscience.com)

`.cell`, `cell_type`, `cell_type_ontology_term_idm`, `cell_type_harmonised`, `confidence_class`, `cell_annotation_azimuth_l2`, `cell_annotation_blueprint_singler`

Through harmonisation and curation we introduced custom column, not present in the original CELLxGENE metadata
* `tissue_harmonised`: a coarser tissue name for better filtering
* `age_days`: the number of days corresponding to the age
* `cell_type_harmonised`: the consensus call identiti (for immune cells) using the original and three novel annotations using Seurat Azimuth and SingleR
* `confidence_class`: an ordinal class of how confident cell_type_harmonised is. 1 is complete consensus, 2 is 3 out of four and so on.
* `cell_annotation_azimuth_l2`: Azimuth cell annotation
* `cell_annotation_blueprint_singler`: SingleR cell annotation using Blueprint reference
* `cell_annotation_blueprint_monaco`: SingleR cell annotation using Monaco reference
* `sample_id_db`: Sample subdivision for internal use
* `file_id_db`: File subdivision for internal use
* `.sample`: Sample ID
* `.sample_name`: How samples were defined
