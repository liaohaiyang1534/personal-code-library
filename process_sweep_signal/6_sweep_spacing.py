# -*- encoding: utf-8 -*-
'''
@File        :   6_sweep_spacing.py
@Time        :   2025/01/03 22:52:13
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import segyio
import os
import numpy as np
import sys

# Accept root_folder and trace_spacing_m from command-line arguments
root_folder = sys.argv[1]
trace_spacing_m = float(sys.argv[2])  # Assume trace_spacing_m is a floating-point number

print(f"Processing directory: {root_folder}")
print(f"Trace spacing (meters): {trace_spacing_m}")

def resample_traces(file_path, output_dir, trace_spacing_m):
    """Resample traces in a SEGY file to a specified trace spacing."""
    with segyio.open(file_path, "r", ignore_geometry=True) as src:
        # Calculate sample interval based on desired trace spacing and assumed velocity
        sample_interval = int(round(trace_spacing_m / 0.5))

        data = segyio.tools.collect(src.trace[::sample_interval])

        spec = segyio.spec()
        spec.sorting = src.sorting
        spec.format = src.format
        spec.samples = src.samples
        spec.tracecount = len(data)

        new_file_name = f"{trace_spacing_m}m_{os.path.basename(file_path)}"
        new_file_path = os.path.join(output_dir, new_file_name)

        with segyio.create(new_file_path, spec) as dst:
            dst.trace[:] = data

    print(f"File saved with {trace_spacing_m}m trace spacing: {new_file_path}")
    return new_file_path

def process_sgy_file(sgy_file_path, trace_spacing_m):
    """Process a single SEGY file."""
    output_dir = os.path.dirname(sgy_file_path)
    resample_traces(sgy_file_path, output_dir, trace_spacing_m)

def process_folder(root_folder, max_depth, trace_spacing_m):
    """Process specific SEGY files in a folder and its subfolders based on exact names."""
    for subdir, dirs, files in os.walk(root_folder):
        if subdir.count(os.sep) - root_folder.count(os.sep) >= max_depth:
            continue
        for file in files:
            if file == "1028.sgy" or file == "1267.sgy":
                original_file_path = os.path.join(subdir, file)
                process_sgy_file(original_file_path, trace_spacing_m)

# Main logic
max_depth = 4
process_folder(root_folder, max_depth, trace_spacing_m)
