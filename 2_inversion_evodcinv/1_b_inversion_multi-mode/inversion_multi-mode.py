# -*- encoding: utf-8 -*-
'''
@File        :   inversion_multi-mode.py
@Time        :   2025/01/03 22:41:47
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
@Description :   This script uses the 'evodcinv' package to perform surface wave dispersion curve inversion using evolutionary algorithms.
                 The inversion is applied to phase velocity dispersion data, specifically for Rayleigh waves. The model is constructed 
                 using multiple layers with specified boundaries for thickness and S-wave velocity. The evolutionary algorithm (CPOS) 
                 is used to optimize the model parameters. The script processes input dispersion data, performs inversion, saves the 
                 results, and generates graphical outputs of the best model fit and comparison with the true data.
'''


import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.font_manager import FontProperties, fontManager
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import MultipleLocator
from disba import PhaseDispersion, depthplot
from evodcinv import EarthModel, Layer, Curve
import evodcinv
import sys
import os
from datetime import datetime
from evodcinv import factory
import contextlib
import io

# ----------------------------------------------------------------------------------
# Font settings
# ----------------------------------------------------------------------------------
font_path = '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf'
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font file not found: {font_path}")
fontManager.addfont(font_path)
font_prop = FontProperties(fname=font_path, size=8)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['font.size'] = 8

# ----------------------------------------------------------------------------------
# Data loading and conversion
# ----------------------------------------------------------------------------------
def load_data_and_convert(txt_file):
    # Read data using comma as the delimiter
    data = np.loadtxt(txt_file, delimiter=',')

    if data.shape[1] == 2:  # Two columns: periods and velocities
        frequency = data[:, 0]
        velocity_ms = data[:, 1]
        modes = np.zeros(len(frequency), dtype=int)  # Default modes to 0 if not present
    elif data.shape[1] > 2:  # If third column exists, extract as modes
        frequency = data[:, 0]
        velocity_ms = data[:, 1]
        modes = data[:, 2].astype(int)
    else:
        raise ValueError("Data format error: At least two columns expected.")

    periods = 1 / frequency
    velocity_kms = velocity_ms / 1000

    return periods, velocity_kms, modes

# Command line arguments
txt_file = sys.argv[1]
output_dir = sys.argv[2]
output_best_model_res_dir = sys.argv[3]
output_best_model_dir = sys.argv[4]
output_models_jpg_dir = sys.argv[5]

# Load and process data
periods, velocities, modes = load_data_and_convert(txt_file)
print(f"Processing file: {txt_file}")

# Store periods and velocities by modes
mode_periods = {}
mode_velocities = {}

for mode in np.unique(modes):
    mask = modes == mode
    mode_periods[mode] = periods[mask]
    mode_velocities[mode] = velocities[mask]

if 0 in mode_periods:
    periods0 = mode_periods[0]
    velocities0 = mode_velocities[0]
else:
    periods0, velocities0 = None, None

if 1 in mode_periods:
    periods1 = mode_periods[1]
    velocities1 = mode_velocities[1]
else:
    periods1, velocities1 = None, None

if 2 in mode_periods:
    periods2 = mode_periods[2]
    velocities2 = mode_velocities[2]
else:
    periods2, velocities2 = None, None

if 3 in mode_periods:
    periods3 = mode_periods[3]
    velocities3 = mode_velocities[3]
else:
    periods3, velocities3 = None, None

print("Periods and Velocities based on Modes:")
if periods0 is not None and velocities0 is not None:
    print(f"periods0: {periods0}, velocities0: {velocities0}")
if periods1 is not None and velocities1 is not None:
    print(f"periods1: {periods1}, velocities1: {velocities1}")
if periods2 is not None and velocities2 is not None:
    print(f"periods2: {periods2}, velocities2: {velocities2}")
if periods3 is not None and velocities3 is not None:
    print(f"periods3: {periods3}, velocities3: {velocities3}")

# ----------------------------------------------------------------------------------
# Model initialization
# ----------------------------------------------------------------------------------
model = EarthModel()
model.add(Layer([0.001, 0.005], [0.01, 0.60]))
model.add(Layer([0.001, 0.005], [0.01, 0.60]))
model.add(Layer([0.001, 0.005], [0.01, 0.60]))
model.add(Layer([0.001, 0.005], [0.01, 0.60]))
model.add(Layer([0.001, 0.005], [0.01, 0.60]))
model.add(Layer(1.0, [0.1, 1.0]))

# ----------------------------------------------------------------------------------
# Configuring the inversion
# ----------------------------------------------------------------------------------
model.configure(
    optimizer="cpso",
    misfit="rmse",
    density=lambda vp: 2.0,
    optimizer_args={"popsize": 500, "maxiter": 200, "workers": -1, "seed": 100},
    increasing_velocity=True,
    normalize_weights=True,
    dc=0.001,
    dt=0.01,
)

