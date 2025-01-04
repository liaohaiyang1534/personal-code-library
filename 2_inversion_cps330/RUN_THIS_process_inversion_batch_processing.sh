#!/bin/bash

# -*- encoding: utf-8 -*-
'''
@File        :   RUN_THIS_process_inversion_batch_processing.sh
@Time        :   2025/01/03 22:41:02
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
@Description :   This script is modified based on the work from Dr. R. B. Herrmann "Computer Programs in Seismology" (Version 3.30, last updated Apr-25-2024). The original programs can be downloaded from: http://www.eas.slu.edu/eqc/eqc_cps/CPS330.html
'''

# This is based on CPS330 (https://www.eas.slu.edu/eqc/eqc_cps/getzip.html)

set -x

# Currently only supports inversion of Rayleigh wave fundamental mode dispersion curves.
# It can also invert Love waves and higher modes by modifying the script accordingly.

# Since some dispersion curve inversions may not always run successfully and could hang,
# set a timeout to skip to the next curve if the inversion exceeds this time.

timeout_duration=60s  # Set timeout duration to 60 seconds

curve_dir="./curve_input"

input_dir="./curve_input_adjustedtocps"
if [ -d "${input_dir}" ]; then
    rm -rf "${input_dir}"/*
    echo "${input_dir} directory has been cleared."
else
    mkdir -p "${input_dir}"
    echo "${input_dir} directory has been created."
fi

python 5_txt_adjustedtocps.py "${curve_dir}"

# Custom settings
output_dir="./output_temp"
final_output_dir="./outputtoday/output"

# Clear output directory
if [ -d "${output_dir}" ]; then
    rm -rf "${output_dir}"/*
    echo "${output_dir} directory has been cleared."
else
    mkdir -p "${output_dir}"
    echo "${output_dir} directory has been created."
fi

# Clear final output directory
if [ -d "${final_output_dir}" ]; then
    rm -rf "${final_output_dir}"/*
    echo "${final_output_dir} directory has been cleared."
else
    mkdir -p "${final_output_dir}"
    echo "${final_output_dir} directory has been created."
fi

processed_files=()
failed_files=()

# Find and process all txt files in the input directory
for input_file in "${input_dir}"/*.txt; do
    # Check if any txt files exist
    if [ ! -e "$input_file" ]; then
        echo "No txt files found. Please ensure there is a txt file in the ${input_dir} directory."
        exit 1
    fi

    # Get the filename of the input txt file without the path
    input_filename=$(basename "${input_file}")

    # Convert dispersion data file to disp.d
    ./1_process_disp.sh "${input_file}" || { echo "Error processing ${input_file}. Skipping this file."; failed_files+=("${input_filename}"); continue; }

    # Generate model file modl.d
    ./2_process_modl.sh "${input_file}" || { echo "Error processing ${input_file}. Skipping this file."; failed_files+=("${input_filename}"); continue; }

    # Perform inversion processing
    ./3_process_single.sh "disp.d" "${output_dir}" "${timeout_duration}" || { echo "Error processing ${input_file}. Skipping this file."; failed_files+=("${input_filename}"); continue; }

    # Copy output_dir to output folder and rename it to the input txt file name
    cp -r "${output_dir}" "${final_output_dir}/${input_filename}"
    echo "${output_dir} has been copied and renamed to ${final_output_dir}/${input_filename}."

    # Record processed files
    processed_files+=("${input_filename}")

    # Clear output_dir
    rm -rf "${output_dir}"/*
    echo "${output_dir} has been cleared."
done

# Delete output_dir folder
rm -rf "${output_dir}"
echo "${output_dir} folder has been deleted."

# Output processed file list
echo "Processed files:"
for file in "${processed_files[@]}"; do
    echo "$file"
done

echo "Failed files:"
for file in "${failed_files[@]}"; do
    echo "$file"
done

echo "All processing is complete."

# Call Python script to organize output files
merge_file_path=$(python 4_out_files_organize.py "${final_output_dir}" | grep 'Merged output saved to' | awk '{print $5}')
if [ -z "$merge_file_path" ]; then
    echo "Error occurred while organizing output files."
    exit 1
fi

echo "All files have been organized."

python 6_txt_plot.py "${merge_file_path}" || { echo "Error occurred while calling the Python script."; exit 1; }
echo "All files have been processed and plotted."
