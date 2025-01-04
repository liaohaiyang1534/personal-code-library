# -*- encoding: utf-8 -*-
'''
@File        :   batch_pick_dispersion_curves_active_imaging_FJ.py
@Time        :   2025/01/03 22:35:50
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import glob
import subprocess

directory_path = r"F:\SYM\ResultS_line1_15traces_10_tracesinterval_0124-13-19_test\outputImage\H5\2024-01-24"

h5_files = glob.glob(os.path.join(directory_path, "*.h5"))

print(f"Found {len(h5_files)} .h5 files: {h5_files}")

new_directory_path = directory_path + "_disp_curve"
os.makedirs(new_directory_path, exist_ok=True)

for file_path in h5_files:
    try:
        print(f"Processing file: {file_path}")
        result = subprocess.run(
            ["python", r"./pick_dispersion_curves_active_imaging_FJ.py", file_path, new_directory_path],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error processing file {file_path}: {e}")
        print(f"Output: {e.output}")
        print(f"Error output: {e.stderr}")

print("All files have been processed.")
