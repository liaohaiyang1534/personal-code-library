# -*- encoding: utf-8 -*-
'''
@File        :   inversion.py
@Time        :   2025/01/03 22:41:35
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
@Description :   This script uses the 'evodcinv' package to perform surface wave dispersion curve inversion using evolutionary algorithms.
                 The inversion is applied to phase velocity dispersion data, specifically for Rayleigh waves. The model is constructed 
                 using multiple layers with specified boundaries for thickness and S-wave velocity. The evolutionary algorithm (CPOS) 
                 is used to optimize the model parameters. The script processes input dispersion data, performs inversion, saves the 
                 results, and generates graphical outputs of the best model fit and comparison with the true data.
'''

from evodcinv import EarthModel, Layer, Curve
from evodcinv import factory

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.font_manager import FontProperties, fontManager
from matplotlib.ticker import FormatStrFormatter, MultipleLocator
from disba import PhaseDispersion, depthplot
import evodcinv
import sys
import os
from datetime import datetime

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
    # Load data using a comma as the delimiter
    data = np.loadtxt(txt_file, delimiter=',')
    if data.shape[1] == 2:  # If there are two columns: frequency and velocity
        frequency = data[:, 0]
        velocity_ms = data[:, 1]
        modes = np.zeros(len(frequency), dtype=int)  # Default modes to 0 if not provided
    elif data.shape[1] > 2:  # If a third column exists, treat it as modes
        frequency = data[:, 0]
        velocity_ms = data[:, 1]
        modes = data[:, 2]
    else:
        raise ValueError("Data format error: Expected at least two columns.")
    
    periods = 1 / frequency
    velocity_kms = velocity_ms / 1000  # Convert to km/s
    
    return periods, velocity_kms, modes

# Command-line arguments
txt_file = sys.argv[1]
output_dir = sys.argv[2]
output_best_model_res_dir = sys.argv[3]
output_best_model_dir = sys.argv[4]
output_models_jpg_dir = sys.argv[5]

# Load data and process
periods, velocities, modes = load_data_and_convert(txt_file)
print(f"Processing file: {txt_file}")
sorted_periods_velocities = sorted(zip(periods, velocities))
periods, velocities = map(np.array, zip(*sorted_periods_velocities))

# ----------------------------------------------------------------------------------
# Model initialization
# ----------------------------------------------------------------------------------
model = EarthModel()
model.add(Layer([0.003, 0.003], [0.01, 0.60]))
model.add(Layer([0.004, 0.004], [0.01, 0.60]))
model.add(Layer([0.005, 0.005], [0.01, 0.60]))
model.add(Layer([0.006, 0.006], [0.01, 0.60]))
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
# Inversion
# ----------------------------------------------------------------------------------
print(np.array(periods))
print(np.array(velocities))

curves = [Curve(np.array(periods), np.array(velocities), mode=0, wave="rayleigh", type="phase", weight=1.0, uncertainties=None)]
res = model.invert(curves, maxrun=1)
res = res.threshold(0.99)

# ----------------------------------------------------------------------------------
# Save best model results
# ----------------------------------------------------------------------------------
import contextlib

res_output_file = os.path.join(output_best_model_res_dir, os.path.basename(txt_file).replace(".txt", f".txt"))
with open(res_output_file, 'w') as f:
    with contextlib.redirect_stdout(f):
        print(res)

# ----------------------------------------------------------------------------------
# Save best model data
# ----------------------------------------------------------------------------------
import io

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

show_min_velocity = res_min_velocity - (res_max_velocity - res_min_velocity) * 0.1
if show_min_velocity < 0:
    show_min_velocity = res_min_velocity * 0.5
show_max_velocity = res_max_velocity + (res_max_velocity - res_min_velocity) * 0.1

fig, ax = plt.subplots(1, 2, figsize=(6, 4))
plt.subplots_adjust(wspace=0.3)

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
import copy
final_model = copy.deepcopy(res.models[np.argmin(res.misfits)])
pd = PhaseDispersion(*final_model.T, dc=0.001)

for mode, color in zip(range(4), ['k', 'green', 'blue', 'orange']):
    cpr_pred = [pd(t, mode=mode, wave="rayleigh")]
    ax[1].plot(1.0 / cpr_pred[0].period, cpr_pred[0].velocity, color=color, label=f"R{mode}", linewidth=1)

ax[1].legend(loc=1, frameon=False)
ax[1].tick_params(direction='in', length=2, width=1)
ax[1].set_xlabel("Frequency (Hz)")
ax[1].set_ylabel("Phase velocity (m/s)")
ax[1].grid(True, linestyle='-', linewidth=0.08, color='gray')
ax[1].set_xlim([1, 50])

plot_file = os.path.join(output_models_jpg_dir, os.path.basename(txt_file).replace(".txt", f".jpg"))
if not plot_file.endswith(('.jpg', '.jpeg', '.png', '.tif', '.tiff')):
    plot_file += '.jpg'

fig.savefig(plot_file, bbox_inches='tight', dpi=300)
plt.close(fig)
# ----------------------------------------------------------------------------------
# THE END
# ----------------------------------------------------------------------------------
