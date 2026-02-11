# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-11

### Added
- Added `metadata()` function to get metadata for all indicators (signatures, parameters, output series with types, descriptions)
- Added `list()` function to get formatted list of all indicators in human-readable format
- Added slicing support for `DataSeries`, `Quotes`, and `IndicatorResult` (returns views)

### Fixed
- Fixed incorrect handling of CCXT format data in `Quotes` constructor

### Changed
- Renamed internal module `core.py` to `data_series.py`

## [1.0.12] - 2026-02-09
### First version