# ----------------------------------------------------------------------------------
# Inverting
# ----------------------------------------------------------------------------------
periods0 = periods0[::-1]
velocities0 = velocities0[::-1]
curves = [Curve(np.array(periods0), np.array(velocities0), mode=0, wave="rayleigh", type="phase")]

res = model.invert(curves, maxrun=1)
res = res.threshold(0.99)

# ----------------------------------------------------------------------------------
# Output: Best model results
# ----------------------------------------------------------------------------------
res_output_file = os.path.join(output_best_model_res_dir, os.path.basename(txt_file).replace(".txt", f".txt"))
with open(res_output_file, 'w') as f:
    with contextlib.redirect_stdout(f):
        print(res)

with open(res_output_file, 'r') as f:
    lines = f.readlines()

second_last_line = lines[-2].strip()
match = re.search(r"Best model misfit:\s*([\d\.]+)", second_last_line)
if match:
    misfit_value = match.group(1)
    print(f"Best model misfit: {misfit_value}")
else:
    print("Could not find 'Best model misfit' value")

# ----------------------------------------------------------------------------------
# Output: Best model data
# ----------------------------------------------------------------------------------
output_buffer = io.StringIO()
with contextlib.redirect_stdout(output_buffer):
    print(res)
res_output = output_buffer.getvalue()
lines = res_output.split('\n')
processed_lines = lines[8:-6]
filtered_lines = []
depth = 0.0
first_vs = 0.0

for index, line in enumerate(processed_lines):
    columns = line.split()
    if len(columns) >= 3:
        thickness = float(columns[0])
        depth += thickness
        if index == 0:
            first_vs = float(columns[2])
        filtered_lines.append(f"{depth:.4f}\t{float(columns[2]):.4f}\n")
filtered_lines.insert(0, f"0.0000\t{first_vs:.4f}\n")
last_line = filtered_lines[-1].split('\t')
last_line[0] = "1.0000"
filtered_lines[-1] = '\t'.join(last_line)
output_file_path = os.path.join(output_best_model_dir, os.path.basename(txt_file).replace(".txt", ".txt"))

with open(output_file_path, 'w') as f:
    f.writelines(filtered_lines)

# ----------------------------------------------------------------------------------
# Plotting
# ----------------------------------------------------------------------------------
penultimate_line = filtered_lines[-2].split('\t')
penultimate_depth_value = float(penultimate_line[0])
show_max_depth = penultimate_depth_value * 1.2

res_velocities = [float(line.split('\t')[1]) for line in filtered_lines]
res_min_velocity = min(res_velocities)
res_max_velocity = max(res_velocities)
show_min_velocity = max(0, res_min_velocity - (res_max_velocity - res_min_velocity) * 0.1)
show_max_velocity = res_max_velocity + (res_max_velocity - res_min_velocity) * 0.1

fig, ax = plt.subplots(1, 2, figsize=(6, 4))
plt.subplots_adjust(wspace=0.3)
for a in ax:
    a.grid(True, linestyle=":")

zmax = show_max_depth
cmap = "viridis_r"

res.plot_model("vs", zmax=zmax, show="all", stride=100, ax=ax[0], plot_args={"cmap": cmap, "linewidth": 1})
res.plot_model("vs", zmax=zmax, show="best", ax=ax[0], plot_args={"color": "red", "linestyle": "--", "label": "Best", "linewidth": 1})
ax[0].tick_params(direction='in', length=2, width=1)
ax[0].grid(True, linestyle='-', linewidth=0.08, color='gray')
ax[0].set_xlabel("S-wave velocity (m/s)")
ax[0].set_ylabel("Depth (m)")
ax[0].set_xlim([show_min_velocity, show_max_velocity])

ax[1].scatter(1.0 / np.array(periods), velocities, color="red", label="True", s=5)
t = np.sort(1.0 / np.linspace(1, 50, 100))
final_model = copy.deepcopy(res.models[np.argmin(res.misfits)])
pd = PhaseDispersion(*final_model.T, dc=0.001)
cpr_pred = [pd(t, mode=0, wave="rayleigh")]
ax[1].plot(1.0 / cpr_pred[0].period, cpr_pred[0].velocity, color='k', label="R0", linewidth=1)

ax[1].legend(loc=1, frameon=False)
ax[1].tick_params(direction='in', length=2, width=1)
ax[1].set_xlabel("Frequency (Hz)")
ax[1].set_ylabel("Phase velocity (m/s)")
ax[1].grid(True, linestyle='-', linewidth=0.08, color='gray')
ax[1].set_xlim([1, 50])
ax[1].set_ylim([0.1, 0.6])

plot_file = os.path.join(output_models_jpg_dir, os.path.basename(txt_file).replace(".txt", f"_misfit_{misfit_value}.jpg"))
fig.savefig(plot_file, bbox_inches='tight', dpi=300)
plt.close(fig)
# ----------------------------------------------------------------------------------
# THE END
# ----------------------------------------------------------------------------------
