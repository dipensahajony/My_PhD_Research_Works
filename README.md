# Research notebook archive

Unmodified copies of 148 supplied Jupyter notebooks, organized by subject. Original filenames, cell content, equations, code, outputs, metadata, and embedded paths are preserved byte-for-byte. No notebooks were executed or refactored during organization.

## Organization

- `cfd_reef/notebooks/`: 2 notebooks.
- `climate_and_sea_level/notebooks/`: 3 notebooks.
- `compound_flood/drivers_and_sensitivity/notebooks/`: 15 notebooks.
- `compound_flood/exposure/notebooks/`: 11 notebooks.
- `compound_flood/inundation_and_comparison/notebooks/`: 22 notebooks.
- `coursework/undated/coastal_engineering/notebooks/`: 5 notebooks.
- `coursework/undated/machine_learning/notebooks/`: 1 notebooks.
- `data_acquisition/notebooks/`: 6 notebooks.
- `gis_processing/mesh_and_bathymetry/notebooks/`: 12 notebooks.
- `gis_processing/rasters_and_vectors/notebooks/`: 10 notebooks.
- `hydrology_and_tides/notebooks/`: 4 notebooks.
- `mikeio_tools/forcing/notebooks/`: 2 notebooks.
- `mikeio_tools/processing_and_plots/notebooks/`: 5 notebooks.
- `model_validation/notebooks/`: 4 notebooks.
- `needs_review/notebooks/`: 16 notebooks.
- `salinity/notebooks/`: 7 notebooks.
- `visualization/notebooks/`: 1 notebooks.
- `wave_reef/notebooks/`: 22 notebooks.

`needs_review` retains untitled notebooks without guessing their final identity. Coursework is under `coursework/undated` because the supplied collection does not establish its term. The previously mentioned Fall 2026 project notebook was not present in this supplied collection; no notebook is assigned to that project without evidence.

## File inventory and review

See [NOTEBOOK_INVENTORY.csv](NOTEBOOK_INVENTORY.csv) for every original filename, repository destination, byte count, SHA-256 checksum, and review note. See [REVIEW_NOTES.md](REVIEW_NOTES.md) for duplicates and ambiguous notebooks.

## Preservation and use

- Only supplied `.ipynb` files and archive documentation are included. No separate datasets, model files, generated figures, or reports were supplied or added.
- Existing outputs embedded inside notebooks are preserved, including plots, tables, and any saved errors. These are historical results, not verification from this import.
- Many notebooks contain machine-specific absolute paths. These remain unchanged to preserve the originals; the documentation does not reproduce their values. Running the archive requires the referenced data and appropriate environment and may require a separately edited working copy.
- Libraries vary by notebook (including MIKE IO, NumPy, pandas, plotting, GIS, and machine learning packages). No single tested environment is asserted.
- Source, metadata, and textual outputs were checked for common credential patterns. Only placeholder credential values were identified. This is a pattern-based review, not a guarantee that every possible sensitive value has been detected.
- Originals in the supplied source folder were read only. Copies were checked using SHA-256 before inclusion. No duplicate was deleted or consolidated.
