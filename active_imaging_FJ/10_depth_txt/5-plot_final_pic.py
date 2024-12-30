import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os
import sys
from matplotlib.ticker import FuncFormatter

# Set font style and size
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 8

# Load data
input_file = sys.argv[1]
data = np.loadtxt(input_file)

# Extract columns
x = data[:, 0]  # First column: x (m)
z = data[:, 1]  # Second column: z (m)
vs = data[:, 2]  # Third column: Vs (m/s)

# Create interpolation grid
xi = np.linspace(min(x), max(x), 1000)
zi = np.linspace(min(z), max(z), 1000)
xi, zi = np.meshgrid(xi, zi)

# Perform cubic interpolation
vs_interp_grid = griddata((x, z), vs, (xi, zi), method='cubic')

# Set up the plot
plt.figure(figsize=(6, 12))
ax = plt.gca()

# Adjust aspect ratio
ax.set_aspect(2)

cmap = 'jet'

# Determine maximum value of Vs for contour levels
vs_max = np.max(vs)  # Fetches maximum value from the Vs data
levels = np.linspace(0, vs_max, 100)  # Generate 100 levels from 0 to maximum Vs value

# Plot interpolation results
contourf = plt.contourf(xi, zi, vs_interp_grid, levels=levels, cmap=cmap, vmin=0, vmax=vs_max)
cbar = plt.colorbar(contourf, label='Vs (m/s)', shrink=0.06, aspect=10)
cbar.set_ticks(np.arange(0, vs_max + 1, 100))
cbar.set_ticklabels([f"{tick:.0f}" for tick in np.arange(0, vs_max + 1, 100)])

# Calculate x-axis range
x_min = min(x)
x_max = max(x)

# Define custom tick formatter for x-axis
def custom_x_ticks(x, pos):
    """Show x-ticks only if x is a multiple of 5 or is the range's min/max value."""
    if x == x_min or x == x_max or x % 5 == 0:
        return f'{x:.0f}'
    return ''

# Apply custom tick formatter to x-axis
ax.xaxis.set_major_formatter(FuncFormatter(custom_x_ticks))

plt.xlabel('Trace')
plt.ylabel('Depth (m)')

# Invert y-axis to show depth increasing downward
ax.invert_yaxis()

# Invert x-axis
ax.invert_xaxis()

# Save the figure
input_dir = os.path.dirname(input_file)
input_filename = os.path.basename(input_file)
output_filename = f"{os.path.splitext(input_filename)[0]}_cubic_interpolation_{cmap}.png"
output_filepath = os.path.join(input_dir, output_filename)
plt.savefig(output_filepath, dpi=300, bbox_inches='tight')
plt.close()

print("Cubic interpolation result image has been saved.")
