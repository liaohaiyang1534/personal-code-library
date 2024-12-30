# Inversion CPS330 Project

This repository contains scripts and tools for seismic inversion analysis using CPS330. It is organized into several folders, each with specific functionalities related to dispersion curve processing, model creation, and inversion workflows.

---

## Folder Structure

### 1. `curve_input`
This folder contains input dispersion curve files in `.disp` format.

- **Example files:**
  - `1-19.5.disp`: Dispersion curve file for specific parameters.
  - `1-21.5.disp`: Another dispersion curve file with different parameters.
  - `1-3.5.disp`: A dispersion curve file representing a different configuration.

---

### 2. `curve_input_adjustedtocps`
This folder contains `.txt` files converted and adjusted from the `.disp` files for compatibility with CPS330.

- **Example files:**
  - `1-19.5.txt`: Converted and adjusted file from `curve_input`.
  - `1-21.5.txt`: Another converted file.
  - `1-3.5.txt`: Adjusted dispersion data for CPS330.

---

### 3. `modl`
This folder contains seismic model data files used for inversion processes.

- **`model_20240616_dongtuceng.d`**  
  Represents a specific geological model for inversion.

- **`model_data_zuankongmoxing_1m.d`**  
  A drilling model file with 1-meter resolution.

- **`model_data_zuankongmoxing_1m_smooth.d`**  
  A smoothed version of the 1-meter drilling model.

- **`modl.d`**  
  General model data file for inversion.

---

### Root Directory Files

#### Scripts

- **`1_process_disp.sh`**  
  Shell script to process dispersion data.

- **`2_process_modl.sh`**  
  Script for model file preparation and processing.

- **`3_process_single.sh`**  
  Script for processing a single inversion case.

- **`process_single_disp.sh`**  
  Shell script for handling single dispersion data processing tasks.

- **`RUN_THIS_process_inversion_batch_processing.sh`**  
  Main script to execute batch processing for seismic inversion.

#### Python Scripts

- **`5_txt_adjustedtocps.py`**  
  Converts `.disp` files in `curve_input` to `.txt` format for CPS330. Adjusts the data by converting the second column to kilometers and ensuring proper formatting.

- **`4_out_files_organize.py`**  
  Organizes `.out` files from inversion results. Removes redundant lines, reformats the data to include depth instead of thickness, and merges the results into a single file.

- **`6_txt_plot.py`**  
  Visualizes the inversion results in the form of interpolated Vs (shear wave velocity) plots. Generates `.png` images for the visualized data.

#### Data and Output Files

- **`.disp`**  
  A placeholder dispersion file.

- **`disp.d`**  
  Dispersion data file used in inversion workflows.

- **`figsrf1.eps` and `figsrf1.png`**  
  Visual output files generated during inversion for surface wave results.

- **`figsrf2.eps` and `figsrf2.png`**  
  Another set of visual outputs for surface wave results.

- **`I.PLT` and `IT.PLT`**  
  Plot data files for inversion visualizations.

- **`modl.out`**  
  Output model data from the inversion process.

---

## Workflow Overview

1. **Prepare Dispersion Input:**
   - Add `.disp` files to the `curve_input` folder.
   - Run `5_txt_adjustedtocps.py` to convert and adjust them into `.txt` files compatible with CPS330.

2. **Process Models:**
   - Use the scripts in the root directory (e.g., `2_process_modl.sh`) to prepare and process model data.

3. **Run Inversion:**
   - Execute `RUN_THIS_process_inversion_batch_processing.sh` to perform batch inversions based on prepared input files.

4. **Organize and Merge Outputs:**
   - Use `4_out_files_organize.py` to clean, reformat, and merge `.out` files into a single summarized result.

5. **Visualize Results:**
   - Run `6_txt_plot.py` on the merged output to generate interpolated plots of shear wave velocity (Vs) as a function of depth and distance.

---

## Notes

- **Dependencies:**  
  Ensure Python is installed along with the following libraries:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `scipy`
  - `natsort`

- **Execution Environment:**  
  - Linux or Windows PowerShell for shell scripts.
  - Python environment for running `.py` scripts.

---

## Contributing

Contributions are welcome! Feel free to submit a pull request with bug fixes, improvements, or new features.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
