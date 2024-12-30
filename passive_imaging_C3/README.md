# README.md

## Overview

This repository contains the implementation of the **Ambient Noise Field Surface Wave Dispersion and Inversion Imaging** project. It is designed to calculate, analyze, and visualize dispersion and inversion models based on seismic ambient noise field data. The project uses a combination of Python scripts and libraries to process, analyze, and plot results, with a structured folder organization for clarity and modularity.

---

## Repository Structure

### Main Folder
The root folder contains Python scripts for high-level operations, primarily focused on seismic ambient noise field analysis. It includes scripts for batch processing, individual computations, and data visualization.

### Subfolders

#### 1. `ambient_seismic_field_imaging`
Contains scripts for seismic field imaging and dispersion calculation.

- **`1_dispersion_calculation_array_run.py`**
  - Implements functions for seismic dispersion calculation, Radon transform, and cross-correlation.
  - Processes `.sgy` seismic files and generates dispersion curves and velocity models.

- **`2_dispersion_calculation_array_run_array_rolling.py`**
  - Automates rolling array dispersion calculations using multiple input files.
  - Uses subprocess to invoke `1_dispersion_calculation_array_run.py` iteratively for different arrays.

- **`3_dispersion_calculation_array_run_array_and_time_rolling.py`**
  - Performs both array-based and time-rolling dispersion calculations.
  - Invokes `2_dispersion_calculation_array_run_array_rolling.py` for batch processing of multiple time windows.

#### 2. `dispersion_curve_picking`
Contains tools for manually revising dispersion curves with a GUI.

- **`dispersion_file_curve_revise_GUI.py`**
  - Interactive GUI tool for visualizing and editing dispersion curve files.
  - Built with PyQt5, supports manual curve adjustments and saves the revised results.

#### 3. `inversion_multi-mode`
Contains scripts for multi-mode inversion processing.

- **`batch_inversion_multi-mode.py`**
  - Automates the inversion of multiple dispersion curve files.
  - Organizes output into structured directories and handles batch processing for multi-mode data.

- **`inversion_multi-mode.py`**
  - Core script for multi-mode seismic inversion.
  - Implements earth modeling and inversion using libraries like `evodcinv` and `disba`.

#### 4. `inversion_single_mode`
Contains scripts for single-mode inversion processing.

- **`batch_inversion.py`**
  - Similar to `batch_inversion_multi-mode.py`, but processes single-mode dispersion data.
  - Automates inversion for multiple single-mode input files.

- **`inversion.py`**
  - Core script for single-mode seismic inversion.
  - Outputs inversion results, including velocity models and plots.

#### 5. `plot`
Contains scripts for visualization and plotting of dispersion and inversion results.

- **`1_depth_conversion.py`**
  - Converts inversion output to depth-velocity text files.
  - Adds depth values based on cumulative thickness calculations.

- **`2_add_x_location.py`**
  - Adds x-location information to the converted depth files.
  - Calculates additional spatial attributes.

- **`3_merge_to_one_txt.py`**
  - Merges multiple `.txt` files into a single consolidated file for further analysis.

- **`4_plot_scatter.py`**
  - Generates scatter plots of seismic velocity data.
  - Useful for analyzing raw velocity distributions.

- **`5_plot_interpolation.py`**
  - Performs interpolation of seismic velocity data and visualizes it as contour plots.
  - Supports customization of aspect ratio and interpolation methods.

- **`4_txt_plot_interpolation_plot_20240617_KD.py`**
  - Implements interpolation using KDTree for smoothed results.
  - Saves results as contour plots.

- **`4_txt_plot_interpolation_plot_20240618_SPI.py`**
  - Uses Smooth Particle Interpolation (SPI) for advanced interpolation.
  - Provides additional flexibility in smoothing parameters.

- **`4_txt_plot_interpolation_plot_20240703_SPI.py`**
  - A refined version of the SPI script with performance optimizations.

- **`12345—A Script—From Inversion to Final Plot.py`**
  - An all-in-one automation script that chains together depth conversion, x-location addition, merging, plotting, and interpolation.
  - Provides a seamless workflow from inversion to final visualization.

---

## Installation and Dependencies

### Prerequisites
- Python 3.8 or later
- Required Python libraries:
  - `numpy`
  - `matplotlib`
  - `scipy`
  - `PyQt5`
  - `sklearn`
  - `segyio`
  - `torch`
  - `evodcinv`

Install all dependencies using:

```bash
pip install -r requirements.txt
```

### Fonts
The scripts assume the availability of Arial and Times New Roman fonts. Update the font paths in the scripts if these are not available on your system.

---

## Usage

1. **Data Preprocessing**
   - Use scripts in `ambient_seismic_field_imaging` to preprocess raw seismic data and generate dispersion curves.

2. **Dispersion Curve Picking**
   - Use the GUI in `dispersion_curve_picking` to manually refine the generated dispersion curves.

3. **Inversion**
   - Use scripts in `inversion_multi-mode` or `inversion_single_mode` to perform inversion on the processed dispersion curves.

4. **Visualization**
   - Use scripts in `plot` to visualize inversion results as scatter plots, interpolations, or contour plots.

5. **Automation**
   - Use `12345—A Script—From Inversion to Final Plot.py` for an end-to-end automated workflow.

---

## Output Structure

The processed results are organized into directories:
- **`best_model_res`**: Text files containing the best velocity models.
- **`models_jpg`**: Visualized inversion results as images.
- **`dispersion_jpg`**: Dispersion curves as images.
- **`merged_txt`**: Consolidated `.txt` files for further analysis.

---

## Contributing

Contributions are welcome! Please follow the standard GitHub workflow:
1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Commit your changes.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact

For questions or support, please open an issue or contact the repository maintainer.
