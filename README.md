# Personal Code Library

This repository serves as a comprehensive collection of Python scripts and tools for seismic data processing, inversion, and imaging. Each subfolder represents a distinct workflow or set of utilities designed for specific tasks in seismic data analysis.

---

## Repository Structure

### `1_active_seismic_imaging_FJ`
Scripts and workflows for **active seismic imaging**, specifically focusing on frequency-domain and spatial-domain analysis. Includes tools for generating seismic images using active sources.

### `2_passive_seismic_imaging_frequency-Bessel_FJ`
Contains tools for **passive seismic imaging** using frequency-domain Bessel function analysis. This workflow is designed for applications in seismic noise analysis and passive imaging.

### `2_passive_seismic_imaging_three_station_C3`
Implements **three-station cross-correlation (C3)** techniques for passive seismic imaging. Useful for extracting seismic velocity and analyzing subsurface structure using passive data.

### `2_passive_seismic_imaging_binstack_and_fkSNR-slecting`
This folder focuses on **bin stacking and FK-based SNR selection** for passive seismic data. Includes advanced methods for improving the signal-to-noise ratio in passive imaging workflows.

### `3_inversion_cps330`
Scripts related to **seismic inversion** using CPS330 techniques. These scripts likely focus on modeling subsurface properties using seismic data.

### `3_inversion_evodcinv`
Contains utilities for **seismic inversion** using the EvodcInv framework. This folder may involve parameter estimation and velocity model refinement for inversion.

### `4_process_file_sgy`
A collection of tools for processing **SEG-Y files**, including reading, writing, and applying various processing steps such as filtering, correlation, and time slicing. 

> For more details, check the corresponding `README.md` in the folder.

### `4_process_file_sac`
Scripts for processing **SAC (Seismic Analysis Code) files**, including trace normalization, waveform filtering, and visualization.

### `4_process_file_dat`
Processing utilities for seismic data stored in **DAT format**, including file conversion and preprocessing steps.

### `5_process_sweep_signal`
A comprehensive toolkit for processing **sweep signals** in SEG-Y files. Includes functionalities such as:
- Correlation-based trace extraction
- Bandpass and velocity filtering
- FK filtering and wavelet-based noise reduction
- SEG-Y header manipulation and trace reversal

> Detailed documentation for this folder is available in its own `README.md`.

---
