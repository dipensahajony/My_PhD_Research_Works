# NOAA water-level download notebook

A cleaned version of the supplied NOAA download notebook, organized as a public-data example.

## Setup and use

From the repository root, in an activated Python environment:

```bash
python -m pip install -r compound_flood/noaa_water_levels/requirements.txt
python -m pip install notebook
python -m notebook compound_flood/noaa_water_levels/download_noaa_water_levels.ipynb
```

Select that environment's kernel. Run the notebook cells in order. Edit the station, inclusive start/end dates (`YYYYMMDD`), and datum in the configuration cell.

The notebook writes a CSV under `data/` relative to its working directory. Filenames include station, date range, datum, units, and time zone. Existing files cause an error rather than being overwritten; choose a new destination to download again.

## Behavior and scientific interpretation

- Downloads six-minute `water_level` observations in chunks of at most 28 days.
- Uses metric water levels (meters) and GMT timestamps.
- MSL means Mean Sea Level; MLLW means Mean Lower Low Water. Confirm the chosen datum is supported by the station.
- Retains NOAA columns, quality flags, and blank values without interpolation.
- Sorts by timestamp, removes identical duplicate records, and rejects conflicting duplicates.
- Stops on network/HTTP failures, error responses, malformed CSV, empty chunks, or unexpected timestamps. No CSV is saved when retrieval fails.
- Does not guarantee a gap-free series or acceptable observation quality; assess both before research use.
- Uses connection/read timeouts. Failed requests are not automatically retried; rerun after resolving the error.

No downloaded data, saved notebook outputs, credentials, or machine-specific paths are committed. The original local notebook is unchanged.

## Validation

Run offline regression checks from the repository root:

```bash
python -m unittest discover -s compound_flood/noaa_water_levels -p "test_*.py" -v
```

The checks use synthetic API responses and do not download data. A live NOAA request is a separate smoke check, not a reproducibility guarantee. Dependency versions are intentionally unpinned until a research environment is selected and recorded.

## Sources

- [NOAA CO-OPS API documentation](https://api.tidesandcurrents.noaa.gov/api/prod/)
- [NOAA station directory](https://tidesandcurrents.noaa.gov/stations.html)
