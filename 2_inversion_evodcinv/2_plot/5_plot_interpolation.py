# -*- encoding: utf-8 -*-
'''
@File        :   5_plot_interpolation.py
@Time        :   2025/01/03 22:42:48
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os
import sys
from matplotlib.ticker import FuncFormatter

# Set font for plots
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 8

# Read input data
input_file = sys.argv[1]
data = np.loadtxt(input_file)

# Extract columns
x = data[:, 0]  # First column: x (m)
z = data[:, 1]  # Second column: z (m)
vs = data[:, 2]  # Third column: Vs (m/s)

# Filter z values within a certain range
deepmeter = 10
mask = z <= deepmeter
x = x[mask]
z = z[mask]
vs = vs[mask]

# Create interpolation grid
xi = np.linspace(min(x), max(x), 1000)
zi = np.linspace(min(z), max(z), 1000)
xi, zi = np.meshgrid(xi, zi)

# Perform cubic interpolation
vs_interp_grid = griddata((x, z), vs, (xi, zi), method='cubic')

# Configure plot
plt.figure(figsize=(8, 8))
ax = plt.gca()

# Set aspect ratio
ax.set_aspect(2)

# Dynamically calculate color range
vmin = np.min(vs_interp_grid) if np.min(vs_interp_grid) >= 0 else 0
vmax = np.max(vs_interp_grid)

# Define colormap
cmap = 'jet'

# Plot interpolation result
contourf = plt.contourf(xi, zi, vs_interp_grid, cmap=cmap, vmin=vmin, vmax=vmax)
cbar = plt.colorbar(contourf, label='Vs (m/s)', shrink=0.06, aspect=10)

# Set colorbar ticks
cbar.set_ticks(np.linspace(vmin, vmax, num=6))

# Set x-axis limits
plt.xlim(90, 203)

# Compute minimum and maximum x-axis range
x_min = min(x)
x_max = max(x)

# Define a function to customize x-axis ticks
def custom_x_ticks(x, pos):
    """Show x if it is a multiple of 5 or the minimum/maximum range."""
    if x == x_min or x == x_max or x % 5 == 0:
        return f'{x:.0f}'
    return ''

# Apply custom tick formatter
ax.xaxis.set_major_formatter(FuncFormatter(custom_x_ticks))

# Set axis labels
plt.xlabel('Channel Number')
plt.ylabel('Depth (m)')

# Invert y-axis
ax.invert_yaxis()

# Save the plot
input_dir = os.path.dirname(input_file)
input_filename = os.path.basename(input_file)
output_filename = f"{os.path.splitext(input_filename)[0]}_linear_interpolation_{cmap}.png"
output_filepath = os.path.join(input_dir, output_filename)
plt.savefig(output_filepath, dpi=300, bbox_inches='tight')
plt.close()

print("Linear interpolation result image has been saved.")
