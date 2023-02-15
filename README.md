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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>tissue</th>
      <th>file_id</th>
      <th>n</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>cortex of kidney</td>
      <td>2977b3fa-e4d6-4929-8540-ae12d33a3c53</td>
      <td>25166</td>
    </tr>
    <tr>
      <th>1</th>
      <td>entorhinal cortex</td>
      <td>29d5d028-6f90-4943-91f7-fa3f93731de8</td>
      <td>5500</td>
    </tr>
    <tr>
      <th>2</th>
      <td>middle temporal gyrus</td>
      <td>2a689fda-d335-4ac0-81b1-a356fdf939db</td>
      <td>18402</td>
    </tr>
    <tr>
      <th>3</th>
      <td>respiratory airway</td>
      <td>2c2d5bea-8be7-4227-8a56-f2a85d57fa56</td>
      <td>4594</td>
    </tr>
    <tr>
      <th>4</th>
      <td>thymus</td>
      <td>2ec94470-8171-4825-8346-34d77383438b</td>
      <td>18524</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>886</th>
      <td>cortex of kidney</td>
      <td>f2ccb395-6800-455a-9655-476cc54ab864</td>
      <td>27036</td>
    </tr>
    <tr>
      <th>887</th>
      <td>lung</td>
      <td>f4065ffa-c2d6-45bf-b596-5a69e36d8fcd</td>
      <td>46500</td>
    </tr>
    <tr>
      <th>888</th>
      <td>heart left ventricle</td>
      <td>f445a8b3-b17a-4cc6-b94e-ff56a180dadc</td>
      <td>2551</td>
    </tr>
    <tr>
      <th>889</th>
      <td>lung epithelium</td>
      <td>f498030e-246c-4376-87e3-90b28c7efb00</td>
      <td>19361</td>
    </tr>
    <tr>
      <th>890</th>
      <td>mesenteric lymph node</td>
      <td>92f8482a-c31d-4482-b84a-7eafac0e7904</td>
      <td>17148</td>
    </tr>
  </tbody>
