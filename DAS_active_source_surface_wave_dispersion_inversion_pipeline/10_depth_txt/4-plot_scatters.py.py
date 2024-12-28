import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KDTree
import os
import sys
from joblib import Parallel, delayed

# Set plot font style
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 9

# Input file from command-line argument
input_file = sys.argv[1]

# Load data
data = np.loadtxt(input_file)

# Extract column data
x = data[:, 0]  # First column: x (Trace)
z = data[:, 1]  # Second column: z (Depth in meters)
vs = data[:, 2]  # Third column: Vs (m/s)

# Display basic statistics of Vs data
print("Basic statistics for Vs data:")
print(f"Minimum: {np.min(vs)}")
print(f"Maximum: {np.max(vs)}")
print(f"Mean: {np.mean(vs)}")
print(f"Standard Deviation: {np.std(vs)}")

# Create grid for visualization (if needed in future interpolation)
xi = np.linspace(min(x), max(x), 1000)
zi = np.linspace(min(z), max(z), 1000)
xi, zi = np.meshgrid(xi, zi)

# Define colormap and color levels
cmap = 'jet'
levels = 100

# Get input file's directory and filename
input_dir = os.path.dirname(input_file)
input_filename = os.path.basename(input_file)

# Compute global min and max values of Vs for consistent color mapping
vs_min = np.min(vs)
vs_max = np.max(vs)
vmin, vmax = vs_min, vs_max  # Ensure consistent colorbar range

# Plot scatter of original data points
plt.figure(figsize=(6, 12))
ax = plt.gca()  # Get current axis object
ax.set_aspect('equal')  # Set aspect ratio to equal

scatter = plt.scatter(x, z, c=vs, cmap=cmap, vmin=vmin, vmax=vmax)
cbar = plt.colorbar(scatter, label='Vs (m/s)', shrink=0.06, aspect=10)
plt.xlabel('Trace')
plt.ylabel('Depth (m)')
plt.title('Original Data Points')
ax.invert_yaxis()  # Invert y-axis to show depth descending

# Save scatter plot
scatter_output_filename = f"{os.path.splitext(input_filename)[0]}_scatter_{cmap}.png"
scatter_output_filepath = os.path.join(input_dir, scatter_output_filename)
plt.savefig(scatter_output_filepath, dpi=300, bbox_inches='tight')
plt.close()

print("Scatter plot of original data points has been saved.")
