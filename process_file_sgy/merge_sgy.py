# -*- encoding: utf-8 -*-
'''
@File        :   merge_sgy.py
@Time        :   2025/01/03 22:50:20
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import segyio
import numpy as np
import os

def find_sgy_files(directory, start_filename, end_filename):
    """
    Find all .sgy files in a specified directory within a range defined by start and end filenames.
    """
    files = [f for f in os.listdir(directory) if f.endswith('.sgy')]
    files.sort()

    try:
        start_index = files.index(start_filename)
        end_index = files.index(end_filename)
    except ValueError as e:
        print(f"Error finding start or end files: {e}")
        return []

    return [os.path.join(directory, f) for f in files[start_index:end_index+1]]

def merge_sgy_files(file_list, output_file):
    """
    Merge multiple SEG-Y files into a single SEG-Y file.
    """
    if not file_list:
        print("No files to merge.")
        return

    # Calculate the total number of traces from all files
    total_traces = 0
    for f in file_list:
        with segyio.open(f, 'r', ignore_geometry=True) as src:
            total_traces += src.tracecount

    # Read specifications from the first file
    with segyio.open(file_list[0], 'r', ignore_geometry=True) as first_file:
        spec = segyio.spec()
        spec.samples = first_file.samples
        spec.format = first_file.format
        spec.tracecount = total_traces  # Set the correct total number of traces

        # Create a new file with the correct specifications
        with segyio.create(output_file, spec) as dst:
            trace_index = 0
            for f in file_list:
                with segyio.open(f, 'r', ignore_geometry=True) as src:
                    for trace in range(src.tracecount):
                        dst.trace[trace_index] = src.trace[trace]
                        dst.header[trace_index].update(src.header[trace])
                        trace_index += 1

            dst.bin.update(first_file.bin)
            dst.text[0] = first_file.text[0]

    print(f"Files merged into {output_file}")

def main():
    """
    Main function to find and merge SEG-Y files.
    """
    directory = r"I:\白蚁114\dat_sgy"
    start_filename = "2024-07-10-01-29-40-out.sgy"
    end_filename = "2024-07-10-01-53-40-out.sgy"
    output_file = r"I:\白蚁114\dat_sgy\merged_output.sgy"
    
    file_list = find_sgy_files(directory, start_filename, end_filename)
    if not file_list:
        print("No files found in the specified range.")
    else:
        merge_sgy_files(file_list, output_file)

if __name__ == "__main__":
    main()
