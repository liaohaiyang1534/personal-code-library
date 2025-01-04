# SEG-Y File Processing Toolkit

This repository contains a series of scripts and tools for processing, analyzing, and converting SEG-Y seismic data. These tools are designed to facilitate tasks such as bandpass filtering, downsampling, FK analysis, trace visualization, and format conversion.



## Scripts

**`csv_to_sgy.py`**  
  Converts CSV files into SEG-Y format. Extracts sampling rates from file names and generates SEG-Y files with trace headers.

**`extra_specific_time_and_trace_of_sgy.py`**  
  Extracts a specific range of traces and time intervals from a SEG-Y file, saving them into a new SEG-Y file. Includes plotting of original and cropped data.

 **`fk_analysis_and_plot.py`**  
  Performs FK analysis on seismic data and generates contour plots of frequency and wavenumber distributions.

 **`remove_mean_and_trend.py`**  
  Removes the mean and detrends traces within a SEG-Y file. Supports polynomial detrending of any degree.

 **`fk_filter.py`**  
  Applies F-K domain filtering to SEG-Y files using predefined velocity masks and smooth Gaussian decay. Outputs filtered SEG-Y files and visualizations.

 **`merge_sgy.py`**  
  Merges multiple SEG-Y files into a single SEG-Y file.

 **`plot_trace_in_sgy.py`**  
  Plots specific traces from a SEG-Y file. Includes options for combining traces, normalizing scales, and marking specific times.

 **`sgy_to_csv.py`**  
  Converts SEG-Y files into CSV format. Each trace is represented as a column in the CSV.

 **`sgy_to_txt.py`**  
  Converts SEG-Y files into TXT format. Each trace is saved as a row in the text file.

 **`sgy_to_sac.py`**  
  Converts traces from SEG-Y files into SAC format. Includes support for calculating distance headers.

 **`single_frequency_energy_sgy.py`**  
  Normalizes the energy of frequency components in SEG-Y files, applies inverse Fourier transforms, and visualizes the results.

 **`theoretical_sweep_signal.py`**  
  Generates a theoretical sweep signal, saves it in SAC format, and visualizes its waveform.
