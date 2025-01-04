# -*- encoding: utf-8 -*-
'''
@File        :   4_out_files_organize.py
@Time        :   2025/01/03 22:40:31
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import shutil
from natsort import natsorted
from datetime import datetime
import re
import sys

def copy_and_merge_out_files(input_folder):
    # Create the output folder
    output_folder = input_folder + "_out"
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)  # Clear the output folder
    os.makedirs(output_folder, exist_ok=True)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.out'):
                parent_folder = os.path.basename(os.path.dirname(root))
                original_folder_name = os.path.basename(root).replace('.txt', '')
                new_file_name = f"{parent_folder}-{original_folder_name}.out"
                src_path = os.path.join(root, file)
                dest_path = os.path.join(output_folder, new_file_name)

                # Remove the first 12 lines and keep only the first and third columns
                with open(src_path, 'r') as src_file:
                    lines = src_file.readlines()[12:]  # Skip the first 12 lines

                new_lines = []
                depth = 0.0
                for line in lines:
                    columns = line.split()  # Adjust delimiter as needed
                    if len(columns) >= 3:
                        thickness = float(columns[0])
                        depth += thickness
                        new_line = f"{depth:.4f} {columns[2]}\n"
                        new_lines.append(new_line)

                # Remove the last line
                new_lines = new_lines[:-1]

                with open(dest_path, 'w') as dest_file:
                    dest_file.writelines(new_lines)
                
                print(f"Copied {src_path} to {dest_path} (without first 12 lines, depth information instead of thickness, with 4 decimal places, last line removed)")

    # Sort all .out files in the output folder
    out_files = natsorted([f for f in os.listdir(output_folder) if f.endswith('.out')])

    # Create a new merged output file with a timestamp in the input folder's parent directory
    mergetxt_output_folder = input_folder + "_txt"
    os.makedirs(mergetxt_output_folder, exist_ok=True)  # Ensure the directory exists
    merged_file_path = os.path.join(mergetxt_output_folder, f"Merged_Output.txt")
    with open(merged_file_path, 'w') as merged_file:
        for out_file in out_files:
            out_file_path = os.path.join(output_folder, out_file)
            
            # Extract the numerical value between the last '-' and '.out'
            match = re.search(r'-(\d+\.\d+)\.out', out_file)
            if not match:
                print(f"Error: File name {out_file} does not match expected pattern.")
                continue
            index_value = float(match.group(1))

            with open(out_file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    columns = line.split()
                    if len(columns) == 2:
                        first_column = float(columns[0]) * -1000
                        second_column = float(columns[1]) * 1000
                        merged_file.write(f"{index_value:.1f} {first_column:.4f} {second_column:.4f}\n")

    print(f"Merged output saved to {merged_file_path}")
    return merged_file_path  # Return the path of the merged file

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 4_out文件整理到一起.py <input_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    merge_path = copy_and_merge_out_files(input_folder)
    print(merge_path)  # Print the path of the merged file
