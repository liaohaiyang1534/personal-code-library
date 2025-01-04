# -*- encoding: utf-8 -*-
'''
@File        :   5_txt_adjustedtocps.py
@Time        :   2025/01/03 22:40:40
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import pandas as pd
import sys

def process_txt_files(input_folder):
    output_folder = input_folder + "_adjustedtocps"
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.disp'):
            file_path = os.path.join(input_folder, filename)
            
            try:
                # Read the file into a DataFrame, using regex to handle multiple spaces
                df = pd.read_csv(file_path, sep=r'\s+', header=None, engine='python')
                
                # Output the number of columns in the input file
                num_columns = len(df.columns)
                print(f"{filename} has {num_columns} columns.")
                
                # Check if the file has at least 3 columns
                if num_columns < 3:
                    # If not, add a third column filled with zeros
                    while len(df.columns) < 3:
                        df[len(df.columns)] = 0
                
                # Convert the second column to kilometers
                df[1] = df[1] * 0.001
                
                # Format the first and second columns to 4 decimal places
                df[0] = df[0].apply(lambda x: f"{x:.4f}")
                df[1] = df[1].apply(lambda x: f"{x:.4f}")
                
                # Change the file extension to .txt
                output_filename = os.path.splitext(filename)[0] + ".txt"
                output_path = os.path.join(output_folder, output_filename)
                
                # Save the modified DataFrame to the output folder
                df.to_csv(output_path, sep="\t", header=False, index=False)
                
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

# Replace 'your_input_folder_path' with the actual path to your input folder
input_folder_path = sys.argv[1]
process_txt_files(input_folder_path)
