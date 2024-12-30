# Passive Seismic Imaging with Frequency-Bessel Function (FJ Method)

This repository contains a set of Python scripts for processing passive seismic data using the Frequency-Bessel (FJ) method. It includes tools for calculating surface wave dispersion spectra, picking dispersion curves, and other related seismic imaging tasks.

---

## Repository Structure

### 1. `1_surface_wave_dispersion_spectrum_calculation`
This folder contains scripts for calculating surface wave dispersion spectra from passive seismic data.

- **`noise_dispersion_from_noise_sacs_to_CCF_FJpng_h5_20241004.py`**  
  Processes seismic noise data to generate cross-correlation functions (CCF), calculate dispersion spectra, and save results in H5 and PNG formats. Includes preprocessing, filtering, and multi-threaded processing for efficiency.

- **`plot_crosscorrelationfunctions_from_npz.py.py`**  
  Loads cross-correlation function data from `.npz` files, calculates time-domain representations, and visualizes them as time series plots. It supports filtering by specific station pairs.

### 2. `2_pick_curve`
This folder includes scripts for picking dispersion curves from pre-calculated spectra.

- **`batch_pick_dispersion_curves_passive_imaging_FJ.py`**  
  Automates the process of running the dispersion curve picking script (`pick_dispersion_curves_passive_imaging_FJ.py`) for multiple `.h5` files in a directory. The results are saved in a new directory.

- **`pick_dispersion_curves_passive_imaging_FJ.py`**  
  A GUI-based script for manually picking dispersion curves from dispersion spectra stored in `.h5` files. Provides tools for visualization, interaction, and saving picked curves.

---

## Workflow Overview

### 1. Surface Wave Dispersion Spectrum Calculation
1. Preprocess seismic data using `noise_dispersion_from_noise_sacs_to_CCF_FJpng_h5_20241004.py`.
   - Generates cross-correlation functions (CCF).
   - Calculates dispersion spectra using the FJ method.
   - Saves results in H5 format for further analysis.
2. Optionally, use `plot_crosscorrelationfunctions_from_npz.py.py` to visualize the CCF data.

### 2. Picking Dispersion Curves
1. Use `batch_pick_dispersion_curves_passive_imaging_FJ.py` to process multiple `.h5` files containing dispersion spectra.
2. The `pick_dispersion_curves_passive_imaging_FJ.py` script provides an interactive interface for picking dispersion curves from the spectra.

---

## Dependencies

Ensure the following dependencies are installed:

- **Python libraries**:
  - `numpy`
  - `matplotlib`
  - `obspy`
  - `h5py`
  - `scipy`
  - `tqdm`
  - `tkinter` (for GUI interaction)
  - `Pillow` (for image processing)

- **External packages**:
  - `ccfj`: A custom library for handling cross-correlation and FJ method calculations.

---

## Notes

1. **Directory Structure**: Ensure that input data is organized according to the requirements of the scripts (e.g., `.h5` files for dispersion spectrum calculation).
2. **Script Parameters**: Each script may require specific input parameters (e.g., file paths, datasets, and processing options). Review the script headers for detailed usage instructions.
3. **Performance**: Multi-threaded processing is implemented in several scripts to handle large datasets efficiently.

---

## Contributing

Contributions are welcome! If you encounter issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
