
# Inversion using evodcinv program



This repository contains scripts for seismic inversion analysis using evodcinv package (https://github.com/keurfonluu/evodcinv). 




## Repository Structure






### `1_a_inversion_single_mode`


- **`batch_inversion.py`**  
Takes a folder as input, retrieves file information, and passes it to `inversion.py`

- **`inversion.py`**  
  Performs single-mode inversion for a single input file and generates results.

### `1_b_inversion_multi-mode`


- **`batch_inversion_multi-mode.py`**  
  Takes a folder as input, retrieves file information, and passes it to `inversion_multi-mode.py`

- **`inversion_multi-mode.py`**  
  Performs multi-mode inversion for a single input file and generates results.

### `2_plot`



- **`Run this script - from inversion results to final plot - 12345.py`**  
  A master script that integrates the full workflow from inversion result processing to final plotting.




- **`1_depth_conversion.py`**  
  Converts inversion result files to depth-based text files.

- **`2_add_x_location.py`**  
  Adds x-location information to processed text files.

- **`3_merge_to_one_txt.py`**  
  Merges multiple processed `.txt` files into a single unified text file.

- **`4_plot_scatter.py`**  
  Creates scatter plots of the original inversion data points.



- **`4_txt_plot_interpolation_plot_20240617_KD.py`**  
  Interpolates and visualizes Vs data using KDTree-based nearest neighbor interpolation.

- **`4_txt_plot_interpolation_plot_20240618_SPI.py`**  
  Visualizes Vs data using Smooth Particle Interpolation (SPI) for more natural smoothing.

- **`4_txt_plot_interpolation_plot_20240703_SPI.py`**  
  Another implementation of SPI-based visualization with adjustable smoothing parameters.

- **`5_plot_interpolation.py`**  
  Performs cubic interpolation of the inversion data and generates visualizations.


