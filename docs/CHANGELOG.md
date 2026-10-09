# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.6.0] - 2026-10-09

### Added

- "get_census_metadata" function to retrieve cell metadata from CZ CELLxGENE Census (default version "2024-07-01"), to be joined to the metadata via "dataset_id" and "observation_joinid"
- "get_specific_annotation_columns" function to identify annotation columns determined by key column(s)
- "hca_2024" and "hca_2025" aliases in "get_metadata_url"
- "nfeature_col" and "min_features" parameters in "keep_quality_cells" (cells with fewer than 5000 features are removed by default)
- Warnings when experiments are dropped for missing requested features, or when genes do not completely overlap across experiments
- "cellxgene_census" dependency

### Changed

- New parquet file version: 2.4.0
- Parameter name: From "parquet_url" to "cloud_metadata" in "get_metadata" and "get_cell_communication_strength"
- "get_metadata" downloads "hca_2024" by default
- "get_pseudobulk" applies "keep_quality_cells" automatically, as pseudobulk counts are computed from quality-controlled cells only
- Pseudobulk metadata columns are computed once on the full query with "get_specific_annotation_columns", so all files share the same columns
- Pseudobulk observation names are kept as "sample_id___cell_type_unified_ensemble", without suffixes
- When "features" are provided, experiments missing any of them are dropped and genes follow the requested order; otherwise, genes are intersected across experiments
- "get_anndata" and "get_pseudobulk" return an AnnData object instead of a view
- Examples updated in "demo.ipynb"

### Deprecated

### Removed

- "join_census_table" function (replaced by "get_census_metadata")
- "METADATA_URL", "SAMPLE_DATABASE_URL" and "CENSUS_SAMPLE_METADATA_URL" constants

### Fixed

- Pseudobulk results now match cellNexus R ("get_pseudobulk")
- Additional assays are aligned to the same genes as the first assay

### Security

## [0.5.0] - 2026-06-09

### Added

### Changed

- New parquet file version: 2.3.0

### Deprecated

### Removed

### Fixed

### Security

## [0.4.0] - 2026-05-06

### Added

- sct normalization as additional option for parameter "assays"
- Adding "get_anndata" and "get_pseudobulk" to "DuckDBPyRelation" to make one-line-code feasible
- "get_metadata_url" function added
- "get_cell_communication_strength" function added
- "join_census_table" function added
- "keep_quality_cells" function added
- Examples of new function in "demo.ipynb"

### Changed

- New parquet file version: 2.2.1
- License: From GPL-3 to Modified MIT (based on GPT-2 License)
- Function name: From get_anndata to _anndata_constructor
- Function name: From get_single_cell_experiment to get_anndata
- Examples for get_anndata and get_pseudobulk in demo.ipynb
- Error checking in _anndata_constructor function

### Deprecated

### Removed

### Fixed

### Security

## [0.3.0] - 2026-03-26

### Added

### Changed

- parquet version updated
- get_anndata splitted into get_single_cell_experiment and get_pseudobulk
- Input data for anndata retreivers accepts also pd.DataFrame

### Deprecated

### Removed

- get_metacell function

### Fixed

- nbconvert and notebook versions requirements

### Security

## [0.2.0] - 2026-01-30

### Added

- Detailed metadata description (https://github.com/MangiolaLaboratory/cellNexus)

### Changed

- New parquet version (1.3.0)
- demo based on sample_parquet file (1.3.0)

### Deprecated

### Removed

- Old folders from curated_atlas_query_py

### Fixed

### Security

## [0.1.0] - 2025-10-24

### Added

- Added First version of cellNexusPy package ([#1](https://github.com/MangiolaLaboratory/cellNexusPy/pull/1))

### Changed
### Deprecated
### Removed
### Fixed
### Security
