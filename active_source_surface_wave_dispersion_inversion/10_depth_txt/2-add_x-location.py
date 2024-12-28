import os
import glob
import re
import sys
import matplotlib.pyplot as plt

def find_txt_files_and_extract_ds_info(folder_path):
    # Find all text files
    txt_files = glob.glob(os.path.join(folder_path, '**', '*.txt'), recursive=True)
    
    # Store file information and extracted numerical info
    files_info = []
    
    for txt_file in sorted(txt_files):
        file_name = os.path.basename(txt_file)
        file_path = os.path.abspath(txt_file)
        
        # Extract location info using the new extract function
        year, month, day, start_time, end_time, ch1, ch2 = extract(file_name)
        ds_number = ch1 + (ch2 - ch1) / 2
        
        files_info.append({
            'file_name': file_name,
            'file_path': file_path,
            'ds_number': ds_number
        })
    
    return files_info

def process_and_output_files(files_info, output_folder):
    # Create output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for info in files_info:
        with open(info['file_path'], 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
        
        # Calculate the relative output file path
        relative_path = os.path.relpath(info['file_path'], os.path.dirname(info['file_path']))
        output_file = os.path.join(output_folder, relative_path)
        output_dir = os.path.dirname(output_file)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for line in lines:
                if line.strip():  # Ignore empty lines
                    thickness, value = map(float, line.split())
                    new_thickness = thickness * 1000
                    new_value = value * 1000
                    outfile.write(f"{info['ds_number']:.6f} {new_thickness:.6f} {new_value:.6f}\n")
    
    print(f"All text files have been processed and output to: {output_folder}")

def extract(file_name):
    base_name = file_name.split('.')[0]
    date_part, info_part = base_name.split('_')
    year, month, day = map(int, date_part.split('-'))
    sgy, start_time, end_time, ch1, ch2 = info_part.split('-')
    start_time = eval(start_time.replace('x', '*'))
    end_time = eval(end_time.replace('x', '*'))
    ch1 = int(ch1)
    ch2 = int(ch2)
    return (year, month, day, start_time, end_time, ch1, ch2)

def main():
    input_folder = sys.argv[1]
    output_folder = input_folder + "_txts"
    
    files_info = find_txt_files_and_extract_ds_info(input_folder)
    process_and_output_files(files_info, output_folder)
    
    print(output_folder)  # Print only the output folder path

if __name__ == "__main__":
    main()
