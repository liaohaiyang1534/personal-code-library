# -*- encoding: utf-8 -*-
'''
@File        :   12_disturb_filter.py
@Time        :   2025/01/03 22:52:56
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import numpy as np
import matplotlib.pyplot as plt
import segyio
import shutil
import matplotlib
matplotlib.use('agg')  # Use Agg backend for non-GUI environments
import sys

# Define input file path
input_file_path = sys.argv[1]
output_file_path = input_file_path.replace('.sgy', '_disturb.sgy')

# Trace spacing
trace_spacing = 0.5  # meters

# Read SEG-Y file
def read_segy(file_path):
    with segyio.open(file_path, "r", ignore_geometry=True) as segyfile:
        segyfile.mmap()
        data = segyio.tools.collect(segyfile.trace[:])
        r = np.arange(1, segyfile.tracecount + 1) * trace_spacing
        delta = segyfile.bin[segyio.BinField.Interval] / 1000000.0
        npts = data.shape[1]
        return data, r, delta, npts

# Normalize data
def normalize_data(data):
    return (data.T / np.max(np.abs(data), axis=1)).T

# Velocity filter with smooth transitions
# Velocity filter with smooth transitions
def velocity_filter(data, r, velocities, delta, taper_length=300):
    Fs = 1.0 / delta
    npts = data.shape[1]
    mask = np.zeros_like(data)
    taper = np.hanning(2 * taper_length)

    for i, distance in enumerate(r):
        min_time = distance / velocities[1]
        max_time = distance / velocities[0]
        min_index = int(min_time * Fs)
        max_index = int(max_time * Fs)

        # Safe application of taper to avoid broadcasting errors
        taper_start = max(min_index - taper_length, 0)
        taper_end = min(max_index + taper_length, npts)

        # Apply taper before min_index
        if taper_start < min_index:
            taper_size = min_index - taper_start
            mask[i, taper_start:min_index] = taper[:taper_size]

        # Set full mask between min_index and max_index
        mask[i, min_index:max(min_index + 1, max_index)] = 1

        # Apply taper after max_index
        if max_index < taper_end:
            taper_start = max_index
            taper_size = taper_end - taper_start
            mask[i, taper_start:taper_end] = taper[-taper_size:]

    filtered_data = data * mask
    return filtered_data, mask


# Save modified data to new SEG-Y file
def save_filtered_segy(input_file, output_file, filtered_data):
    shutil.copy(input_file, output_file)
    with segyio.open(output_file, "r+", ignore_geometry=True) as segyfile:
        segyfile.mmap()
        for i, trace in enumerate(filtered_data):
            segyfile.trace[i] = trace

# Plot original and filtered seismic data
def plot_data(normalized_data, filtered_data, r, delta, npts):
    fig, axes = plt.subplots(1, 2, figsize=(18, 8), sharey=True)
    time_extent = npts / (1.0 / delta)
    axes[0].imshow(normalized_data.T, cmap='gray', extent=[0, max(r), time_extent, 0], aspect='auto')
    axes[1].imshow(filtered_data.T, cmap='gray', extent=[0, max(r), time_extent, 0], aspect='auto')
    axes[0].set_title('Original Data')
    axes[1].set_title('Velocity Filtered Data')
    for ax in axes:
        ax.set_xlabel('Distance (m)')
        ax.set_ylabel('Time (s)')
    plt.colorbar(axes[1].images[0], ax=axes, orientation='vertical')
    plt.savefig('velocity_filtered_comparison.png')
    plt.close()

# Main execution
data, r, delta, npts = read_segy(input_file_path)
normalized_data = normalize_data(data)
filtered_data, mask = velocity_filter(normalized_data, r, [100, 2000], delta)
save_filtered_segy(input_file_path, output_file_path, filtered_data)
plot_data(normalized_data, filtered_data, r, delta, npts)

print("Comparison plot saved as 'velocity_filtered_comparison.png'")
