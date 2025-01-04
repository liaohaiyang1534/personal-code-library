# -*- encoding: utf-8 -*-
'''
@File        :   3_merge_to_one_txt.py
@Time        :   2025/01/03 22:42:24
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import sys

def merge_txt_files(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define the output file path
    output_file = os.path.join(output_folder, f"{os.path.basename(input_folder)}.txt")
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Iterate through sorted files in the input folder
        for filename in sorted(os.listdir(input_folder)):
            if filename.endswith('.txt'):
                file_path = os.path.join(input_folder, filename)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    for line in infile:
                        line = line.strip()
                        if line:
                            columns = line.split()
                            if len(columns) > 1:
                                try:
                                    # Try to convert the second column to float and check the condition
                                    second_column_value = float(columns[1])
                                    if second_column_value <= 600:
                                        # No modification for the first column
                                        columns[0] = str(float(columns[0]))

                                        # Write the updated columns as a line in the output file
                                        outfile.write(" ".join(columns))
                                        outfile.write("\n")
                                except ValueError:
                                    continue  # Skip lines where conversion to float fails
    return output_file

def main():
    # Get the input folder path from command-line arguments
    input_folder = sys.argv[1]
    output_folder = input_folder + '_onetxt'
    output_file = merge_txt_files(input_folder, output_folder)
    print(output_file)  # Print the output file path

if __name__ == "__main__":
    main()
