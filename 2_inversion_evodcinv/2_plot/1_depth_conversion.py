# -*- encoding: utf-8 -*-
'''
@File        :   1_depth_conversion.py
@Time        :   2025/01/03 22:42:15
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import sys


def process_files(input_folder):
    # Define the output folder
    output_folder = input_folder + "_depthtxt"
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Process each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)
            
            # Read the input file
            with open(input_file_path, 'r') as infile:
                lines = infile.readlines()
            
            # Extract the relevant lines
            processed_lines = lines[8:-7]
            
            filtered_lines = []
            depth = 0.0
            first_vs = 0.0  # To store the Vs value of the first layer
            
            # Process each line
            for index, line in enumerate(processed_lines):
                columns = line.split()
                if len(columns) >= 3:
                    thickness = float(columns[0])
                    depth += thickness
                    if index == 0:
                        first_vs = float(columns[2])  # Store the Vs value of the first layer
                    filtered_lines.append(f"{depth:.4f}\t{float(columns[2]):.4f}\n")
            
            # Add a row at the beginning for depth 0 with the same Vs as the first layer
            filtered_lines.insert(0, f"0.0000\t{first_vs:.4f}\n")
            
            # Write the processed lines to the output file
            with open(output_file_path, 'w') as outfile:
                outfile.writelines(filtered_lines)
    
    return output_folder


def main():
    # Get the input folder path from command-line arguments
    input_folder = sys.argv[1]

    # Process files and print the output folder path
    output_folder = process_files(input_folder)
    print(output_folder)


if __name__ == "__main__":
    main()
