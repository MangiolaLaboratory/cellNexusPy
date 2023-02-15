# Curated Atlas Query (Python)

## Importing the package


```python
from curated_atlas_query_py import get_metadata, get_anndata
```

## Getting the metadata
The `get_metadata()` function returns a database connection and a DuckDB table.
The table can be used to query the metadata, while the connection's main purpose is to be closed when you are finished.


```python
conn, table = get_metadata()
table
```


    FloatProgress(value=0.0, layout=Layout(width='100%'), style=ProgressStyle(bar_color='black'))





    ┌────────────────────┬──────────────────────┬──────────────────────┬───┬──────────────────────┬──────────────────────┐
    │       .cell        │     sample_id_db     │       .sample        │ … │ n_cell_type_in_tis…  │ n_tissue_in_cell_t…  │
    │      varchar       │       varchar        │       varchar        │   │        int64         │        int64         │
    ├────────────────────┼──────────────────────┼──────────────────────┼───┼──────────────────────┼──────────────────────┤
    │ AAACCTGAGAGACGAA_1 │ 8a0fe0928684d6765d…  │ 5f20d7daf6c42f4f91…  │ … │                 NULL │                 NULL │
    │ AAACCTGAGTTGTCGT_1 │ 8a0fe0928684d6765d…  │ 5f20d7daf6c42f4f91…  │ … │                 NULL │                 NULL │
    │ AAACCTGCAGTCGATT_1 │ 02eb2ebcb5f802e271…  │ 5f20d7daf6c42f4f91…  │ … │                 NULL │                 NULL │
    │ AAACCTGCAGTTCATG_1 │ 02eb2ebcb5f802e271…  │ 5f20d7daf6c42f4f91…  │ … │                 NULL │                 NULL │
    │ AAACCTGGTCTAAACC_1 │ 8a0fe0928684d6765d…  │ 5f20d7daf6c42f4f91…  │ … │                 NULL │                 NULL │
    │ AAACCTGTCGTACCGG_1 │ 8a0fe0928684d6765d…  │ 5f20d7daf6c42f4f91…  │ … │                 NULL │                 NULL │
    │ AAACCTGTCTTGTACT_1 │ 8a0fe0928684d6765d…  │ 5f20d7daf6c42f4f91…  │ … │                 NULL │                 NULL │
    │ AAACGGGAGTACGTTC_1 │ 8a0fe0928684d6765d…  │ 5f20d7daf6c42f4f91…  │ … │                 NULL │                 NULL │
    │ AAACGGGAGTAGGTGC_1 │ 02eb2ebcb5f802e271…  │ 5f20d7daf6c42f4f91…  │ … │                 NULL │                 NULL │
    │ AAACGGGAGTGGGATC_1 │ 8a0fe0928684d6765d…  │ 5f20d7daf6c42f4f91…  │ … │                 NULL │                 NULL │
    │         ·          │          ·           │          ·           │ · │                   ·  │                   ·  │
    │         ·          │          ·           │          ·           │ · │                   ·  │                   ·  │
    │         ·          │          ·           │          ·           │ · │                   ·  │                   ·  │
    │ CAGCGACAGCTGTTCA_4 │ 1e1a5f41371bd8c9c8…  │ 03c6a35e026a17b3a0…  │ … │                 NULL │                 NULL │
    │ CAGCGACCAATGAATG_4 │ 1e1a5f41371bd8c9c8…  │ 03c6a35e026a17b3a0…  │ … │                 NULL │                 NULL │
    │ CAGCGACCACAGACAG_4 │ 1e1a5f41371bd8c9c8…  │ 03c6a35e026a17b3a0…  │ … │                 NULL │                 NULL │
    │ CAGCGACCACTAAGTC_4 │ 1e1a5f41371bd8c9c8…  │ 03c6a35e026a17b3a0…  │ … │                 NULL │                 NULL │
    │ CAGCGACGTATAGGTA_4 │ c6296550d1bf737378…  │ 03c6a35e026a17b3a0…  │ … │                 NULL │                 NULL │
    │ CAGCGACGTGAGTGAC_4 │ 1e1a5f41371bd8c9c8…  │ 03c6a35e026a17b3a0…  │ … │                 NULL │                 NULL │
    │ CAGCGACGTGTTGAGG_4 │ c6296550d1bf737378…  │ 03c6a35e026a17b3a0…  │ … │                 NULL │                 NULL │
    │ CAGCGACTCAGCTTAG_4 │ 1e1a5f41371bd8c9c8…  │ 03c6a35e026a17b3a0…  │ … │                 NULL │                 NULL │
    │ CAGCGACTCCTTTCTC_4 │ 1e1a5f41371bd8c9c8…  │ 03c6a35e026a17b3a0…  │ … │                 NULL │                 NULL │
    │ CAGCGACTCGCGCCAA_4 │ 1e1a5f41371bd8c9c8…  │ 03c6a35e026a17b3a0…  │ … │                 NULL │                 NULL │
    ├────────────────────┴──────────────────────┴──────────────────────┴───┴──────────────────────┴──────────────────────┤
    │ ? rows (>9999 rows, 20 shown)                                                                 56 columns (5 shown) │
    └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘



