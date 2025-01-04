# Sweep Signal Processing Toolkit

This repository contains a set of Python scripts for processing seismic sweep signals stored in SEG-Y format. The scripts facilitate tasks such as trace extraction, correlation, bandpass filtering, velocity filtering, FK analysis, and wavelet filtering.



## Repository Structure



**`1_sweep_to_pulse_batch_processing_15_previous_correlation_code.py`**  
   Implements correlation-based trace extraction and creates multiple outputs, including cropped and correlated traces, frequency analysis plots, and waveform visualizations.

**`2_sweep_copy_process_extrace_to913_and_to1522.py`**  
   Extracts specific ranges of traces from SEG-Y files based on shot indices and creates cropped SEG-Y files for further processing.

**`3_sweep_reverse.py`**  
   Reverses the order of traces in SEG-Y files. 

**`4_sweep_extra_specific_time.py`**  
   Extracts a specific time range from SEG-Y files and saves the result as a new SEG-Y file. 

**`5_clean_files.py`**  
   Deletes unnecessary files in directories and renames specific files based on predefined rules. 

**`6_sweep_spacing.py`**  
   Resamples traces in SEG-Y files based on a specified trace spacing, creating SEG-Y files with adjusted trace distributions.

**`7_sweep_sgy_trace_add_GroupX.py`**  
   Updates `GroupX` coordinates in SEG-Y trace headers to reflect a specified trace spacing. 

**`8_plot_vel_windows_with_sgy_2d_data.py`**  
   Visualizes velocity profiles over 2D seismic data.

**`9_sweep_bandpass.py`**  
   Applies a bandpass filter to traces in SEG-Y files, saving filtered traces into new SEG-Y files.

**`10_fk_filter.py`**  
    Implements FK filtering with velocity-based masks.

**`11_wavelet_filter_rbio.py`**  
    Applies wavelet filtering to seismic traces using biorthogonal wavelets. 

**`12_disturb_filter.py`**  
    Applies velocity filtering to suppress noise in seismic data.
