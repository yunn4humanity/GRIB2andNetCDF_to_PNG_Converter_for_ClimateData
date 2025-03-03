# Introduction

GRIB2 and NetCDF file format is often used for Climate Data Format. To train climate forecasting AI model with these data format, it should be converted to image data like PNG.
This repository is for converting them to PNG file format. All code is based on Python. Hope these codes are helpful to train climate forecasting AI model easier.

# Included
- grib2 to png, netcdf to png
- file viewer of grib2, netcdf
- statistics viewer of grib2, netcdf
- comparing png files from grib2 and netcdf with original png
- sample files of grib2, netcdf, and png 
- MRMS dataset downloader (Openned American Climate Dataset)

# Environment Setup Guide

This project was developed in a Python 3.9.21 environment, and all required packages are specified in the `requirements.txt` file.

## Installation Methods

### 1. Clone the Repository

```bash
git clone https://github.com/yunn4humanity/GRIB2andNetCDF_to_PNG_Converter_for_ClimateData.git
cd GRIB2andNetCDF_to_PNG_Converter_for_ClimateData
```

### 2. Conda Environment Setup (Recommended)

Conda is recommended as it makes it easier to install scientific computing and geospatial packages (GDAL, NetCDF4, etc.).

```bash
# Create a new environment based on Python 3.9.21
conda create -n nowcast python=3.9.21

# Activate the environment
conda activate nowcast

# Install packages from the requirements.txt file
conda install --file requirements.txt -c conda-forge
```

If the above command doesn't complete the installation, try the following:

```bash
# Install key packages individually
conda install -c conda-forge numpy pandas xarray matplotlib netcdf4 cfgrib scipy pygrib
```

### 3. Using Pip (Alternative)

```bash
# Create a Python 3.9 virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

## Notes

- This project has been tested with Python 3.9.21; compatibility issues may arise with other versions.
- Geospatial packages (GDAL, NetCDF4) can be difficult to install with pip, so Conda is recommended.
- Initial commit includes Korean comments. If you are familiar with Korean, you can use it.
