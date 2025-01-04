# Passive Seismic Imaging using Frequency-Bessel Method

This repository contains scripts for active seismic imaging using Distributed Acoustic Sensing (DAS) and the CC-FJpy package (https://github.com/ColinLii/CC-FJpy).

## Experimental Setup

1. **Fiber-optic cables preparation**: Ensure fiber-optic cables are ready and perform tap tests.
2. **Passive seismic sources**: Just record the ambient noise data, set reasonable gauge length and channel spacing.
3. **Data conversion**: Convert `.dat` files to `.sgy` file format, or other type but the code need to be modified.
4. **Data processing**: Follow the data processing workflow.


## Repository Structure

### `1_surface_wave_dispersion_spectrum_calculation`
This folder contains scripts for calculating surface wave dispersion spectra from passive seismic data.

- **`noise_dispersion_from_noise_sacs_to_CCF_FJpng_h5_20241004.py`**  
  Processes seismic noise data to generate cross-correlation functions (CCFs), calculate dispersion spectra, and save results in H5 and PNG formats. Includes preprocessing, filtering, and multi-threaded processing for efficiency.

- **`plot_crosscorrelationfunctions_from_npz.py`**  
  Loads cross-correlation function data from `.npz` files, calculates time-domain representations, and visualizes them as time series plots. It supports filtering by specific station pairs.

### `2_pick_curve`
This folder includes scripts for picking dispersion curves from pre-calculated spectra.

- **`batch_pick_dispersion_curves_passive_imaging_FJ.py`**  
  Takes a folder as input, retrieves file information, and passes it to 'pick_dispersion_curves_passive_imaging_FJ.py' for processing.

- **`pick_dispersion_curves_passive_imaging_FJ.py`**  
  A GUI-based script for manually picking dispersion curves from dispersion spectra stored in `.h5` files. Provides tools for visualization, interaction, and saving picked curves.
