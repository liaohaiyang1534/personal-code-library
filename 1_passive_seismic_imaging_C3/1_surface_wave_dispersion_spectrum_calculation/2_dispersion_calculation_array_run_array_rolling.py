# -*- encoding: utf-8 -*-
'''
@File        :   2_dispersion_calculation_array_run_array_rolling.py
@Time        :   2025/01/03 22:37:10
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''

import subprocess
import os
import sys
from tqdm import tqdm

data_dir = sys.argv[3]
upper_dir = os.path.dirname(os.path.dirname(data_dir))
inputfolder_name = os.path.basename(os.path.dirname(data_dir))

# Output directory, set output folder's name
result_dir = os.path.join(upper_dir, "RESULTS_LHY_20241201_whole_line1_rolling_8_12marray")

start_file_number = sys.argv[1]
end_file_number = sys.argv[2]

# survey line start channel number and end channel number
line_start = 90  # Channel start
line_end = 203  # Channel end

# Parameters
spacing = 0.5  # Channel spacing in meters
array_length = 12  # Array length in meters
array_interval = 0.5  # Rolling distance in meters, that means, when we move the array, the distance that the array moves
channel_number = array_length / spacing

current_directory = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(current_directory, "1_dispersion_calculation_array_run.py")

jpg_dir = os.path.join(result_dir, "dispersion_jpg/")
dispersion_curve_dir = os.path.join(result_dir, "dispersion_curve/")
dispersion_file_dir = os.path.join(result_dir, "dispersion_file/")

CCFs_C2_dir = os.path.join(result_dir, "CCFs_C2/")
CCFs_C3_compute_dir = os.path.join(result_dir, "CCFs_C3_compute/")
CCFs_C3_plot_dir = os.path.join(result_dir, "CCFs_C3_plot/")
CCFs_ccfj_dir = os.path.join(result_dir, "CCFs_ccfj/")
spectrum_C2_dir = os.path.join(result_dir, "spectrum_C2/")
spectrum_C3_dir = os.path.join(result_dir, "spectrum_C3/")
spectrum_ccfj_dir = os.path.join(result_dir, "spectrum_ccfj/")
curve_C2_dir = os.path.join(result_dir, "curve_C2/")
curve_C3_dir = os.path.join(result_dir, "curve_C3/")
curve_ccfj_dir = os.path.join(result_dir, "curve_ccfj/")

# Create directories if they do not exist
os.makedirs(result_dir, exist_ok=True)
os.makedirs(jpg_dir, exist_ok=True)
os.makedirs(dispersion_curve_dir, exist_ok=True)
os.makedirs(CCFs_C2_dir, exist_ok=True)
os.makedirs(CCFs_C3_compute_dir, exist_ok=True)
os.makedirs(CCFs_C3_plot_dir, exist_ok=True)
os.makedirs(CCFs_ccfj_dir, exist_ok=True)
os.makedirs(spectrum_C2_dir, exist_ok=True)
os.makedirs(spectrum_C3_dir, exist_ok=True)
os.makedirs(spectrum_ccfj_dir, exist_ok=True)
os.makedirs(curve_C2_dir, exist_ok=True)
os.makedirs(curve_C3_dir, exist_ok=True)
os.makedirs(curve_ccfj_dir, exist_ok=True)

step_size = int(array_interval / spacing)

# Loop through the arrays
for array_start in tqdm(range(line_start, line_end, step_size), desc="Processing arrays"):
    array_end = array_start + int(array_length / spacing)
    if array_end > line_end:
        break

    try:
        print(f"Running script: {script_path} with array_start: {array_start}, array_end: {array_end}")
        subprocess.run([
            "python3", script_path,
            data_dir,                    # 1
            jpg_dir,                     # 2
            dispersion_curve_dir,        # 3
            str(spacing),                # 4
            str(array_start),            # 5
            str(array_end),              # 6
            str(start_file_number),      # 7
            str(end_file_number),        # 8
            dispersion_file_dir,         # 9
            CCFs_C2_dir,                 # 10
            CCFs_C3_compute_dir,         # 11
            CCFs_C3_plot_dir,            # 12
            CCFs_ccfj_dir,               # 13
            spectrum_C2_dir,             # 14
            spectrum_C3_dir,             # 15
            spectrum_ccfj_dir,           # 16
            curve_C2_dir,                # 17
            curve_C3_dir,                # 18
            curve_ccfj_dir,              # 19
        ], check=True)
        print("Script ran successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the script: {e}")
