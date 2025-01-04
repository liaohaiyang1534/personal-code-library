# Passive Seismic Imaging: Three-Station C3 Method

This repository provides scripts for calculating surface wave dispersion spectra using the Three-Station C3 method, developed by Dr. Zhenghong Song (https://gitee.com/gemini_lh/surfacewave-c3/tree/master/surfacewaveC3). The main focus of the repository is on performing rolling array processing for seismic data analysis in our research group. Dispersion spectrum calculations are based on the C3 method, with ongoing improvements for higher quality cross-correlation functions (CCFs), including the development of the FJ method.

## Repository Structure

### `1_surface_wave_dispersion_spectrum_calculation`
This module contains scripts for calculating surface wave dispersion spectra from passive seismic data, including rolling array functionality.

- **`1_dispersion_calculation_array_run.py`**  
  Implements the dispersion spectrum calculation, including preprocessing, cross-correlation, and spectrum computation.  
  **Note**: This script needs modification to incorporate the FJ method for computing the dispersion spectrum to improve CCFs. The random transform method is currently used, and the FJ method is still under development.

- **`2_dispersion_calculation_array_run_array_rolling.py`**  
  Automates rolling array processing for dispersion spectrum calculations by iteratively moving the array over the data set. Supports configurable array length, spacing, and interval.

- **`3_dispersion_calculation_array_run_array_and_time_rolling.py`**  
  Extends the rolling array functionality to incorporate time-based rolling, processing seismic data across multiple time intervals and spatial positions.

### `2_pick_curve`
This module provides tools for visualizing and refining dispersion curves extracted from seismic data.

- **`dispersion_file_curve_revise_GUI.py`**  
  A PyQt-based graphical user interface (GUI) tool for editing and refining dispersion curves. The tool allows interactive data selection, removal, and editing, and it supports visualizing dispersion spectra and saving the results to new files.

## Workflow

1. **Data Collection**: Gather ambient noise data using DAS or other seismic sensors. 
   
2. **Data Transformation**: Convert the data files to formats such as SGY or NPZ. Other formats are supported, but the code may need to be modified for those.

3. **Processing**: Place the daily data into a single folder and run the relevant scripts to process the data.
