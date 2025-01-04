# -*- encoding: utf-8 -*-
'''
@File        :   NOT USED FOR NOW - batch_shot_time_match.py
@Time        :   2025/01/03 22:31:50
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import sys
import subprocess

def create_output_folder(input_folder):
    output_folder = f"{input_folder}_shottimematch"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def find_sgy_files(input_folder):
    sgy_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".sgy"):
                sgy_files.append(os.path.join(root, file))
    return sgy_files

if __name__ == "__main__":





    input_folder = r"H:\lhyonedrive\OneDrive\diff_coupling\active_source_2\tumai_2024-05-02_sgy_273_389_split_removebad"

    txt_file_path = r"H:\lhyonedrive\OneDrive\diff_coupling\active_source_2\shot_time.txt"





    output_folder = create_output_folder(input_folder)
    sgy_files = find_sgy_files(input_folder)
    python_file_path = r"H:\lhyonedrive\OneDrive\code_copy\active_source_classification\3_shot_time_match\shot_time_match.py"


    success_files = []
    no_match_files = []
    multiple_match_files = []
    file_not_found_files = []

    for sgy_file in sgy_files:
        result = subprocess.run(["python", python_file_path, txt_file_path, sgy_file, output_folder], capture_output=True, text=True)
        if result.returncode == 0:
            success_files.append(sgy_file)
        elif result.returncode == 1:
            no_match_files.append(sgy_file)
        elif result.returncode == 2:
            multiple_match_files.append(sgy_file)
        elif result.returncode == 3:
            file_not_found_files.append(sgy_file)

    print("\nSummary:")
    print(f"Total SGY files processed: {len(sgy_files)}")
    print(f"Successful matches: {len(success_files)}")
    print(f"No matching times found: {len(no_match_files)}")
    print(f"Multiple matching times found: {len(multiple_match_files)}")
    print(f"File not found: {len(file_not_found_files)}")

    if no_match_files:
        print("\nFiles with no matching times:")
        for file in no_match_files:
            print(file)

    if multiple_match_files:
        print("\nFiles with multiple matching times:")
        for file in multiple_match_files:
            print(file)

    if file_not_found_files:
        print("\nFiles not found:")
        for file in file_not_found_files:
            print(file)
