#!/bin/bash

# -*- encoding: utf-8 -*-
'''
@File        :   3_process_single.sh
@Time        :   2025/01/03 22:40:25
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


set -x

script_to_run="./process_single_disp.sh"  # Script to run
files_to_move=("modl.out" "I.PLT" "T.PLT" "IT.PLT" "SRFPHV96.PLT" "disp.d" "modl.d" "figsrf1.eps" "figsrf2.eps" "figsrf1.png" "figsrf2.png")

# Get parameters
disp_file="$1"
output_dir=$2
timeout_duration="$3"

echo "Processing file $disp_file"

# Ensure the output directory exists
if [ ! -d "${output_dir}" ]; then
    mkdir -p "${output_dir}"
    echo "${output_dir} directory has been created."
fi

# Check if the dispersion file exists
if [ ! -f "${disp_file}" ]; then
    echo "File ${disp_file} does not exist."
    exit 1
fi

# Ensure disp.d and modl.d exist
if [ ! -f "disp.d" ] || [ ! -f "modl.d" ]; then
    echo "disp.d or modl.d file does not exist."
    exit 1
fi

# Output the contents of disp.d and modl.d
echo "Contents of disp.d:"
cat disp.d

echo "Contents of modl.d:"
cat modl.d

# Execute the script with a timeout and capture the output
timeout $timeout_duration $script_to_run
exit_status=$?

# Check the return code of the script
if [ $exit_status -ne 0 ]; then
    if [ $exit_status -eq 124 ]; then
        echo "$script_to_run script timed out."
    else
        echo "$script_to_run script execution failed."
    fi
    exit 1
fi

# Check the script output for floating-point exception
if timeout $timeout_duration $script_to_run 2>&1 | grep -q "floating-point exceptions"; then
    echo "Inversion failed, floating-point exception detected."
    exit 1
fi

# Move files to the output directory
for file in "${files_to_move[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" "${output_dir}/"
        echo "$file has been copied to ${output_dir}/"
    else
        echo "$file does not exist and cannot be copied."
    fi
done
