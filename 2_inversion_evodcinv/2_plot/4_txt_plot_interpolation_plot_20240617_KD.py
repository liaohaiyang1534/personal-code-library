import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KDTree
import os

# Set font styles
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 9

# Load data from the input file
input_file = r"\\?\H:\lhyonedrive\OneDrive\termite\school\active_source_2\shots_510_610_split_removebad_shottimematch_ALL_dispersion_6_18_disp_curve_adjusted_inversion_left_depthtxt_txts_onetxt\shots_510_610_split_removebad_shottimematch_ALL_dispersion_6_18_disp_curve_adjusted_inversion_left_depthtxt_txts.txt"
data = np.loadtxt(input_file)

# Extract columns
x = data[:, 0]  # First column: x (distance in meters)
z = data[:, 1]  # Second column: z (depth in meters)
vs = data[:, 2]  # Third column: Vs (shear-wave velocity in m/s)

# Filter out data where z < -6
mask = z >= -6
x_filtered = x[mask]
z_filtered = z[mask]
vs_filtered = vs[mask]

# Create a KDTree for interpolation
tree = KDTree(np.column_stack((x_filtered, z_filtered)))

# Create an interpolation grid
xi = np.linspace(min(x_filtered), max(x_filtered), 1000)
zi = np.linspace(min(z_filtered), max(z_filtered), 1000)
xi, zi = np.meshgrid(xi, zi)
grid_points = np.vstack([xi.ravel(), zi.ravel()]).T

# Perform weighted nearest-neighbor interpolation using KDTree
k = 1  # Number of neighbors to use (e.g., k=5 for more neighbors)
dist, indices = tree.query(grid_points, k=k)
weights = 1 / (dist + 1e-10)  # Compute weights, avoid division by zero
weights /= weights.sum(axis=1)[:, np.newaxis]  # Normalize weights

# Compute weighted average for interpolation
vs_interp = np.sum(vs_filtered[indices] * weights, axis=1)

# Reshape interpolated Vs results to match the grid
vs_interp_grid = vs_interp.reshape(xi.shape)

# Set up the plot
plt.figure(figsize=(10, 6))
cmap = 'jet'  # Use the 'jet' colormap
levels = np.linspace(0, 300, 13)  # Divide Vs range (0-300 m/s) into 12 intervals

# Plot interpolated results
contourf = plt.contourf(xi, zi, vs_interp_grid, levels=levels, cmap=cmap, vmin=0, vmax=300)
cbar = plt.colorbar(contourf, label='Vs (m/s)')
cbar.set_ticks(levels)
cbar.set_ticklabels([f"{level:.0f}" for level in levels])

plt.xlabel('Distance (m)')
plt.ylabel('Depth (m)')
plt.title('Smoothed Interpolated Vs Data Using KDTree')

# Get the input file's directory and filename
input_dir = os.path.dirname(input_file)
input_filename = os.path.basename(input_file)

# Save the output image
output_filename = f"{os.path.splitext(input_filename)[0]}_smooth_kdtree_interpolation_{cmap}.png"
output_filepath = os.path.join(input_dir, output_filename)
plt.savefig(output_filepath, dpi=300, bbox_inches='tight')
plt.close()

print("Smoothed interpolated Vs image using KDTree has been saved.")