</table>
<p>891 rows × 3 columns</p>
</div>




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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>.cell</th>
      <th>sample_id_db</th>
      <th>.sample</th>
      <th>.sample_name</th>
      <th>assay</th>
      <th>assay_ontology_term_id</th>
      <th>file_id_db</th>
      <th>cell_type</th>
      <th>cell_type_ontology_term_id</th>
      <th>development_stage</th>
      <th>...</th>
      <th>s3_uri</th>
      <th>user_submitted</th>
      <th>created_at.y</th>
      <th>updated_at.y</th>
      <th>cell_type_harmonised</th>
      <th>confidence_class</th>
      <th>cell_annotation_azimuth_l2</th>
      <th>cell_annotation_blueprint_singler</th>
      <th>n_cell_type_in_tissue</th>
      <th>n_tissue_in_cell_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ACAGCCGGTCCGTTAA_F02526</td>
      <td>33cdeb84ae1462d723c19af1bea2a366</td>
      <td>4fc10a6b85e5fa688b253db4e0db8ba0</td>
      <td>VUHD92___lung parenchyma___55-year-old human s...</td>
      <td>10x 5' v1</td>
      <td>EFO:0011025</td>
      <td>bc380dae8b14313a870973697842878b</td>
      <td>CD4-positive, alpha-beta T cell</td>
      <td>CL:0000624</td>
      <td>55-year-old human stage</td>
      <td>...</td>
      <td>s3://corpora-data-prod/13825e35-ea32-4104-a0b7...</td>
      <td>1</td>
      <td>19226.0</td>
      <td>19227.0</td>
      <td>cd4 tem</td>
      <td>1.0</td>
      <td>mait</td>
      <td>cd4 tem</td>
      <td>28.0</td>
      <td>31.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>GGGAATGAGCCCAGCT_F02526</td>
      <td>33cdeb84ae1462d723c19af1bea2a366</td>
      <td>4fc10a6b85e5fa688b253db4e0db8ba0</td>
      <td>VUHD92___lung parenchyma___55-year-old human s...</td>
      <td>10x 5' v1</td>
      <td>EFO:0011025</td>
      <td>bc380dae8b14313a870973697842878b</td>
      <td>CD4-positive, alpha-beta T cell</td>
      <td>CL:0000624</td>
      <td>55-year-old human stage</td>
      <td>...</td>
      <td>s3://corpora-data-prod/13825e35-ea32-4104-a0b7...</td>
      <td>1</td>
      <td>19226.0</td>
      <td>19227.0</td>
      <td>cd4 tcm</td>
      <td>4.0</td>
      <td>cd4 tcm</td>
      <td>cd4 tem</td>
      <td>28.0</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>TCTTCGGAGTAGCGGT_F02526</td>
      <td>33cdeb84ae1462d723c19af1bea2a366</td>
      <td>4fc10a6b85e5fa688b253db4e0db8ba0</td>
      <td>VUHD92___lung parenchyma___55-year-old human s...</td>
      <td>10x 5' v1</td>
      <td>EFO:0011025</td>
      <td>bc380dae8b14313a870973697842878b</td>
      <td>CD4-positive, alpha-beta T cell</td>
      <td>CL:0000624</td>
      <td>55-year-old human stage</td>
      <td>...</td>
      <td>s3://corpora-data-prod/13825e35-ea32-4104-a0b7...</td>
      <td>1</td>
      <td>19226.0</td>
      <td>19227.0</td>
      <td>cd4 tcm</td>
      <td>4.0</td>
      <td>cd4 tcm</td>
      <td>cd4 tem</td>
      <td>28.0</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>CCTTACGAGAGCTGCA_F02526</td>
      <td>33cdeb84ae1462d723c19af1bea2a366</td>
      <td>4fc10a6b85e5fa688b253db4e0db8ba0</td>
      <td>VUHD92___lung parenchyma___55-year-old human s...</td>
      <td>10x 5' v1</td>
      <td>EFO:0011025</td>
      <td>bc380dae8b14313a870973697842878b</td>
      <td>CD4-positive, alpha-beta T cell</td>
      <td>CL:0000624</td>
      <td>55-year-old human stage</td>
      <td>...</td>
      <td>s3://corpora-data-prod/13825e35-ea32-4104-a0b7...</td>
      <td>1</td>
      <td>19226.0</td>
      <td>19227.0</td>
      <td>cd4 tcm</td>
      <td>4.0</td>
      <td>cd4 tcm</td>
      <td>cd4 tem</td>
      <td>28.0</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ATCTACTCAATGGAAT_F02526</td>
      <td>33cdeb84ae1462d723c19af1bea2a366</td>
      <td>4fc10a6b85e5fa688b253db4e0db8ba0</td>
      <td>VUHD92___lung parenchyma___55-year-old human s...</td>
      <td>10x 5' v1</td>
      <td>EFO:0011025</td>
      <td>bc380dae8b14313a870973697842878b</td>
      <td>CD4-positive, alpha-beta T cell</td>
      <td>CL:0000624</td>
      <td>55-year-old human stage</td>
      <td>...</td>
      <td>s3://corpora-data-prod/13825e35-ea32-4104-a0b7...</td>
      <td>1</td>
      <td>19226.0</td>
      <td>19227.0</td>
      <td>cd4 tcm</td>
      <td>4.0</td>
      <td>cd4 tcm</td>
      <td>cd4 tem</td>
      <td>28.0</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1566</th>
      <td>TACTTACGTAATAGCA_F02526</td>
      <td>33cdeb84ae1462d723c19af1bea2a366</td>
      <td>4fc10a6b85e5fa688b253db4e0db8ba0</td>
      <td>VUHD92___lung parenchyma___55-year-old human s...</td>
      <td>10x 5' v1</td>
      <td>EFO:0011025</td>
      <td>bc380dae8b14313a870973697842878b</td>
      <td>CD4-positive, alpha-beta T cell</td>
      <td>CL:0000624</td>
      <td>55-year-old human stage</td>
      <td>...</td>
      <td>s3://corpora-data-prod/13825e35-ea32-4104-a0b7...</td>
      <td>1</td>
      <td>19226.0</td>
      <td>19227.0</td>
      <td>cd4 tcm</td>
      <td>4.0</td>
      <td>cd4 tcm</td>
      <td>cd4 tem</td>
      <td>28.0</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th>1567</th>
      <td>AGATAGAGTGCCTTCT_SC84</td>
      <td>21ef23ac07391c64cadc78e16511effa</td>
      <td>13f5331436ecaeaeffada423c8dbd1ef</td>
      <td>NU_CZI01___lung parenchyma___52-year-old human...</td>
      <td>10x 3' v3</td>
      <td>EFO:0009922</td>
      <td>bc380dae8b14313a870973697842878b</td>
      <td>CD4-positive, alpha-beta T cell</td>
      <td>CL:0000624</td>
      <td>52-year-old human stage</td>
      <td>...</td>
      <td>s3://corpora-data-prod/13825e35-ea32-4104-a0b7...</td>
      <td>1</td>
      <td>19226.0</td>
      <td>19227.0</td>
      <td>cd4 tcm</td>
      <td>4.0</td>
      <td>cd4 tcm</td>
      <td>cd4 tem</td>
      <td>28.0</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th>1568</th>
      <td>CGCGGTATCCGCGCAA_SC24</td>
      <td>9dfbd16390b119392af9406561cb664f</td>
      <td>055e5172053464e8efc5de1b5b3a7646</td>
      <td>Donor_06___lung parenchyma___22-year-old human...</td>
      <td>10x 3' v2</td>
      <td>EFO:0009899</td>
      <td>bc380dae8b14313a870973697842878b</td>
      <td>CD4-positive, alpha-beta T cell</td>
      <td>CL:0000624</td>
      <td>22-year-old human stage</td>
      <td>...</td>
      <td>s3://corpora-data-prod/13825e35-ea32-4104-a0b7...</td>
      <td>1</td>
      <td>19226.0</td>
      <td>19227.0</td>
      <td>cd4 tcm</td>
      <td>4.0</td>
      <td>cd4 tcm</td>
      <td>cd4 tem</td>
      <td>28.0</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th>1569</th>
      <td>TACAACGTCAGCATTG_SC84</td>
      <td>21ef23ac07391c64cadc78e16511effa</td>
      <td>13f5331436ecaeaeffada423c8dbd1ef</td>
      <td>NU_CZI01___lung parenchyma___52-year-old human...</td>
      <td>10x 3' v3</td>
      <td>EFO:0009922</td>
      <td>bc380dae8b14313a870973697842878b</td>
      <td>CD4-positive, alpha-beta T cell</td>
      <td>CL:0000624</td>
      <td>52-year-old human stage</td>
      <td>...</td>
      <td>s3://corpora-data-prod/13825e35-ea32-4104-a0b7...</td>
      <td>1</td>
      <td>19226.0</td>
      <td>19227.0</td>
      <td>cd4 tcm</td>
      <td>3.0</td>
      <td>cd4 tcm</td>
      <td>tregs</td>
      <td>28.0</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th>1570</th>
      <td>CATTCGCTCAATACCG_F02526</td>
      <td>33cdeb84ae1462d723c19af1bea2a366</td>
      <td>4fc10a6b85e5fa688b253db4e0db8ba0</td>
      <td>VUHD92___lung parenchyma___55-year-old human s...</td>
      <td>10x 5' v1</td>
      <td>EFO:0011025</td>
      <td>bc380dae8b14313a870973697842878b</td>
      <td>CD4-positive, alpha-beta T cell</td>
      <td>CL:0000624</td>
      <td>55-year-old human stage</td>
      <td>...</td>
      <td>s3://corpora-data-prod/13825e35-ea32-4104-a0b7...</td>
      <td>1</td>
      <td>19226.0</td>
      <td>19227.0</td>
      <td>cd4 tem</td>
      <td>1.0</td>
      <td>cd4 tem</td>
      <td>cd4 tem</td>
      <td>28.0</td>
      <td>31.0</td>
    </tr>
  </tbody>
</table>
<p>1571 rows × 56 columns</p>
</div>



## Finishing Up

When you are finished, you should close the connection:


```python
conn.close()
```