### Querying the metadata
The DuckDB table can be queried using a number of methods [described here](https://duckdb.org/docs/api/python/reference/#duckdb.DuckDBPyRelation). In particular:
* [`.filter()`](https://duckdb.org/docs/api/python/reference/#duckdb.DuckDBPyRelation.filter): filters the metadata using a string expression
* [`.aggregate()`](https://duckdb.org/docs/api/python/reference/#duckdb.DuckDBPyRelation.aggregate): groups by one or more columns, and calculates some aggregate statistics such as counts
* [`.fetchdf()`](https://duckdb.org/docs/api/python/reference/#duckdb.DuckDBPyRelation.fetchdf): Executes the query and returns it as a pandas DataFrame


```python
table.aggregate("tissue, file_id, COUNT(*) as n", group_expr="tissue, file_id").fetchdf()
```




                        tissue                               file_id        n
    0                    blood  07beec85-51be-4d73-bb80-8f85b7b643d5  1399186
    1         cortex of kidney  38eaca52-0ce4-4be2-8173-c6bab05f308a   122914
    2            renal medulla  38eaca52-0ce4-4be2-8173-c6bab05f308a    57086
    3            renal papilla  38eaca52-0ce4-4be2-8173-c6bab05f308a    20338
    4            adrenal gland  5c1cc788-2645-45fb-b1d9-2f43d368bba8    95588
    ..                     ...                                   ...      ...
    886          renal medulla  ffc36957-efef-4c98-879c-833215e850a9    12531
    887            conjunctiva  343f46f2-7cdd-4da8-bc7f-50a18b2c0e8e     2084
    888       cortex of kidney  f7e94dbb-8638-4616-aaf9-16e2212c369f     4628
    889  mesenteric lymph node  59dfc135-19c1-4380-a9e8-958908273756    13958
    890           renal pelvis  f7e94dbb-8638-4616-aaf9-16e2212c369f      163
    
    [891 rows x 3 columns]




```python
table.filter("ethnicity == 'African'")
```




    ┌──────────────────────┬──────────────────────┬──────────────────────┬───┬──────────────────────┬──────────────────────┐
    │        .cell         │     sample_id_db     │       .sample        │ … │ n_cell_type_in_tis…  │ n_tissue_in_cell_t…  │
    │       varchar        │       varchar        │       varchar        │   │        int64         │        int64         │
    ├──────────────────────┼──────────────────────┼──────────────────────┼───┼──────────────────────┼──────────────────────┤
    │ AGGGAGTAGCGTTTAC_S…  │ 9da02eab40e49d1a07…  │ 20071ec5a126508641…  │ … │                   28 │                   32 │
    │ ATTGGACAGCCGATTT_F…  │ 89ec472baa9d514068…  │ 4fc10a6b85e5fa688b…  │ … │                   28 │                   32 │
    │ CCCAGTTCATACCATG_S…  │ 26750b2a06c447f7f2…  │ 055e5172053464e8ef…  │ … │                   28 │                   32 │
    │ TGGACGCAGTGATCGG_S…  │ 26750b2a06c447f7f2…  │ 055e5172053464e8ef…  │ … │                   28 │                   32 │
    │ ACGGTTACAGTCTTCC_S…  │ c87e74c1cd0b6e77c9…  │ 13f5331436ecaeaeff…  │ … │                   28 │                   32 │
    │ CTACCCAAGGCTCTCG_S…  │ e23e69a42aa5ddc1af…  │ 13f5331436ecaeaeff…  │ … │                   28 │                   32 │
    │ ACAGCCGGTCCGTTAA_F…  │ 33cdeb84ae1462d723…  │ 4fc10a6b85e5fa688b…  │ … │                   28 │                   31 │
    │ CCTTCCCGTCGTCTTC_S…  │ a1f6193169da254c02…  │ e87dae9bb6023ed28e…  │ … │                   28 │                   32 │
    │ CACGTTCGTGCCCAGT_S…  │ e23e69a42aa5ddc1af…  │ 13f5331436ecaeaeff…  │ … │                   28 │                   32 │
    │ GTAAGTCCACTGCATA_S…  │ c87e74c1cd0b6e77c9…  │ 13f5331436ecaeaeff…  │ … │                   28 │                   32 │
    │          ·           │          ·           │          ·           │ · │                    · │                    · │
    │          ·           │          ·           │          ·           │ · │                    · │                    · │
    │          ·           │          ·           │          ·           │ · │                    · │                    · │
    │ TGGAGGACAGGTCAAG_S…  │ 134ec519fba2c8337f…  │ 13f5331436ecaeaeff…  │ … │                   28 │                   32 │
    │ CTAATGGCAGTGACAG_F…  │ 61de653353b5def308…  │ 45510770cc8d68cd8d…  │ … │                   28 │                   32 │
    │ AGCATACTCGTAGATC_S…  │ 5ba60d5bcaa394b144…  │ 24a33a79b2dd6fbe24…  │ … │                   28 │                   32 │
    │ GCTTCCAAGCTAAGAT_S…  │ b6dc430c282444889a…  │ 24a33a79b2dd6fbe24…  │ … │                   28 │                   32 │
    │ D367_Biop_Int1_CGT…  │ de0f5f1f69f8755b97…  │ 0d8aaa61f1c2206a0e…  │ … │                   28 │                   32 │
    │ TGATTTCCACATTCGA_S…  │ c87e74c1cd0b6e77c9…  │ 13f5331436ecaeaeff…  │ … │                   28 │                   32 │
    │ GTTCGGGCAACACCCG_S…  │ 4f0bb1af662dbc477e…  │ 948efa032d715a169f…  │ … │                   28 │                   32 │
    │ ACATGCATCCTGGGTG_S…  │ e23e69a42aa5ddc1af…  │ 13f5331436ecaeaeff…  │ … │                   28 │                   32 │
    │ ATTTCACGTCCACTTC_S…  │ ce4d8fac7898fb096c…  │ 318d4b5b99cb76ef40…  │ … │                   28 │                   32 │
    │ AAGCCATGTGACCTGC_S…  │ 567446369eec47961e…  │ 13f5331436ecaeaeff…  │ … │                   28 │                   32 │
    ├──────────────────────┴──────────────────────┴──────────────────────┴───┴──────────────────────┴──────────────────────┤
    │ ? rows (>9999 rows, 20 shown)                                                                   56 columns (5 shown) │
    └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘




```python
query = table.filter("""
    ethnicity == 'African'
    AND assay LIKE '%10%'
    AND tissue == 'lung parenchyma'
    AND cell_type LIKE '%CD4%'
""")
query
```




    ┌──────────────────────┬──────────────────────┬──────────────────────┬───┬──────────────────────┬──────────────────────┐
    │        .cell         │     sample_id_db     │       .sample        │ … │ n_cell_type_in_tis…  │ n_tissue_in_cell_t…  │
    │       varchar        │       varchar        │       varchar        │   │        int64         │        int64         │
    ├──────────────────────┼──────────────────────┼──────────────────────┼───┼──────────────────────┼──────────────────────┤
    │ ACAGCCGGTCCGTTAA_F…  │ 33cdeb84ae1462d723…  │ 4fc10a6b85e5fa688b…  │ … │                   28 │                   31 │
    │ GGGAATGAGCCCAGCT_F…  │ 33cdeb84ae1462d723…  │ 4fc10a6b85e5fa688b…  │ … │                   28 │                   32 │
    │ TCTTCGGAGTAGCGGT_F…  │ 33cdeb84ae1462d723…  │ 4fc10a6b85e5fa688b…  │ … │                   28 │                   32 │
    │ CCTTACGAGAGCTGCA_F…  │ 33cdeb84ae1462d723…  │ 4fc10a6b85e5fa688b…  │ … │                   28 │                   32 │
    │ ATCTACTCAATGGAAT_F…  │ 33cdeb84ae1462d723…  │ 4fc10a6b85e5fa688b…  │ … │                   28 │                   32 │
    │ CATCAGACACCGTTGG_F…  │ c7f14e86df84af9ad1…  │ 9ef5eab00316c489a3…  │ … │                 NULL │                 NULL │
    │ AGTCTTTGTTAGTGGG_F…  │ c7f14e86df84af9ad1…  │ 9ef5eab00316c489a3…  │ … │                   28 │                   31 │
    │ CGCGTTTGTAAGTAGT_F…  │ 33cdeb84ae1462d723…  │ 4fc10a6b85e5fa688b…  │ … │                   28 │                   32 │
    │ TGGCTGGCAACGATCT_F…  │ c7f14e86df84af9ad1…  │ 9ef5eab00316c489a3…  │ … │                   28 │                   32 │
    │ TTCCCAGAGCAGGCTA_F…  │ 33cdeb84ae1462d723…  │ 4fc10a6b85e5fa688b…  │ … │                   28 │                   32 │
    │          ·           │          ·           │          ·           │ · │                    · │                    · │
    │          ·           │          ·           │          ·           │ · │                    · │                    · │
    │          ·           │          ·           │          ·           │ · │                    · │                    · │
    │ GTAACCATCGCTGTTC_S…  │ 21ef23ac07391c64ca…  │ 13f5331436ecaeaeff…  │ … │                   28 │                   32 │
    │ ACGAGCCAGGTCATCT_F…  │ 33cdeb84ae1462d723…  │ 4fc10a6b85e5fa688b…  │ … │                   28 │                   32 │
    │ CAGCATACAAGGGTCA_F…  │ 87e1dbaeee064aa213…  │ 88c152c8536575c47a…  │ … │                   28 │                   32 │
    │ TCGTACCAGAGTACCG_F…  │ c7f14e86df84af9ad1…  │ 9ef5eab00316c489a3…  │ … │                   28 │                   32 │
    │ GCGGGTTAGCGTTGCC_F…  │ c7f14e86df84af9ad1…  │ 9ef5eab00316c489a3…  │ … │                   28 │                   32 │
    │ TACTTACGTAATAGCA_F…  │ 33cdeb84ae1462d723…  │ 4fc10a6b85e5fa688b…  │ … │                   28 │                   32 │
    │ AGATAGAGTGCCTTCT_S…  │ 21ef23ac07391c64ca…  │ 13f5331436ecaeaeff…  │ … │                   28 │                   32 │
    │ CGCGGTATCCGCGCAA_S…  │ 9dfbd16390b119392a…  │ 055e5172053464e8ef…  │ … │                   28 │                   32 │
    │ TACAACGTCAGCATTG_S…  │ 21ef23ac07391c64ca…  │ 13f5331436ecaeaeff…  │ … │                   28 │                   32 │
    │ CATTCGCTCAATACCG_F…  │ 33cdeb84ae1462d723…  │ 4fc10a6b85e5fa688b…  │ … │                   28 │                   31 │
    ├──────────────────────┴──────────────────────┴──────────────────────┴───┴──────────────────────┴──────────────────────┤
    │ 1571 rows (20 shown)                                                                            56 columns (5 shown) │
    └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘



## Extracting Counts

Once you're happy with your query, you can pass it into `get_anndata()` to obtain an AnnData object:


```python
get_anndata(query, assays=["counts"])
```




    AnnData object with n_obs × n_vars = 1571 × 60661
        obs: '.cell', 'sample_id_db', '.sample', '.sample_name', 'assay', 'assay_ontology_term_id', 'file_id_db', 'cell_type', 'cell_type_ontology_term_id', 'development_stage', 'development_stage_ontology_term_id', 'disease', 'disease_ontology_term_id', 'ethnicity', 'ethnicity_ontology_term_id', 'file_id', 'is_primary_data.x', 'organism', 'organism_ontology_term_id', 'sample_placeholder', 'sex', 'sex_ontology_term_id', 'tissue', 'tissue_ontology_term_id', 'tissue_harmonised', 'age_days', 'dataset_id', 'collection_id', 'cell_count', 'dataset_deployments', 'is_primary_data.y', 'is_valid', 'linked_genesets', 'mean_genes_per_cell', 'name', 'published', 'revision', 'schema_version', 'tombstone', 'x_normalization', 'created_at.x', 'published_at', 'revised_at', 'updated_at.x', 'filename', 'filetype', 's3_uri', 'user_submitted', 'created_at.y', 'updated_at.y', 'cell_type_harmonised', 'confidence_class', 'cell_annotation_azimuth_l2', 'cell_annotation_blueprint_singler', 'n_cell_type_in_tissue', 'n_tissue_in_cell_type'



You can query counts scaled per million. This is helpful if just few genes are of interest:


```python
get_anndata(query, assays=['cpm'])
```




    AnnData object with n_obs × n_vars = 1571 × 60661
        obs: '.cell', 'sample_id_db', '.sample', '.sample_name', 'assay', 'assay_ontology_term_id', 'file_id_db', 'cell_type', 'cell_type_ontology_term_id', 'development_stage', 'development_stage_ontology_term_id', 'disease', 'disease_ontology_term_id', 'ethnicity', 'ethnicity_ontology_term_id', 'file_id', 'is_primary_data.x', 'organism', 'organism_ontology_term_id', 'sample_placeholder', 'sex', 'sex_ontology_term_id', 'tissue', 'tissue_ontology_term_id', 'tissue_harmonised', 'age_days', 'dataset_id', 'collection_id', 'cell_count', 'dataset_deployments', 'is_primary_data.y', 'is_valid', 'linked_genesets', 'mean_genes_per_cell', 'name', 'published', 'revision', 'schema_version', 'tombstone', 'x_normalization', 'created_at.x', 'published_at', 'revised_at', 'updated_at.x', 'filename', 'filetype', 's3_uri', 'user_submitted', 'created_at.y', 'updated_at.y', 'cell_type_harmonised', 'confidence_class', 'cell_annotation_azimuth_l2', 'cell_annotation_blueprint_singler', 'n_cell_type_in_tissue', 'n_tissue_in_cell_type'



We can query a subset of genes. Notice how the result only has `nvars = 1`:


```python
anndata = get_anndata(query, features = ['PUM1'], repository='file:///vast/projects/human_cell_atlas_py/anndata')
anndata
```




    AnnData object with n_obs × n_vars = 1571 × 1
        obs: '.cell', 'sample_id_db', '.sample', '.sample_name', 'assay', 'assay_ontology_term_id', 'file_id_db', 'cell_type', 'cell_type_ontology_term_id', 'development_stage', 'development_stage_ontology_term_id', 'disease', 'disease_ontology_term_id', 'ethnicity', 'ethnicity_ontology_term_id', 'file_id', 'is_primary_data.x', 'organism', 'organism_ontology_term_id', 'sample_placeholder', 'sex', 'sex_ontology_term_id', 'tissue', 'tissue_ontology_term_id', 'tissue_harmonised', 'age_days', 'dataset_id', 'collection_id', 'cell_count', 'dataset_deployments', 'is_primary_data.y', 'is_valid', 'linked_genesets', 'mean_genes_per_cell', 'name', 'published', 'revision', 'schema_version', 'tombstone', 'x_normalization', 'created_at.x', 'published_at', 'revised_at', 'updated_at.x', 'filename', 'filetype', 's3_uri', 'user_submitted', 'created_at.y', 'updated_at.y', 'cell_type_harmonised', 'confidence_class', 'cell_annotation_azimuth_l2', 'cell_annotation_blueprint_singler', 'n_cell_type_in_tissue', 'n_tissue_in_cell_type'
        layers: 'cpm'



We can access the metadata using normal anndata conventions:


```python
anndata.obs
```




                            .cell                      sample_id_db  \
    0     ACAGCCGGTCCGTTAA_F02526  33cdeb84ae1462d723c19af1bea2a366   
    1     GGGAATGAGCCCAGCT_F02526  33cdeb84ae1462d723c19af1bea2a366   
    2     TCTTCGGAGTAGCGGT_F02526  33cdeb84ae1462d723c19af1bea2a366   
    3     CCTTACGAGAGCTGCA_F02526  33cdeb84ae1462d723c19af1bea2a366   
    4     ATCTACTCAATGGAAT_F02526  33cdeb84ae1462d723c19af1bea2a366   
    ...                       ...                               ...   
    1566  TACTTACGTAATAGCA_F02526  33cdeb84ae1462d723c19af1bea2a366   
    1567    AGATAGAGTGCCTTCT_SC84  21ef23ac07391c64cadc78e16511effa   
    1568    CGCGGTATCCGCGCAA_SC24  9dfbd16390b119392af9406561cb664f   
    1569    TACAACGTCAGCATTG_SC84  21ef23ac07391c64cadc78e16511effa   
    1570  CATTCGCTCAATACCG_F02526  33cdeb84ae1462d723c19af1bea2a366   
    
                                   .sample  \
    0     4fc10a6b85e5fa688b253db4e0db8ba0   
    1     4fc10a6b85e5fa688b253db4e0db8ba0   
    2     4fc10a6b85e5fa688b253db4e0db8ba0   
    3     4fc10a6b85e5fa688b253db4e0db8ba0   
    4     4fc10a6b85e5fa688b253db4e0db8ba0   
    ...                                ...   
    1566  4fc10a6b85e5fa688b253db4e0db8ba0   
    1567  13f5331436ecaeaeffada423c8dbd1ef   
    1568  055e5172053464e8efc5de1b5b3a7646   
    1569  13f5331436ecaeaeffada423c8dbd1ef   
    1570  4fc10a6b85e5fa688b253db4e0db8ba0   
    
                                               .sample_name      assay  \
    0     VUHD92___lung parenchyma___55-year-old human s...  10x 5' v1   
    1     VUHD92___lung parenchyma___55-year-old human s...  10x 5' v1   
    2     VUHD92___lung parenchyma___55-year-old human s...  10x 5' v1   
    3     VUHD92___lung parenchyma___55-year-old human s...  10x 5' v1   
    4     VUHD92___lung parenchyma___55-year-old human s...  10x 5' v1   
    ...                                                 ...        ...   
    1566  VUHD92___lung parenchyma___55-year-old human s...  10x 5' v1   
    1567  NU_CZI01___lung parenchyma___52-year-old human...  10x 3' v3   
    1568  Donor_06___lung parenchyma___22-year-old human...  10x 3' v2   
    1569  NU_CZI01___lung parenchyma___52-year-old human...  10x 3' v3   
    1570  VUHD92___lung parenchyma___55-year-old human s...  10x 5' v1   
    
         assay_ontology_term_id                        file_id_db  \
    0               EFO:0011025  bc380dae8b14313a870973697842878b   
    1               EFO:0011025  bc380dae8b14313a870973697842878b   
    2               EFO:0011025  bc380dae8b14313a870973697842878b   
    3               EFO:0011025  bc380dae8b14313a870973697842878b   
    4               EFO:0011025  bc380dae8b14313a870973697842878b   
    ...                     ...                               ...   
    1566            EFO:0011025  bc380dae8b14313a870973697842878b   
    1567            EFO:0009922  bc380dae8b14313a870973697842878b   
    1568            EFO:0009899  bc380dae8b14313a870973697842878b   
    1569            EFO:0009922  bc380dae8b14313a870973697842878b   
    1570            EFO:0011025  bc380dae8b14313a870973697842878b   
    
                                cell_type cell_type_ontology_term_id  \
    0     CD4-positive, alpha-beta T cell                 CL:0000624   
    1     CD4-positive, alpha-beta T cell                 CL:0000624   
    2     CD4-positive, alpha-beta T cell                 CL:0000624   
    3     CD4-positive, alpha-beta T cell                 CL:0000624   
    4     CD4-positive, alpha-beta T cell                 CL:0000624   
    ...                               ...                        ...   
    1566  CD4-positive, alpha-beta T cell                 CL:0000624   
    1567  CD4-positive, alpha-beta T cell                 CL:0000624   
    1568  CD4-positive, alpha-beta T cell                 CL:0000624   
    1569  CD4-positive, alpha-beta T cell                 CL:0000624   
    1570  CD4-positive, alpha-beta T cell                 CL:0000624   
    
                development_stage  ...  \
    0     55-year-old human stage  ...   
    1     55-year-old human stage  ...   
    2     55-year-old human stage  ...   
    3     55-year-old human stage  ...   
    4     55-year-old human stage  ...   
    ...                       ...  ...   
    1566  55-year-old human stage  ...   
    1567  52-year-old human stage  ...   
    1568  22-year-old human stage  ...   
    1569  52-year-old human stage  ...   
    1570  55-year-old human stage  ...   
    
                                                     s3_uri user_submitted  \
    0     s3://corpora-data-prod/13825e35-ea32-4104-a0b7...              1   
    1     s3://corpora-data-prod/13825e35-ea32-4104-a0b7...              1   
    2     s3://corpora-data-prod/13825e35-ea32-4104-a0b7...              1   
    3     s3://corpora-data-prod/13825e35-ea32-4104-a0b7...              1   
    4     s3://corpora-data-prod/13825e35-ea32-4104-a0b7...              1   
    ...                                                 ...            ...   
    1566  s3://corpora-data-prod/13825e35-ea32-4104-a0b7...              1   
    1567  s3://corpora-data-prod/13825e35-ea32-4104-a0b7...              1   
    1568  s3://corpora-data-prod/13825e35-ea32-4104-a0b7...              1   
    1569  s3://corpora-data-prod/13825e35-ea32-4104-a0b7...              1   
    1570  s3://corpora-data-prod/13825e35-ea32-4104-a0b7...              1   
    
         created_at.y updated_at.y cell_type_harmonised confidence_class  \
    0         19226.0      19227.0              cd4 tem              1.0   
    1         19226.0      19227.0              cd4 tcm              4.0   
    2         19226.0      19227.0              cd4 tcm              4.0   
    3         19226.0      19227.0              cd4 tcm              4.0   
    4         19226.0      19227.0              cd4 tcm              4.0   
    ...           ...          ...                  ...              ...   
    1566      19226.0      19227.0              cd4 tcm              4.0   
    1567      19226.0      19227.0              cd4 tcm              4.0   
    1568      19226.0      19227.0              cd4 tcm              4.0   
    1569      19226.0      19227.0              cd4 tcm              3.0   
    1570      19226.0      19227.0              cd4 tem              1.0   
    
         cell_annotation_azimuth_l2 cell_annotation_blueprint_singler  \
    0                          mait                           cd4 tem   
    1                       cd4 tcm                           cd4 tem   
    2                       cd4 tcm                           cd4 tem   
    3                       cd4 tcm                           cd4 tem   
    4                       cd4 tcm                           cd4 tem   
    ...                         ...                               ...   
    1566                    cd4 tcm                           cd4 tem   
    1567                    cd4 tcm                           cd4 tem   
    1568                    cd4 tcm                           cd4 tem   
    1569                    cd4 tcm                             tregs   
    1570                    cd4 tem                           cd4 tem   
    
         n_cell_type_in_tissue n_tissue_in_cell_type  
    0                     28.0                  31.0  
    1                     28.0                  32.0  
    2                     28.0                  32.0  
    3                     28.0                  32.0  
    4                     28.0                  32.0  
    ...                    ...                   ...  
    1566                  28.0                  32.0  
    1567                  28.0                  32.0  
    1568                  28.0                  32.0  
    1569                  28.0                  32.0  
    1570                  28.0                  31.0  
    
    [1571 rows x 56 columns]



## Finishing Up

When you are finished, you should close the connection:


```python
conn.close()
```
