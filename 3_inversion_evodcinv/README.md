# Inversion Evodcinv Project

This repository contains tools and scripts for performing seismic inversion analysis using the `evodcinv` library and related packages. The project is organized into several folders, each serving a specific purpose in the workflow from input data preparation to visualization of results.

---

## Repository Structure

### 1. `1_a_inversion_single_mode`
This folder contains scripts for handling single-mode inversion.

- **`batch_inversion.py`**  
  Automates the batch processing of single-mode inversion for multiple input files in a specified directory.

- **`inversion.py`**  
  Performs single-mode inversion for a single input file and generates results. Includes data loading, model initialization, inversion configuration, and visualization.

### 2. `1_b_inversion_multi-mode`
This folder contains scripts for handling multi-mode inversion.

- **`batch_inversion_multi-mode.py`**  
  Automates the batch processing of multi-mode inversion for multiple input files in a specified directory. Creates output directories and organizes results.

- **`inversion_multi-mode.py`**  
  Handles multi-mode inversion for a single input file. Processes dispersion curve data, performs inversion using `evodcinv`, and generates both text and graphical results.

### 3. `2_plot`
This folder contains scripts for processing and visualizing inversion results.

- **`1_depth_conversion.py`**  
  Converts inversion result files to depth-based text files. Processes layers, calculates depth increments, and saves reformatted files.

- **`2_add_x_location.py`**  
  Adds x-location information to processed text files. Adjusts and formats data to include x-location based on specific scenarios.

- **`3_merge_to_one_txt.py`**  
  Merges multiple processed `.txt` files into a single unified text file. Ensures data integrity by filtering specific columns and values.

- **`4_plot_scatter.py`**  
  Creates scatter plots of the original inversion data points. Includes color mapping based on Vs (shear-wave velocity) values.

- **`5_plot_interpolation.py`**  
  Performs cubic interpolation of the inversion data and generates visualizations. Useful for smoothing and filling gaps in the data.

- **`12345—A Script—From Inversion to Final Plot.py`**  
  A master script that integrates the full workflow from inversion result processing to final plotting.

- **`4_txt_plot_interpolation_plot_20240617_KD.py`**  
  Interpolates and visualizes Vs data using KDTree-based nearest neighbor interpolation.

- **`4_txt_plot_interpolation_plot_20240618_SPI.py`**  
  Visualizes Vs data using Smooth Particle Interpolation (SPI) for more natural smoothing.

- **`4_txt_plot_interpolation_plot_20240703_SPI.py`**  
  Another implementation of SPI-based visualization with adjustable smoothing parameters.

### Root Directory
The root directory contains the following files:

- **`README.md`**  
  This file, documenting the structure and functionality of the repository.

---

## Workflow Overview

### 1. Single-Mode Inversion
1. Place input files in a specified directory.
2. Use `1_a_inversion_single_mode/batch_inversion.py` to process all files.
3. The results will be saved in the output directory.

### 2. Multi-Mode Inversion
1. Place input files in a specified directory.
2. Use `1_b_inversion_multi-mode/batch_inversion_multi-mode.py` to process all files.
3. The results will include text summaries and graphical plots.

### 3. Visualization
1. Use the scripts in `2_plot` to process inversion results:
   - Convert results to depth-based text files.
   - Merge multiple files into a single dataset.
   - Generate scatter plots and interpolated visualizations.
2. Use the master script `12345—A Script—From Inversion to Final Plot.py` for a complete end-to-end workflow.

---

## Dependencies

Ensure the following dependencies are installed:

- Python libraries:
  - `numpy`
  - `matplotlib`
  - `scipy`
  - `sklearn`
  - `joblib`
- Fonts: Arial (`/usr/share/fonts/truetype/msttcorefonts/Arial.ttf`)
- External libraries:
  - `evodcinv`
  - `disba`

---

## Notes

- **File Naming Conventions:** Ensure that input and output files follow the naming conventions used in the scripts for smooth execution.
- **Path Adjustments:** Update paths in scripts to match your directory structure.
- **Custom Modifications:** Adjust specific parameters (e.g., x-location, interpolation methods) in the scripts based on your data and requirements.

---

## Contributing

Contributions are welcome! If you encounter issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
