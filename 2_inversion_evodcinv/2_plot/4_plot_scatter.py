# -*- encoding: utf-8 -*-
'''
@File        :   4_plot_scatter.py
@Time        :   2025/01/03 22:42:28
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KDTree
import os
import sys
from joblib import Parallel, delayed

# Set font for plots
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 8

# Read input file
input_file = sys.argv[1]

# Example: Uncomment the line below for testing locally
# input_file = r"\\?\H:\lhyonedrive\OneDrive\termite\school\active_source_2\shots_510_610_split_removebad_shottimematch_ALL_dispersion_6_18_disp_curve_adjusted_inversion_together_onetxt\shots_510_610_split_removebad_shottimematch_ALL_dispersion_6_18_disp_curve_adjusted_inversion_together.txt"

data = np.loadtxt(input_file)

# Extract columns from the data
x = data[:, 0]  # First column: x (distance in meters)
z = data[:, 1]  # Second column: z (depth in meters)
vs = data[:, 2]  # Third column: Vs (shear-wave velocity in m/s)

# Check basic statistics of Vs data
print("Basic statistics of Vs data:")
print(f"Minimum: {np.min(vs)}")
print(f"Maximum: {np.max(vs)}")
print(f"Mean: {np.mean(vs)}")
print(f"Standard Deviation: {np.std(vs)}")

# Create a grid
xi = np.linspace(min(x), max(x), 1000)
zi = np.linspace(min(z), max(z), 1000)
xi, zi = np.meshgrid(xi, zi)

# Define colormap and levels
cmap = 'jet'
levels = 100

# Get the input file's directory and name
input_dir = os.path.dirname(input_file)
input_filename = os.path.basename(input_file)

# Calculate global minimum and maximum of Vs data
vs_min = np.min(vs)
vs_max = np.max(vs)

# Ensure the colormap range is set correctly
vmin, vmax = vs_min, vs_max

# Plot a scatter plot of the original data points
plt.figure(figsize=(6, 12))
ax = plt.gca()  # Get the current axis
ax.set_aspect('equal')  # Set equal aspect ratio for x and y axes
scatter = plt.scatter(x, z, c=vs, cmap=cmap, vmin=vmin, vmax=vmax)
plt.colorbar(scatter, label='Vs (m/s)', shrink=0.06, aspect=10)
plt.xlabel('Trace')
plt.ylabel('Depth (m)')
plt.title('Original Data Points')

# Invert the y-axis
ax.invert_yaxis()

# Save the scatter plot
scatter_output_filename = f"{os.path.splitext(input_filename)[0]}_scatter_{cmap}.png"
scatter_output_filepath = os.path.join(input_dir, scatter_output_filename)
plt.savefig(scatter_output_filepath, dpi=300, bbox_inches='tight')
plt.close()

print("Scatter plot of original data points has been saved.")
