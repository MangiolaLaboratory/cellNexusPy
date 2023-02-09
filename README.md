# CuratedAtlasQueryPy
    
## Import the package


```python
import curatedatlasquerypy
import pandas as pd
import sqlalchemy
```

## Connect to the metadata database


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
