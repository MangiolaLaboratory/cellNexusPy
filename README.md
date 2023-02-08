# Curated Atlas Query (Python)

## Importing the package


```python
import hcaquery
```

You will probably need pandas and sqlalchemy too, to query and organise the metadata


```python
import pandas as pd
import sqlalchemy
```

## Getting the metadata
The `get_metadata()` function returns an SQLAlchemy engine and `MetaData` object which can be used to form queries and execute them.


```python
eng, mdtab = hcaquery.get_metadata()
```

    Downloading https://swift.rc.nectar.org.au/v1/AUTH_06d6e008e3e642da99d806ba3ea629c5/metadata-sqlite/metadata.tar.xz to /vast/scratch/users/yang.e/tmp/hca_harmonised/metadata.tar.xz
    Download progress: 100.0%
    Extracting database...


### Querying the metadata
SQLAlchemy core syntax can be used to form and execute the query


```python
q = sqlalchemy.select('*').where( \
                                 mdtab.c.ethnicity == "African", \
                                 mdtab.c.assay.like('%10x%'), \
                                 mdtab.c.tissue == "lung parenchyma", \
                                 mdtab.c.cell_type.like('%CD4%') \
                                )
```


```python
with eng.connect() as conn:
    mddf = pd.DataFrame(conn.execute(q))
    
eng.dispose()
mddf
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



### Exploring the HCA contents


```python
eng, mdtab = hcaquery.get_metadata()

from sqlalchemy import func

q = sqlalchemy.select(mdtab.c.tissue, mdtab.c.file_id, func.count()).distinct().group_by(mdtab.c.tissue)
with eng.connect() as conn:
    mddf = pd.DataFrame(conn.execute(q))
    
eng.dispose()
mddf
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
      <th>count_1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>adipose tissue</td>
      <td>343f46f2-7cdd-4da8-bc7f-50a18b2c0e8e</td>
      <td>22114</td>
    </tr>
    <tr>
      <th>1</th>
      <td>adrenal gland</td>
      <td>16217568-ec4e-4391-891d-1e14c64da474</td>
      <td>547539</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ampulla of uterine tube</td>
      <td>3044b5dd-a499-456e-86d9-94769bc3b63e</td>
      <td>43247</td>
    </tr>
    <tr>
      <th>3</th>
      <td>anterior cingulate cortex</td>
      <td>a91f075b-52d5-4aa3-8ecc-86c4763a49b3</td>
      <td>7417</td>
    </tr>
    <tr>
      <th>4</th>
      <td>anterior part of tongue</td>
      <td>343f46f2-7cdd-4da8-bc7f-50a18b2c0e8e</td>
      <td>10734</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>160</th>
      <td>vasculature</td>
      <td>343f46f2-7cdd-4da8-bc7f-50a18b2c0e8e</td>
      <td>5572</td>
    </tr>
    <tr>
      <th>161</th>
      <td>vault of skull</td>
      <td>e40591e7-0e5a-4bef-9b60-7015abe5b17f</td>
      <td>5129</td>
    </tr>
    <tr>
      <th>162</th>
      <td>venous blood</td>
      <td>a84321f2-5b06-4274-8f96-e1876340600e</td>
      <td>17625</td>
    </tr>
    <tr>
      <th>163</th>
      <td>vermiform appendix</td>
      <td>e40591e7-0e5a-4bef-9b60-7015abe5b17f</td>
      <td>4486</td>
    </tr>
    <tr>
      <th>164</th>
      <td>zone of skin</td>
      <td>c48402e4-e7db-4c82-a9e9-51e285e5165c</td>
      <td>15457</td>
    </tr>
  </tbody>
</table>
<p>165 rows × 3 columns</p>
</div>



### Querying using raw SQL
For those who prefer writing raw SQL over SQLalchemy, you can use pandas `read_sql_query()` instead of SQLAlchemy.


```python
eng, mdtab = hcaquery.get_metadata()

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



## Extracting Counts

Query raw counts


```python
res = hcaquery.get_SingleCellExperiment(mddf, assays = ['counts'], repository='file:///vast/projects/human_cell_atlas_py/anndata')
res
```

    Downloading file:///vast/projects/human_cell_atlas_py/anndata/original/bc380dae8b14313a870973697842878b.h5ad to /vast/scratch/users/yang.e/tmp/hca_harmonised/original/bc380dae8b14313a870973697842878b.h5ad
    Reading sample files: 100%|█████████████████| 1/1 [00:00<00:00, 13315.25files/s]
    Concatenating files...





    AnnData object with n_obs × n_vars = 21285 × 60661



Query counts scaled per million. This is helpful if just few genes are of interest


```python
res = hcaquery.get_SingleCellExperiment(mddf, assays = ['cpm'], repository='file:///vast/projects/human_cell_atlas_py/anndata')
res
```

    Downloading file:///vast/projects/human_cell_atlas_py/anndata/cpm/bc380dae8b14313a870973697842878b.h5ad to /vast/scratch/users/yang.e/tmp/hca_harmonised/cpm/bc380dae8b14313a870973697842878b.h5ad
    Reading sample files: 100%|█████████████████| 1/1 [00:00<00:00, 11155.06files/s]
    Concatenating files...





    AnnData object with n_obs × n_vars = 21285 × 60661




```python
res=hcaquery.get_SingleCellExperiment(mddf, features = ['PUM1'], repository='file:///vast/projects/human_cell_atlas_py/anndata')
res
```

    Reading sample files: 100%|██████████████████| 2/2 [00:00<00:00, 9927.35files/s]
    Concatenating files...





    AnnData object with n_obs × n_vars = 42570 × 1




```python
res.obs
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>P2_2_TGTTCCGAGGCCCGTT-0</th>
    </tr>
    <tr>
      <th>CTAATGGAGTGGGATC_HD67-0</th>
    </tr>
    <tr>
      <th>GCTCCTAAGTGGACGT-1-HCATisStab7659969-0</th>
    </tr>
    <tr>
      <th>CATGTACAGTGGGAT_GRO-09_biopsy-0</th>
    </tr>
    <tr>
      <th>ACAGCCGGTCCGTTAA_F02526-0</th>
    </tr>
    <tr>
      <th>...</th>
    </tr>
    <tr>
      <th>CGGACACAGTGGAGTC_GRO-03_biopsy-1</th>
    </tr>
    <tr>
      <th>D344_Brus_Dis1_GATGCTAAGTACGCCC-1-14-1</th>
    </tr>
    <tr>
      <th>CTGATAGCAAATACAG-SC45-1</th>
    </tr>
    <tr>
      <th>P2_3_TAAGTGCGTCCAACTA-1</th>
    </tr>
    <tr>
      <th>AGCGGCACCCGATA-SC31-1</th>
    </tr>
  </tbody>
</table>
<p>42570 rows × 0 columns</p>
</div>




```python

```
