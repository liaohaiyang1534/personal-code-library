# DAS Active Source Surface Wave Processing

This repository contains a complete workflow for processing DAS (Distributed Acoustic Sensing) hammering active source seismic records. The workflow includes steps from raw data preprocessing, signal selection, classification, and processing, to surface wave dispersion analysis, dispersion curve extraction, inversion, and visualization.

The repository is intended for personal use, but others can also utilize it with proper credit to third-party code used in some core parts.

---

## **Folder Structure**

The project is organized into several modules:

### `10_depth_txt`
- Python scripts for depth transformation, adding X-location, combining text files, and plotting scatter points.
- **Main scripts:**
  - `main_12345.py`: Core script for orchestrating tasks.

### `1_extract_specific_traces`
- Extract specific traces from seismic records.
- **Main scripts:**
  - `batch_extract_specific_traces.py`
  - `extract_specific_traces.py`

### `2_STALTA`
- STA/LTA-based signal processing.
- Includes `old_project` and `optimized_project` subfolders.
- **Main scripts:**
  - `optimized_project/main.py`: Improved STA/LTA processing pipeline.

### `3_shot_time_match`
- Tools for matching shot times (currently deprecated).

### `4_shot_center`
- Split SGY files for shot center processing.
- **Main scripts:**
  - `batch_split_sgy.py`
  - `split_sgy.py`

### `5_bandpass`
- Bandpass filtering of SGY files and frequency analysis.
- **Main scripts:**
  - `batch_bandpass_sgy.py`
  - `plot_sgy_frequency.py`

### `6_single_sgy_FJs`
- Scripts for processing single SGY files, including renaming, converting SAC files, and addressing differences in array length or trace spacing.
- **Main scripts:**
  - `FJ_single_processing_sacs_to_pic.py`

### `7_windows_PickDispersionCurves-master`
- Scripts for surface wave dispersion curve picking (third-party code).
- **Main scripts:**
  - `pick_dispersion_curves.py`: Core script for picking dispersion curves.
  - `batch_pick_dispersion_curves_主动源FJ提取脚本.py`: Batch extraction script for active source FJ signals.
- **Output:**
  - `dispersion_curve.csv`: Extracted dispersion curve data.

### `8_dispersion_txt_adjustment`
- Scripts for adjusting and preparing dispersion text files.

### `9_inversion`
- Scripts for surface wave dispersion curve inversion (third-party code).
- **Main scripts:**
  - `inversion.py`: Core script for inversion.
  - `batch_inversion.py`: Batch inversion script.

---

## **Workflow**

1. **Preprocessing**
   - Extract specific traces using scripts in `1_extract_specific_traces`.
   - Perform STA/LTA processing using `2_STALTA` scripts.
   - Match shot times (if needed) using `3_shot_time_match`.

2. **Signal Processing**
   - Use `4_shot_center` to split SGY files.
   - Apply bandpass filtering and analyze frequency using `5_bandpass`.

3. **Dispersion Curve Analysis**
   - Process single SGY files with `6_single_sgy_FJs` scripts.
   - Pick dispersion curves using `7_windows_PickDispersionCurves-master` (third-party code).

4. **Dispersion Curve Adjustment**
   - Use scripts in `8_dispersion_txt_adjustment` for text adjustments.

5. **Inversion**
   - Perform inversion with `9_inversion` scripts (third-party code).

6. **Visualization**
   - Generate final visualizations using scripts in `10_depth_txt`.

---

## **Requirements**

- Python 3.x
- Required Python libraries:
  - numpy
  - scipy
  - matplotlib
  - pandas
  - obspy
- Third-party software for dispersion analysis and inversion (included in `7_windows_PickDispersionCurves-master` and `9_inversion`).

---

## **Usage**

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/DAS_Active_Source_Surface_Wave_Processing.git
   cd DAS_Active_Source_Surface_Wave_Processing
