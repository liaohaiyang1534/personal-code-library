# Passive Seismic Imaging: Three-Station C3 Method

This repository contains tools and scripts for passive seismic imaging using the three-station correlation method (C3). The workflow includes processing seismic data, calculating surface wave dispersion spectra, and extracting dispersion curves. The repository is organized into two main modules, each containing scripts for specific tasks.

---

## Repository Structure

### 1. `1_surface_wave_dispersion_spectrum_calculation`
This module contains scripts for calculating surface wave dispersion spectra from seismic data and includes rolling array functionality for dynamic arrays.

- **`1_dispersion_calculation_array_run.py`**  
  Implements dispersion spectrum calculations for seismic data using array-based processing. Includes preprocessing, cross-correlation, and spectrum computation.

- **`2_dispersion_calculation_array_run_array_rolling.py`**  
  Automates rolling array processing for dispersion spectrum calculations by iteratively moving the array over the data set. Supports configurable array length, spacing, and interval.

- **`3_dispersion_calculation_array_run_array_and_time_rolling.py`**  
  Extends rolling array functionality to incorporate time-based rolling. Processes seismic data across multiple time intervals and spatial positions.

---

### 2. `2_pick_curve`
This module provides tools for visualizing and refining dispersion curves extracted from seismic data.

- **`dispersion_file_curve_revise_GUI.py`**  
  A PyQt-based GUI tool for editing and refining dispersion curves. Allows interactive data selection, removal, and editing. Supports visualizing dispersion spectra and saving results to new files.

---

## Workflow Overview

### 1. Dispersion Spectrum Calculation
1. Use scripts in the `1_surface_wave_dispersion_spectrum_calculation` folder to process seismic data and calculate dispersion spectra.  
2. The rolling array functionality in `2_dispersion_calculation_array_run_array_rolling.py` enables efficient processing for dynamic seismic arrays.

### 2. Dispersion Curve Picking
1. Extract dispersion curves from the calculated spectra using the `dispersion_file_curve_revise_GUI.py` script.
2. Refine the curves interactively with the GUI and save the updated results.

---

## Dependencies

Ensure the following dependencies are installed:

- **Python Libraries**:
  - `numpy`
  - `matplotlib`
  - `scipy`
  - `pandas`
  - `torch`
  - `segyio`
  - `PyQt5`
  - `tqdm`

---

## Notes

- **Input Data**: Ensure seismic data is pre-organized in directories. Supported formats include `.sgy` and `.npz`.
- **Parameter Configuration**: Scripts allow flexibility with parameters like array spacing, length, and time windows. Adjust these to suit your data.
- **Performance**: Multi-threaded processing and GPU acceleration (using PyTorch) are implemented in several scripts.

---

## Contributing

Contributions are welcome! If you encounter issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
