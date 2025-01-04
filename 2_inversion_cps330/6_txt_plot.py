# -*- encoding: utf-8 -*-
'''
@File        :   6_txt_plot.py
@Time        :   2025/01/03 22:40:45
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os
import sys

# Use the Agg backend to save plots without displaying them
plt.switch_backend('Agg')

# Read input data file
input_file = sys.argv[1]
data = np.loadtxt(input_file)

# Extract columns from the data
x = data[:, 0]  # First column: x (m)
z = data[:, 1]  # Second column: z (m)
vs = data[:, 2]  # Third column: Vs (m/s)

# Create a grid for interpolation
xi = np.linspace(min(x), max(x), 100)
zi = np.linspace(min(z), max(z), 100)
xi, zi = np.meshgrid(xi, zi)

# Define interpolation methods
methods = ['cubic']

# Define colormap
cmap = 'jet'

# Get the input file's directory and name
input_dir = os.path.dirname(input_file)
input_filename = os.path.basename(input_file)

# Interpolate and plot for each method
for i, method in enumerate(methods):
    vi = griddata((x, z), vs, (xi, zi), method=method)

    # Create the plot
    plt.figure(figsize=(10, 6))
    contour = plt.contourf(xi, zi, vi, levels=15, cmap=cmap)
    plt.colorbar(contour, label='Vs (m/s)')
    plt.xlabel('Distance (m)')
    plt.ylabel('Depth (m)')

    # Save the plot
    output_filename = f"{os.path.splitext(input_filename)[0]}_{i+1}_{method}_{cmap}.png"
    output_filepath = os.path.join(input_dir, output_filename)
    plt.savefig(output_filepath, dpi=300)
    plt.close()

print("All interpolated images have been saved.")
