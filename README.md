# Personal Code Library

This repository contains Python scripts and tools for seismic data processing, inversion, and imaging. Each subfolder represents a specific workflow or utility for seismic data analysis.

## Repository Structure

### `1_active_seismic_imaging_FJ`
Tools for **active seismic imaging** focused on frequency-domain and spatial-domain analysis using Distributed Acoustic Sensing (DAS) and the CC-FJpy package. For detailed setup and processing, refer to the https://github.com/ColinLii/CC-FJpy.

### `1_passive_seismic_imaging_C3`
Implements **three-station cross-correlation (C3)** for passive seismic imaging. This method calculates surface wave dispersion spectra based on ambient noise and rolling array processing. For additional details, refer to the https://gitee.com/gemini_lh/surfacewave-c3/tree/master/surfacewaveC3.

### `1_passive_seismic_imaging_FJ`
Tools for **passive seismic imaging** using the Frequency-Bessel Method. This repository includes scripts for processing ambient seismic data to generate cross-correlation functions (CCFs) and dispersion spectra. For more details, see https://github.com/ColinLii/CC-FJpy.

### `2_inversion_cps330`
Scripts for **seismic inversion** using CPS330 for subsurface modeling. This includes data preparation, processing, and inversion using dispersion curves. See the https://www.eas.slu.edu/eqc/eqc_cps/getzip.html for further details.

### `2_inversion_evodcinv`
Tools for **seismic inversion** using the **EvodcInv** framework, which allows parameter estimation and velocity model refinement. This package supports single and multi-mode inversions. For more information, refer to the https://github.com/keurfonluu/evodcinv.

### `process_file_dat`
Tools for processing **DAT format** seismic data, including file conversion and preprocessing tasks. This includes converting `DAT` files to `SAC` and `SEG-Y` formats.

### `process_file_sac`
Scripts for processing **SAC files**, including normalization, filtering, and visualization of seismic data.

### `process_file_sgy`
Scripts for processing **SEG-Y files**, including tasks such as filtering, correlation, time slicing, and various transformations.

### `process_sweep_signal`
Toolkit for processing **sweep signals** in SEG-Y files. It includes trace extraction, filtering, correlation, and velocity filtering.
