# -*- encoding: utf-8 -*-
'''
@File        :   pick_diff_offset_2.py
@Time        :   2025/01/03 22:34:50
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import segyio
import shutil
import os
import sys
import numpy as np
import re

def remove_traces_by_offset(file_path, output_dir, offset_meters, trace_spacing, current_min_offset):
    traces_to_remove = int(offset_meters / trace_spacing)

    with segyio.open(file_path, "r", ignore_geometry=True) as src:
        if traces_to_remove >= src.tracecount:
            print(f"Offset {offset_meters}m results in removing all traces. Skipping.")
            return None

        # Prepare specifications for the new SEGY file
        spec = segyio.spec()
        spec.sorting = src.sorting
        spec.format = src.format
        spec.samples = src.samples
        spec.tracecount = src.tracecount - traces_to_remove

        new_file_name = f"offset_minoff_{offset_meters}m_{os.path.basename(file_path)}"
        new_file_path = os.path.join(output_dir, new_file_name)

        with segyio.create(new_file_path, spec) as dst:
            for i in range(traces_to_remove, src.tracecount):
                # Calculate new GroupX coordinate
                new_group_x = current_min_offset + (i + 1) * trace_spacing  # Assuming units are meters
                new_group_x = new_group_x

                dst.header[i - traces_to_remove] = src.header[i]
                dst.header[i - traces_to_remove][segyio.TraceField.GroupX] = int(new_group_x)
                dst.trace[i - traces_to_remove] = src.trace[i]

    print(f"File saved with minimum offset {offset_meters}m: {new_file_path}")
    return new_file_path

def process_traces_for_offsets(file_path, min_offset, max_offset, trace_spacing, current_min_offset, add_gap):
    # Extract the file name from the file path
    file_name = os.path.basename(file_path)

    # Use a regex to extract trace spacing from the file name
    match = re.search(r'(\d+(?:\.\d+)?)m_', file_name)
    if match:
        trace_spacing = float(match.group(1))
        print(f"Extracted trace spacing: {trace_spacing}m")
    else:
        print("Could not extract trace spacing from file name.")
        return  # Stop processing if trace spacing cannot be extracted

    # Ensure all parameters are converted to floats
    min_offset = float(min_offset)
    max_offset = float(max_offset)
    trace_spacing = float(trace_spacing)
    current_min_offset = float(current_min_offset)

    base_dir = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.join(base_dir, f"{base_name}_diffoffset")

    os.makedirs(output_dir, exist_ok=True)

    print(f"Source file copied to {output_dir}")

    for offset_meters in np.arange(min_offset, max_offset + 1, trace_spacing * add_gap):
        remove_traces_by_offset(file_path, output_dir, offset_meters, trace_spacing, current_min_offset)

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Usage: python script.py <file_path> <trace_spacing> <min_offset> <max_offset> <current_min_offset> <add_gap>")
        sys.exit(1)

    file_path = sys.argv[1]
    trace_spacing = float(sys.argv[2])
    min_offset = sys.argv[3]
    max_offset = sys.argv[4]
    current_min_offset = sys.argv[5]
    add_gap = float(sys.argv[6])

    process_traces_for_offsets(file_path, min_offset, max_offset, trace_spacing, current_min_offset, add_gap)
