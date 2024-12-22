# Change Log

## [0.3.1] - 2024-12-22

### Fixed

- `__version__` was not correctly set in the package

## [0.3.0] - 2024-12-21

### Added

- Snakemake process output is now kept internally, and it's return code is checked for errors
- Automatically deleting/re-using existing Snakemake output files is now possible, based on previous config files

### Changed

- Moved from `poetry` to `uv`
- Moved to `snakemake` (and versions `>= 8`)
- Updated dependencies
- Moved from `black` to `ruff`

### Fixed

- Passed parameters are now correctly passed to the Snakemake workflow

## [0.2.0] - 2023-11-15

### Added

- `.config("someproperty")`` allows extracting the value of "someproperty" from the used Snakemake config

## [0.1.1] - 2023-11-15

First working and tagged version; base for the incremental change log.
