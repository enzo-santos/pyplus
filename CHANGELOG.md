# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[PEP 440 -- Version Identification and Dependency Specification](https://www.python.org/dev/peps/pep-0440/).

## [Unreleased]

## [0.2.1] - 2023-11-12
### Added
- `encoding` parameter to `pyplus.io.i.csv_*` functions
- Tests for reading CSV files

### Fixed
- `delimiter` parameter of `pyplus.io.i.csv_models` now works

## [0.2.0] - 2023-11-11
### Added
- Model support for `pyplus.io.i` as `csv_models`, `xls_models` and `xlsx_models`
- `sheet_index` parameter to `pyplus.io.i.xls`
- `read_only` parameter to `pyplus.io.i.xlsx`

### Changed
- `pyplus.io.i` functions are now suffixed with `_lines`
- `header` parameter of `pyplus.io.i` functions is now `skiprows`
- `fpath` parameter of `pyplus.io.o.url` now accepts any path-like object

### Fixed
- Improved typing

## [0.1.0] - 2023-08-04
### Added
- `pyplus.io.i.csv`
- `pyplus.io.i.xls`
- `pyplus.io.i.xlsx`
- `pyplus.io.o.csv`
- `pyplus.io.o.url`
