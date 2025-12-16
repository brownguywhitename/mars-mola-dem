# Global Mars MOLA DEM (Preliminary Work)

This repository contains scripts and preliminary results for constructing a
global Mars Digital Elevation Model (DEM) from Mars Orbiter Laser Altimeter (MOLA)
Mission Experiment Gridded Data Record (MEGDR) products.

## Scientific Motivation
Mars lacks a global intrinsic magnetic field, making local topography an
important control on atmospheric column depth and surface radiation exposure.
This DEM provides the topographic reference frame for subsequent analysis of
crustal magnetic field topology and energetic particle access using MAVEN data.

## Data Sources
- MOLA MEGDR 463 m global tiles:
  - megt90n000gb
  - megt90n180gb
  - megt00n000gb
  - megt00n180gb
NASA PDS Geosciences Node

## Method
- PDS label ingestion to preserve scaling and geolocation
- Application of standard half-pixel offset correction
- Global mosaicking using GDAL
- Conversion to physical elevation units (meters relative to the Mars areoid)

## Output
The script produces:
- A virtual global mosaic (`mars_mola_global.vrt`)
- A materialised GeoTIFF DEM (`mars_mola_global_463m.tif`)

The full GeoTIFF is not included due to size; users can reproduce it locally.

## Requirements
See `requirements.txt`.

## Author
Andrew Allan
