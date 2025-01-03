# Active Seismic Imaging Project

This repository contains scripts, tools, and data processing workflows for active seismic imaging. The project is organized into multiple subfolders, each addressing specific tasks such as trace extraction, STA/LTA processing, shot center splitting, bandpass filtering, and dispersion curve picking. Below is a detailed description of the repository structure and the functionality of each file and folder.

---

## Folder Structure

### `1_extract_specific_traces`
This folder contains scripts for extracting specific traces from SEG-Y files.

- **`batch_extract_specific_traces.py`**  
  Processes a folder containing `.sgy` files and extracts specific traces using predefined parameter ranges.

- **`extract_specific_traces.py`**  
  Extracts a specified range of traces from a single `.sgy` file and saves the result as a new `.sgy` file.

---

### `2_STALTA`
This folder contains scripts and modules for implementing STA/LTA (Short-Term Average over Long-Term Average) seismic signal analysis.

- **`config.json`**  
  Configuration file for STA/LTA processing parameters.

- **`main.py`**  
  Main script to run STA/LTA detection and processing.

- **`shot_time_match_module.py`**  
  Matches shot times in SEG-Y files to a reference timestamp file.

- **`stalta_module.py`**  
  Detects trigger events using STA/LTA and extracts time windows of interest from SEG-Y files.

- **`total_energy_module.py`**  
  Calculates the total energy of seismic traces and filters files based on energy thresholds.

- **`utils.py`**  
  Contains utility functions such as logging setup, output folder creation, and listing SEG-Y files in a directory.

---

### `3_shot_time_match`
This folder focuses on matching shot times and processing related to shot metadata.

- **`batch_shot_time_match.py`**  
  Batch processes SEG-Y files for matching shot times to a reference file.

- **`shot_time_match.py`**  
  Matches shot times in a single SEG-Y file using a timestamp file.

---

### `4_shot_center`
This folder contains scripts for splitting SEG-Y files into parts based on shot centers.

- **`batch_split_sgy.py`**  
  Splits SEG-Y files into left and right parts based on calculated shot centers and coordinates.

- **`split_sgy.py`**  
  Splits a single SEG-Y file into left and right parts using a specified middle trace index.

---

### `5_bandpass`
This folder provides scripts for applying bandpass filters to SEG-Y files and analyzing their frequency spectra.

- **`bandpass_sgy.py`**  
  Applies a bandpass filter to a single SEG-Y file and saves the filtered result.

- **`batch_bandpass_sgy.py`**  
  Processes multiple SEG-Y files in a directory by applying bandpass filters.

- **`plot_sgy_frequency.py`**  
  Analyzes and plots the frequency spectrum of SEG-Y files, generating visualizations for direct and normalized spectra.

---

### `6_single_sgy_FJs`
This folder contains scripts for advanced processing of single SEG-Y files, including SAC file conversion, array length picking, and trace spacing adjustments.

- **`FJ_single_processing_sacs_to_pic.py`**  
  Processes SAC files for dispersion analysis using FJ (Frequency-Joint) transformation and generates visualizations.

- **`batch_grouping_file.py`**  
  Groups files into subfolders based on patterns in their filenames.

- **`batch_rename_file.py`**  
  Renames files in bulk based on filename patterns.

- **`convert_sacs_from_a_sgy.py`**  
  Converts traces in a SEG-Y file to SAC format.

- **`pick_diff_arraylength.py`**  
  Extracts traces from a SEG-Y file to create subarrays of different lengths.

- **`pick_diff_offset_2.py`**  
  Removes traces based on offset and generates new SEG-Y files with adjusted offsets.

- **`pick_diff_trace_spacing.py`**  
  Resamples traces in a SEG-Y file to achieve different trace spacing.

- **`rename_file.py`**  
  Renames files to adjust the order of `arraylength` and `offset_minoff` in filenames.

- **Shell Scripts**  
  Various shell scripts for automating batch processing tasks:
  - `single_batch_processing.sh`
  - `single_batch_processing_attack.sh`
  - `single_sgy_FJ.sh`
  - `single_sgy_FJ_attack.sh`

---

### `7_pick_curve`
This folder is dedicated to picking dispersion curves from processed data.

- **`pick_dispersion_curves_active_imaging_FJ.py`**  
  Provides a GUI tool for manually picking dispersion curves from `.h5` files containing processed seismic data.

- **`batch_pick_dispersion_curves_active_imaging_FJ.py`**  
  Automates the process of dispersion curve picking for multiple `.h5` files using the above GUI tool.

---

## General Notes
- **SEG-Y Files**  
  The repository heavily relies on SEG-Y files, a standard format for storing seismic data. The `segyio` library is used extensively for reading, writing, and manipulating these files.

- **Dependencies**  
  Most scripts require Python and libraries such as `segyio`, `numpy`, `matplotlib`, `obspy`, and `h5py`. Make sure to install these dependencies before running the scripts.

- **Data Processing Workflow**  
  1. Extract traces of interest using scripts in `1_extract_specific_traces`.
  2. Perform STA/LTA analysis with scripts in `2_STALTA`.
  3. Match shot times using scripts in `3_shot_time_match`.
  4. Split SEG-Y files into parts with scripts in `4_shot_center`.
  5. Apply bandpass filters using scripts in `5_bandpass`.
  6. Process single SEG-Y files for advanced analysis using scripts in `6_single_sgy_FJs`.
  7. Pick dispersion curves using scripts in `7_pick_curve`.

---

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.
