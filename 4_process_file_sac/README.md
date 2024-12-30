# SAC File Processing Toolkit

This repository provides a comprehensive toolkit for processing, analyzing, and visualizing seismic data in SAC format. The scripts are designed to handle various tasks, such as filtering, downsampling, frequency analysis, wavelet analysis, and conversion between formats.

---

## Repository Structure

### Root Directory

- **`find_sac.py`**  
  Searches for SAC files matching specific criteria (e.g., containing "0700" in their names) and copies them to a target directory.  
  - **Input**: A directory containing SAC files.  
  - **Output**: A target directory with matching SAC files.

- **`merge_sac.py`**  
  Merges seismic data in SEGY format and applies F-K filtering.  
  - **Input**: Seismic data in SEGY format.  
  - **Output**: Filtered SEGY files and visualizations of the filtering process.

- **`plot_time_and_frequency_sac.py`**  
  Generates time-domain waveforms and frequency spectra for individual SAC files.  
  - **Input**: SAC file.  
  - **Output**: Waveform and frequency spectrum visualizations.

- **`plot_sac_frequency_one_sac_5s_each_plot.py`**  
  Splits a SAC file into 5-second segments and plots the frequency spectrum for each segment.  
  - **Input**: SAC file.  
  - **Output**: Frequency spectrum plots for each segment.

- **`plot_multi_sacs.py`**  
  Plots multiple SAC waveforms on a single canvas, showing waveform amplitudes normalized by distance.  
  - **Input**: Directory containing SAC files.  
  - **Output**: Combined waveform visualization.

- **`plot_psd_for_sac_time_ranges.py`**  
  Computes and plots Power Spectral Density (PSD) for specified time ranges within a SAC file.  
  - **Input**: SAC file.  
  - **Output**: PSD plots for each time range.

- **`fft_psd_wavelet_frequency_analysis_sac.py`**  
  Performs advanced signal processing on SAC files, including FFT, PSD, and wavelet denoising.  
  - **Input**: SAC file.  
  - **Output**: Waveform, spectrum, and denoising visualizations.

- **`sac_bandpass.py`**  
  Applies bandpass filtering to SAC files and compares frequency spectra before and after filtering.  
  - **Input**: SAC file.  
  - **Output**: Filtered SAC file and spectrum comparison plots.

- **`sac_downsample.py`**  
  Downsamples SAC files to a specified sampling rate.  
  - **Input**: SAC file.  
  - **Output**: Downsampled SAC file.

- **`sac_to_sgy.py`**  
  Converts multiple SAC files into a single SEGY file.  
  - **Input**: Directory containing SAC files.  
  - **Output**: Merged SEGY file.

- **`theoretical_sweep_signal_to_sac.py`**  
  Generates theoretical sweep signals, saves them as SAC files, and performs time-frequency analysis.  
  - **Input**: Sweep signal parameters.  
  - **Output**: SAC file, waveform plot, and time-frequency visualization.

- **`txt_to_sac.py`**  
  Converts seismic data from TXT format to SAC format.  
  - **Input**: TXT file with seismic data.  
  - **Output**: SAC file.

- **`waveform_process_and_visual_of_sac.py`**  
  Processes SAC files by trimming and visualizing waveforms in specific time ranges.  
  - **Input**: SAC file.  
  - **Output**: Trimmed SAC file and waveform visualizations.

- **`wavelet_transform_of_sac.py`**  
  Analyzes SAC files using continuous wavelet transform (CWT) and visualizes wavelet power spectra.  
  - **Input**: SAC file.  
  - **Output**: Wavelet power spectrum plots.

---

### Subdirectories

#### `sample_sac_files/`

Contains sample SAC files for testing and demonstration purposes. Example files include:
- `2024-01-24-11-17-19-out0016.sac`
- `2024-01-24-11-17-19-out0017.sac`
- (and more)

---

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/sac-processing-toolkit.git
   cd sac-processing-toolkit
