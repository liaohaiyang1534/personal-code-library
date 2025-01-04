# -*- encoding: utf-8 -*-
'''
@File        :   pick_diff_arraylength.py
@Time        :   2025/01/03 22:34:44
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import segyio
import numpy as np
import sys


def extract_array_by_length(file_path, output_dir, array_length_m, trace_spacing):
    trace_count = int(array_length_m // trace_spacing)
    
    with segyio.open(file_path, "r", ignore_geometry=True) as src:
        if trace_count > src.tracecount:
            print(f"The requested array length {array_length_m}m exceeds the number of traces in the file. Skipping.")
            return None

        start_trace = 0
        end_trace = trace_count - 1

        spec = segyio.tools.metadata(src)
        spec.tracecount = trace_count

        new_file_name = f"arraylength_{array_length_m}m_{os.path.basename(file_path)}"
        new_file_path = os.path.join(output_dir, new_file_name)

        with segyio.create(new_file_path, spec) as dst:
            dst.text[0] = src.text[0]
            dst.bin = src.bin

            for i in range(start_trace, end_trace + 1):
                dst.trace[i - start_trace] = src.trace[i]
                dst.header[i - start_trace] = src.header[i]
                dst.header[i - start_trace].update({segyio.TraceField.TRACE_SEQUENCE_LINE: i - start_trace + 1})

    print(f"File saved with array length {array_length_m}m: {new_file_path}")
    print("Output file header information:")
    return new_file_path

def process_traces_for_array_lengths(file_path, min_length, max_length, step_length, trace_spacing):
    base_dir = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.join(base_dir, f"{base_name}_arraylengths")

    os.makedirs(output_dir, exist_ok=True)

    trace_spacing = float(trace_spacing)

    for array_length_m in np.arange(min_length, max_length + step_length, step_length):
        extract_array_by_length(file_path, output_dir, array_length_m, trace_spacing)

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python script.py <file_path> <trace_spacing> <min_length> <max_length> <step_length>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    trace_spacing = float(sys.argv[2])
    min_length = float(sys.argv[3])
    max_length = float(sys.argv[4])
    step_length = float(sys.argv[5])

    print("Input file header information:")

    process_traces_for_array_lengths(file_path, min_length, max_length, step_length, trace_spacing)

    print("Processing complete.")
