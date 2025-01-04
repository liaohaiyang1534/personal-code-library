# -*- encoding: utf-8 -*-
'''
@File        :   pick_diff_trace_spacing.py
@Time        :   2025/01/03 22:34:55
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import sys

# Print the path to the current Python executable
print("Python Executable Path:", sys.executable)

# Print the version of Python
print("Python Version:", sys.version)

import segyio
from segyio import TraceField
import shutil
import os
import numpy as np

def resample_traces(file_path, output_dir, trace_spacing_m, spacing_now):
    with segyio.open(file_path, "r", ignore_geometry=True) as src:
        sample_interval = round(trace_spacing_m / spacing_now)
        spec = segyio.spec()
        spec.sorting = src.sorting
        spec.format = src.format
        spec.samples = src.samples
        spec.tracecount = int(len(src.trace) / sample_interval)

        new_file_name = f"spacing_{trace_spacing_m}m_{os.path.basename(file_path)}"
        new_file_path = os.path.join(output_dir, new_file_name)

        with segyio.create(new_file_path, spec) as dst:
            start_group_x = 0
            for i in range(spec.tracecount):
                current_group_x = start_group_x + (i + 1) * trace_spacing_m
                dst.header[i] = src.header[i * sample_interval]
                dst.header[i][TraceField.GroupX] = int(current_group_x)  # Assuming meters to millimeters conversion
                dst.trace[i] = src.trace[i * sample_interval]

    print(f"File saved with {trace_spacing_m}m trace spacing: {new_file_path}")
    return new_file_path

def process_traces_for_spacing(file_path, spacings, spacing_now):
    base_name, _ = os.path.splitext(os.path.basename(file_path))
    output_dir = os.path.join(os.path.dirname(file_path), base_name)
    os.makedirs(output_dir, exist_ok=True)

    for spacing in spacings:
        resample_traces(file_path, output_dir, spacing, spacing_now)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <file_path> <spacing_now> <desired_spacings>")
        sys.exit(1)

    file_path = sys.argv[1]
    spacing_now = float(sys.argv[2])
    desired_spacings = [float(x) for x in sys.argv[3].split(',')]

    process_traces_for_spacing(file_path, desired_spacings, spacing_now)
