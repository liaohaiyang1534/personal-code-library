# -*- encoding: utf-8 -*-
'''
@File        :   5_clean_files.py
@Time        :   2025/01/03 22:52:00
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import sys

def clean_specific_files(root_folder, target_filenames, rename_rules, specific_depth=3):
    """
    Retain specific files, delete all other files in directories at a specified depth,
    and rename certain files based on rename rules.
    
    :param root_folder: Path to the root directory
    :param target_filenames: List of filenames to keep
    :param rename_rules: Rename rules as a dictionary {original_filename: new_filename}
    :param specific_depth: Specific depth of the directory to process
    """
    print(f"Starting processing in {root_folder}")
    
    # Initialize counters for tracking actions
    kept_files_count = 0
    deleted_files_count = 0
    renamed_files_count = 0

    # Calculate the depth of the root directory
    root_depth = root_folder.count(os.sep)

    for subdir, dirs, files in os.walk(root_folder):
        # Calculate the current directory depth
        current_depth = subdir.count(os.sep) - root_depth

        if current_depth == specific_depth:
            for file in files:
                # Construct the full file path
                file_path = os.path.join(subdir, file)

                if file not in target_filenames:
                    # If the file is not in the target list, delete it
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                    deleted_files_count += 1
                else:
                    # If the file is in the target list, keep it
                    print(f"Kept: {file_path}")
                    kept_files_count += 1
                    # Check if the file needs to be renamed
                    if file in rename_rules:
                        new_file_name = rename_rules[file]
                        new_file_path = os.path.join(subdir, new_file_name)
                        os.rename(file_path, new_file_path)
                        print(f"Renamed: {file_path} to {new_file_path}")
                        renamed_files_count += 1

    print(f"Finished processing. Files kept: {kept_files_count}, Files deleted: {deleted_files_count}, Files renamed: {renamed_files_count}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No directory path provided. Usage: python script.py <root_folder_path>")
        sys.exit(1)

    root_folder = sys.argv[1]
    target_file_names = [
        "to_1028_reversed_time_cropped.sgy", 
        "to_1267_time_cropped.sgy",
        "x_plot_waveform.png",
        "x_plot_spectrum.png",
        "x_plot_time_and_frequency_analysis.png"
    ]
    rename_rules = {
        "to_1028_reversed_time_cropped.sgy": "1028.sgy",
        "to_1267_time_cropped.sgy": "1267.sgy"
    }

    clean_specific_files(root_folder, target_file_names, rename_rules)
