import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.font_manager import FontProperties, fontManager
from disba import PhaseDispersion, depthplot
from evodcinv import EarthModel, Layer, Curve
import sys
import os
from datetime import datetime
import contextlib
import inspect

# Check if the font file exists
font_path = '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf'
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font file not found: {font_path}")

# Add font path and rebuild font manager
fontManager.addfont(font_path)
font_prop = FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['font.size'] = 9

# Initial velocity model (layer thickness in km, Vs in km/s)
velocity_model = np.array([
    [0.0010, 0.2975, 0.1700, 1.2197],
])

def load_data_and_convert(txt_file):
    data = np.loadtxt(txt_file)
    periods = data[:, 0]
    velocities = data[:, 1]
    modes = data[:, 2]
    if not np.all(modes == 0):
        raise ValueError("All modes must be 0")
    return periods, velocities

# Read data from input file
txt_file = sys.argv[1]
output_dir = sys.argv[2]
timestamp = sys.argv[3]
periods, velocities = load_data_and_convert(txt_file)

print(f"Processing file: {txt_file}")

# Sort periods and velocities
sorted_periods_velocities = sorted(zip(periods, velocities))
periods, velocities = map(np.array, zip(*sorted_periods_velocities))

# Initialize Earth Model
model = EarthModel()

# ---------------------------------------------------------------------------------
# ** Initial Model Setup with Variable Layer Thickness **
initial_velocity = 0.130  # Starting velocity in km/s
final_velocity = 0.400   # Ending velocity in km/s
num_layers = 7           # Number of layers
initial_thickness = 0.001  # Thickness of the first layer (km)
final_thickness = 0.005    # Thickness of the last layer (km)
base_thickness_percent = 0.60
base_velocity_percent = 0.30
depth_threshold = 0.035
enhanced_factor = 35  # Adjustment factor for depths beyond the threshold

velocity_increment = (final_velocity - initial_velocity) / (num_layers - 1)
thickness_increment = (final_thickness - initial_thickness) / (num_layers - 1)
cumulative_depth = 0  # Initialize cumulative depth

# Add layers to the model
for i in range(num_layers):
    thickness = initial_thickness + i * thickness_increment
    velocity = initial_velocity + i * velocity_increment
    cumulative_depth += thickness  # Update cumulative depth

    def adjust_velocity_percent(depth, base_pct, threshold, factor):
        if depth > threshold:
            adjusted_pct = base_pct * (1 - factor * (depth - threshold))
            return max(0.2, adjusted_pct)  # Prevent going below 0.2
        return base_pct

    current_velocity_percent = adjust_velocity_percent(cumulative_depth, base_velocity_percent, depth_threshold, enhanced_factor)
    layer = Layer(
        [thickness * (1 - base_thickness_percent), thickness * (1 + base_thickness_percent)],
        [velocity * (1 - current_velocity_percent), velocity * (1 + current_velocity_percent)]
    )
    model.add(layer)

max_depth = cumulative_depth * 1000  # Convert depth to meters
print(f"Max Depth: {max_depth} m")

# Configure inversion model
model.configure(
    optimizer="cpso",
    misfit="rmse",
    density='nafe-drake',
    optimizer_args={
        "popsize": 30,
        "maxiter": 300,
        "workers": -1,
        "seed": 0,
    },
    increasing_velocity=False,
    normalize_weights=True,
)

# Define dispersion curves
curves = [Curve(np.array(periods), np.array(velocities), mode=0, wave="rayleigh", type="phase", weight=1.0, uncertainties=None)]
res = model.invert(curves, maxrun=1)
res = res.threshold(0.5)

# Save results
res_output_file = os.path.join(output_dir, os.path.basename(txt_file).replace(".txt", f"_res_output_{timestamp}.txt"))
with open(res_output_file, 'w') as f:
    with contextlib.redirect_stdout(f):
        print(res)

# Plot results
fig, ax = plt.subplots(1, 3, figsize=(7, 3.5))
fig.subplots_adjust(wspace=0)  # Adjust spacing between subplots

for a in ax:
    a.grid(False)

zmax = max_depth * 0.001
cmap = "viridis_r"

# Plot velocity model
res.plot_model(
    "vs",
    zmax=zmax,
    show="all",
    ax=ax[0],
    plot_args={"cmap": cmap},
)

res.plot_model(
    "vs",
    zmax=zmax,
    show="best",
    ax=ax[0],
    plot_args={
        "color": "red",
        "linestyle": "--",
        "label": "Best",
    },
)

ax[0].legend(loc=1, frameon=False)
ax[0].text(0.04, 0.03, '(a)', transform=ax[0].transAxes, fontsize=12, verticalalignment='bottom')

# Plot dispersion curve
ax[1].semilogx(1.0 / np.array(periods), velocities * 1000, color="black", linewidth=2, label="True")
res.plot_curve(periods, 0, "rayleigh", "phase", show="best", ax=ax[1], plot_args={"type": "semilogx", "xaxis": "frequency", "color": "red", "linestyle": "--", "label": "Best"})
ax[1].xaxis.set_major_formatter(ScalarFormatter())
ax[1].xaxis.set_minor_formatter(ScalarFormatter())
ax[1].legend(loc=1, frameon=False)
ax[1].text(0.04, 0.03, '(b)', transform=ax[1].transAxes, fontsize=12, verticalalignment='bottom')

# Plot misfit
res.plot_misfit(ax=ax[2])
ax[2].text(0.04, 0.03, '(c)', transform=ax[2].transAxes, fontsize=12, verticalalignment='bottom')

# Save plot
plot_file = os.path.join(output_dir, os.path.basename(txt_file).replace(".txt", f"_{timestamp}.png"))
plt.tight_layout()
fig.savefig(plot_file, bbox_inches='tight', dpi=300)

plt.close(fig)  # Close the figure to free memory
