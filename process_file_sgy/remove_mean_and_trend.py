# -*- encoding: utf-8 -*-
'''
@File        :   remove_mean_and_trend.py
@Time        :   2025/01/03 22:50:56
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import segyio
import shutil
import numpy as np

def remove_mean_and_detrend_from_sgy(original_file_path, poly_degree=1):
    """
    Removes mean and detrends SEGY file data.
    Parameters:
    - original_file_path: Path to the original SEGY file.
    - poly_degree: Degree of the polynomial for trend fitting, default is 1 (linear trend).
    """
    # Generate new file path by replacing .sgy extension with _meantrend.sgy
    new_file_path = original_file_path.replace('.sgy', '_meantrend.sgy')
    
    # Copy the original file to the new path
    shutil.copyfile(original_file_path, new_file_path)

    # Open the SEG-Y file in read-write mode, ignoring geometry
    with segyio.open(new_file_path, "r+", ignore_geometry=True) as f:
        # Iterate through all traces
        for i in range(len(f.trace)):
            # Get the current trace data
            trace_data = f.trace[i]
            # Remove mean
            trace_data_without_mean = trace_data - np.mean(trace_data)
            
            # Generate a time series (assuming interval is 1, adjust if needed)
            time_series = np.arange(len(trace_data))
            # Fit a polynomial trend line and get its coefficients
            trend = np.polyfit(time_series, trace_data_without_mean, poly_degree)
            # Compute the values of the trend line
            trend_line = np.polyval(trend, time_series)
            # Subtract the trend line from the mean-removed data to detrend
            detrended_trace_data = trace_data_without_mean - trend_line
            
            # Write the processed trace back to the file
            f.trace[i] = detrended_trace_data

    print(f"File '{new_file_path}' processed successfully with {len(f.trace)} traces.")

# Example usage
original_file_path = "./1.0m_913_gx.sgy"  # Replace with your file path
remove_mean_and_detrend_from_sgy(original_file_path, poly_degree=5)  # Example: detrend with a 5th-degree polynomial
