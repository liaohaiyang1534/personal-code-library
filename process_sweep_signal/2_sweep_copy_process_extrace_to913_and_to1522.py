# -*- encoding: utf-8 -*-
'''
@File        :   2_sweep_copy_process_extrace_to913_and_to1522.py
@Time        :   2025/01/03 22:51:44
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import segyio
import os
import re
import sys

# Accept directory path from command line
if len(sys.argv) > 1:
    root_folder = sys.argv[1]
else:
    print("Error: No directory path provided.")
    sys.exit(1)

print(f"Processing directory: {root_folder}")

def extract_numbers_from_parent_folder_name(folder_path):
    parent_folder_name = os.path.basename(os.path.dirname(folder_path))
    return re.findall(r'\d+', parent_folder_name)

def copy_trace_range(src_filename, dst_filename, start_trace, end_trace):
    with segyio.open(src_filename, "r", ignore_geometry=True) as src:
        if start_trace < 1 or end_trace > src.tracecount:
            print(f"Invalid trace range. File contains {src.tracecount} traces.")
            return

        spec = segyio.tools.metadata(src)
        spec.tracecount = end_trace - start_trace + 1

        with segyio.create(dst_filename, spec) as dst:
            dst.text[0] = src.text[0]
            dst.bin = src.bin

            for i in range(start_trace - 1, end_trace):
                dst.trace[i - start_trace + 1] = src.trace[i]
                dst.header[i - start_trace + 1] = src.header[i]
                dst.header[i - start_trace + 1].update({segyio.TraceField.TRACE_SEQUENCE_LINE: i - start_trace + 2})

        print(f"Copied traces {start_trace} to {end_trace} from {src_filename} to {dst_filename}.")

def process_sgy_file(sgy_file_path, x1, x2):

    grandfather_folder_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(sgy_file_path))))
    shot_number = re.findall(r'\d+', grandfather_folder_name)
    shot_number = int(shot_number[0])

    shot_trace_index = int(int(shot_number * 6 / 1.014) - (shot_number - 28) * 0.1129)

    shot_trace_index = shot_trace_index + 0.14814815 * shot_number - 0.44444444

    shot_trace_index = int(shot_trace_index)

    print(f"Calculated shot_trace_index: {shot_trace_index} for shot number: {shot_number}")

    with segyio.open(sgy_file_path, "r", ignore_geometry=True) as src:
        total_traces = src.tracecount
        print(f"Total traces in file: {total_traces}")

    start_trace = 1
    end_trace = total_traces  # Use total number of traces in the file as the end_trace

    path = os.path.dirname(sgy_file_path)
    new_name = f"to_1028.sgy"
    to_1028_name = os.path.join(path, new_name)
    copy_trace_range(sgy_file_path, to_1028_name, start_trace, shot_trace_index)

    new_name = f"to_1267.sgy"
    to_1267_name = os.path.join(path, new_name)
    copy_trace_range(sgy_file_path, to_1267_name, shot_trace_index, end_trace)

def process_folder(root_folder, max_depth, x1, x2, x0):
    for subdir, dirs, files in os.walk(root_folder):
        if subdir.count(os.sep) - root_folder.count(os.sep) >= max_depth:
            continue
        for file in files:
            if file.endswith("correlated_after_zero.sgy"):
                original_file_path = os.path.join(subdir, file)
                process_sgy_file(original_file_path, x1, x2)

# Main logic
max_depth = 4
x1 = 1028
x2 = 1280
x0 = 100  # Adjust as needed

process_folder(root_folder, max_depth, x1, x2, x0)
