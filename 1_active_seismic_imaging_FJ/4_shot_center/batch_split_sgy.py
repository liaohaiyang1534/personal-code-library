# -*- encoding: utf-8 -*-
'''
@File        :   batch_split_sgy.py
@Time        :   2025/01/03 22:32:44
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import subprocess
import re
import shutil
import segyio
import numpy as np

# Store the paths of each folder and their respective coordinate points
folders_and_coords = {
    r"H:\lhyonedrive\OneDrive\termite\dike\shots_218_257_split_removebad_shottimematch": [(1, 7), (10, 22), (17, 36)],
}

def calculate_a_b(coords):
    """Calculate the coefficients a and b for a linear equation y = ax + b."""
    x = np.array([coord[0] for coord in coords])
    y = np.array([coord[1] for coord in coords])
    A = np.vstack([x, np.ones(len(x))]).T
    a, b = np.linalg.lstsq(A, y, rcond=None)[0]
    return a, b

def calculate_x_middle(value, a, b):
    """Calculate the middle index of seismic traces based on the linear equation."""
    return round(a * value + b)

def reverse_traces(src_filename, dst_filename):
    """Reverse the seismic traces in a SEG-Y file and save the result to a new file."""
    print(f"Reversing traces in {src_filename}")
    try:
        with segyio.open(src_filename, "r", ignore_geometry=True) as src:
            data = segyio.tools.collect(src.trace[:])

            spec = segyio.spec()
            spec.sorting = src.sorting
            spec.format = src.format
            spec.samples = src.samples
            spec.tracecount = len(data)

            reversed_data = data[::-1]

            with segyio.create(dst_filename, spec) as dst:
                dst.trace[:] = reversed_data
                dst.text[0] = src.text[0]
                dst.bin = src.bin

        print(f"Created reversed file: {dst_filename}")
    except Exception as e:
        print(f"Error reversing traces in {src_filename}: {e}")

# Path to the external script for splitting SEG-Y files
script_path = r"H:\lhyonedrive\OneDrive\code_copy\active_source_classification\4_shot_center\split_sgy.py"
problem_files = []

# Process each folder and its respective coordinates
for root_folder, coords in folders_and_coords.items():
    a, b = calculate_a_b(coords)
    parent_folder = os.path.dirname(root_folder)
    output_folder = os.path.join(parent_folder, os.path.basename(root_folder) + "_centersplit")
    left_folder = os.path.join(parent_folder, os.path.basename(root_folder) + "_left")
    right_folder = os.path.join(parent_folder, os.path.basename(root_folder) + "_right")
    left_reverse_folder = os.path.join(parent_folder, os.path.basename(root_folder) + "_left_reverse")

    # Create necessary output directories if they do not exist
    for folder in [output_folder, left_folder, right_folder, left_reverse_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    print(f"Input folder: {root_folder}")
    print(f"Output folder: {output_folder}")
    print(f"Left folder: {left_folder}")
    print(f"Right folder: {right_folder}")
    print(f"Left reversed folder: {left_reverse_folder}")

    # Process each file in the input folder
    for subdir, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".sgy"):
                match = re.search(r'(\d+)-(\d+)_', file)
                if match:
                    try:
                        value = int(match.group(1))
                        x_middle = calculate_x_middle(value, a, b)
                        sgy_file_path = os.path.join(subdir, file)
                        print(f"Processing file: {sgy_file_path}, calculated middle trace index: {x_middle}")
                        print(f"Calling script: python {script_path} {sgy_file_path} {str(x_middle)} {output_folder}")
                        result = subprocess.run(["python", script_path, sgy_file_path, str(x_middle), output_folder], capture_output=True, text=True)
                        print(result.stdout)
                        if result.stderr:
                            print(f"Error in split_sgy.py: {result.stderr}")

                        base_name = os.path.splitext(file)[0]
                        left_sgy_path = os.path.join(output_folder, f"{base_name}_left.sgy")
                        right_sgy_path = os.path.join(output_folder, f"{base_name}_right.sgy")

                        # Copy and reverse traces for left and right output files
                        if os.path.exists(left_sgy_path):
                            shutil.copy(left_sgy_path, left_folder)
                            reversed_left_sgy_path = os.path.join(left_reverse_folder, f"{base_name}_left_reversed.sgy")
                            reverse_traces(left_sgy_path, reversed_left_sgy_path)

                        if os.path.exists(right_sgy_path):
                            shutil.copy(right_sgy_path, right_folder)
                    except Exception as e:
                        print(f"Error processing file {sgy_file_path}: {e}")
                        problem_files.append(sgy_file_path)

    # Create an _ALL folder and copy contents from _right and _left_reverse folders
    all_folder = os.path.join(parent_folder, os.path.basename(root_folder) + "_ALL")

    if not os.path.exists(all_folder):
        os.makedirs(all_folder)

    # Copy contents from _right folder to _ALL folder
    for root, dirs, files in os.walk(right_folder):
        for file in files:
            shutil.copy(os.path.join(root, file), all_folder)

    # Copy contents from _left_reverse folder to _ALL folder
    for root, dirs, files in os.walk(left_reverse_folder):
        for file in files:
            shutil.copy(os.path.join(root, file), all_folder)

    print(f"All files have been successfully copied to: {all_folder}")

# Print the list of problematic files
if problem_files:
    print("\nProblematic files:")
    for problem_file in problem_files:
        print(problem_file)
