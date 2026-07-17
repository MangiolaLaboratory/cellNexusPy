# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.5.1] - 2026-07-17

### Added

- `get_specific_annotation_columns()` and `keep_specific_annotation_columns()` to identify and keep columns functionally determined by selected key column(s). Works on local data frames and lazy DuckDB tables from `get_metadata()`.
- `get_pseudobulk()` now retains metadata columns that are constant within each `sample_id` × `cell_type_unified_ensemble` combination, including user-added annotations, when building `obs`. Cell-level columns are dropped.

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
