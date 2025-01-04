# -*- encoding: utf-8 -*-
'''
@File        :   3_dispersion_calculation_array_run_array_and_time_rolling.py
@Time        :   2025/01/03 22:37:18
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''

import subprocess
import os

# Directories containing the data files to be processed
directories = [
    "/mnt/i/diff_dis_to_cavity/2024-06-28_sgy/",
    # "/mnt/i/diff_dis_to_cavity/2024-06-29_sgy/",
    # "/mnt/i/diff_dis_to_cavity/2024-06-30_sgy/",
    # "/mnt/i/diff_dis_to_cavity/2024-07-01_sgy/",
    # "/mnt/i/diff_dis_to_cavity/2024-07-02_sgy/",
    # "/mnt/i/diff_dis_to_cavity/2024-07-03_sgy/",
    # "/mnt/i/diff_dis_to_cavity/2024-07-04_sgy/",
    # "/mnt/i/diff_dis_to_cavity/2024-07-05_sgy/",
]

# File number pairs for processing (e.g., '60x20' to '60x22' represents files from 20:00 to 22:00)
file_number_pairs = [
    ('60x20', '60x22'),
]

# Get the current directory of the script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the script for dispersion calculation
script_path = os.path.join(current_directory, "2_dispersion_calculation_array_run_array_rolling.py")

# Iterate through each directory and file number pair for processing
for directory in directories:
    for start_file_number, end_file_number in file_number_pairs:
        command = ["python3", script_path, start_file_number, end_file_number, directory]
        try:
            print(f"Processing files from {start_file_number} to {end_file_number} in directory {directory}")
            subprocess.run(command, check=True, cwd=directory)
            print(f"Completed processing files from {start_file_number} to {end_file_number} in directory {directory}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while processing files from {start_file_number} to {end_file_number} in directory {directory}: {e}")
