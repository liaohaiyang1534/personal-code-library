# -*- encoding: utf-8 -*-
'''
@File        :   8_plot_vel_windows_with_sgy_2d_data.py
@Time        :   2025/01/03 22:52:35
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import sys
import segyio
import numpy as np
from matplotlib import pyplot as plt
import os
import matplotlib
matplotlib.use('agg')

# Get the file path from command-line arguments
if len(sys.argv) > 1:
    sgy_file_path = sys.argv[1]
else:
    print("Error: No file path provided.")
    sys.exit(1)

def normalize_traces(traces):
    """ Normalize each seismic trace to the range [-1, 1]. """
    max_abs_vals = np.max(np.abs(traces), axis=1, keepdims=True)
    normalized_traces = traces / max_abs_vals
    return normalized_traces

def plot_velocity_profile(sgy_file_path, dx=0.5, dt=0.002, vmin=100, vmax=2000):
    """
    Plot the velocity profile on seismic data.

    Args:
        sgy_file_path (str): Path to the SEG-Y file.
        dx (float): Spatial spacing between traces (meters).
        dt (float): Time sampling interval (seconds).
        vmin (int): Minimum velocity to plot (m/s).
        vmax (int): Maximum velocity to plot (m/s).
    """
    with segyio.open(sgy_file_path, "r", ignore_geometry=True) as f:
        # Read all traces
        traces = segyio.tools.collect(f.trace[:])
        nt = f.samples.size  # Number of time samples
        nx = f.tracecount    # Number of traces

    # Normalize the traces
    normalized_traces = normalize_traces(traces)

    # Compute the spatial position for each trace
    r = np.arange(0, nx * dx, dx)

    # Compute the time array in milliseconds
    t = np.linspace(0, 1400, nt)  # Create an evenly spaced time array up to 1400 ms

    # Initialize the plot
    plt.figure(figsize=(12, 6), dpi=50)
    plt.imshow(normalized_traces.T, aspect='auto', cmap='gray', extent=[0, max(r), max(t), 0])

    # Compute velocity lines for vmin and vmax
    t_vmin = 2 * r / vmin * 1000  # For vmin
    t_vmax = 2 * r / vmax * 1000  # For vmax

    # Plot velocity lines
    plt.plot(r, t_vmin, 'r', label=f'v = {vmin} m/s')
    plt.plot(r, t_vmax, 'b', label=f'v = {vmax} m/s')

    plt.xlabel('Distance (m)')
    plt.ylabel('Time (ms)')
    plt.title('Velocity Profile on Seismic Data')
    plt.colorbar(label='Normalized Amplitude')
    plt.legend()

    plt.ylim(max(t), 0)  # Ensure time axis increases from top to bottom
    plt.xlim(0, max(r))

    # Save the plot
    folder_path = os.path.dirname(sgy_file_path)
    file_name = os.path.basename(sgy_file_path)
    base_file_name, _ = os.path.splitext(file_name)
    output_file_path = os.path.join(folder_path, f'{base_file_name}_velocity_profile.png')

    plt.savefig(output_file_path)
    plt.close()

    print(f"Velocity profile image saved as '{output_file_path}'.")

# Call the function to plot the velocity profile
plot_velocity_profile(sgy_file_path)
