# SAC Processing

This repository contains a collection of Python scripts for processing and analyzing SAC (Seismic Analysis Code) files.

## Scripts

**`fft_psd_wavelet_frequency_analysis_sac.py`**
Performs FFT, PSD, and wavelet frequency analysis on SAC files and visualizes the results.

**`find_sac.py`**
Searches for SAC files containing '0700' in their names within a specified directory and copies them to a destination folder.

**`merge_sac.py`**
Merges SEGY seismic data, applies F-K domain filtering, normalizes traces, and saves the filtered data as a SEGY file.

**`plot_multi_sacs.py`**
Reads multiple SAC files from a folder, sorts them, and plots their waveforms on a single figure.

**`plot_psd_for_sac_time_ranges.py`**
Computes and plots the Power Spectral Density (PSD) for specified time ranges within SAC files.

**`plot_sac_frequency_one_sac_5s_each_plot.py`**
Divides a SAC file into 5-second segments and plots the frequency spectrum for each segment.

**`plot_time_and_frequency_sac.py`**
Plots both the time-domain waveform and the frequency spectrum of a SAC file.

**`sac_bandpass.py`**
Applies a bandpass filter to SAC files, saves the filtered data, and plots spectral comparisons before and after filtering.

**`sac_downsample.py`**
Downsamples SAC files to a target sampling rate and saves the downsampled versions.

**`sac_to_sgy.py`**
Converts a directory of SAC files into a single merged SEGY file.

**`theoretical_sweep_signal_to_sac.py`**
Generates a theoretical sweep signal, saves it as a SAC file, and performs time-frequency analysis on the signal.

**`txt_to_sac.py`**
Converts waveform data from a text file into a SAC file with appropriate headers.

**`waveform_process_and_visual_of_sac.py`**
Trims SAC files to specified time ranges, plots the original and trimmed waveforms, and saves the plots.

**`wavelet_transform_of_sac.py`**
Performs a wavelet transform on SAC file data and visualizes the wavelet power spectrum.
