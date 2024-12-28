# DAS Sweep Signal Processing and Surface Wave Preprocessing Scripts

## Overview

This folder contains a collection of Python scripts designed for the preprocessing of active-source seismic data. The data is recorded using DAS (Distributed Acoustic Sensing) technology with a controlled vibroseis source. The main goal is to transform the recorded sweep signals into pulse signals using cross-correlation and apply various preprocessing techniques for surface wave analysis.

---

## Scripts Included

1. **`1_sweep_to_pulse_batch_processing_15_previous_correlation_code.py`**  
   Batch processes sweep signals into pulse signals using cross-correlation.

2. **`2_sweep_copy_process_extrace_to913_and_to1522.py`**  
   Handles copying and extracting specific data from sweep signals.

3. **`3_sweep_reverse.py`**  
   Reverses the sweep signal for further processing.

4. **`4_sweep_extra_specific_time.py`**  
   Extracts sweep data within specific time windows.

5. **`5_clean_files.py`**  
   Cleans up unnecessary or temporary files generated during processing.

6. **`6_sweep_spacing.py`**  
   Adjusts the spacing of sweep signals for further analysis.

7. **`7_sweep_sgy_trace_add_GroupX.py`**  
   Adds GroupX headers to SEG-Y files for enhanced metadata management.

8. **`8_plot_vel_windows_with_sgy_2d_data.py`**  
   Visualizes 2D seismic data with velocity windows for better understanding of data quality.

9. **`9_sweep_bandpass.py`**  
   Applies bandpass filtering to sweep signals for noise reduction.

10. **`10_fk_filter.py`**  
    Performs F-K domain filtering to enhance seismic data quality.

11. **`11_wavelet_filter_rbio.py`**  
    Applies wavelet-based filtering to remove unwanted noise and enhance resolution.

12. **`12_disturb_filter.py`**  
    Implements disturbance filtering for removing unwanted artifacts in the data.

---

## Prerequisites

To run these scripts, you will need the following Python libraries installed:

- `numpy`
- `matplotlib`
- `segyio`
- `scipy`
- `pywt`
- Other dependencies as needed by individual scripts.

---

## Workflow

### 1. Sweep to Pulse Conversion
Use `1_sweep_to_pulse_batch_processing_15_previous_correlation_code.py` to convert sweep signals into pulse signals using cross-correlation.

### 2. Data Preprocessing
Run scripts such as `6_sweep_spacing.py`, `9_sweep_bandpass.py`, and `10_fk_filter.py` to preprocess the pulse signals.

### 3. Surface Wave Analysis
Apply visualization (`8_plot_vel_windows_with_sgy_2d_data.py`) and advanced filtering techniques (`11_wavelet_filter_rbio.py`, `12_disturb_filter.py`) to prepare data for surface wave analysis.

---

## Folder Structure

- **Raw_Data/**: Place raw SEG-Y files here.
- **Processed_Data/**: Store processed SEG-Y files and intermediate results here.
- **Plots/**: Save visualization outputs such as velocity windows and TX domain plots here.
- **Scripts/**: This folder contains all the Python scripts.

---

## Author and Contact

- **Author**: [Your Name]  
- **Contact**: [Your Email Address]  

If you have any questions or suggestions, feel free to reach out.

---

## License

This code is provided as-is, without warranty of any kind. Use at your own risk.
