# -*- encoding: utf-8 -*-
'''
@File        :   batch_bandpass_sgy.py
@Time        :   2025/01/03 22:44:50
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import subprocess

def find_sgy_files(folder_path):
    sgy_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.sgy'):
                sgy_files.append(os.path.join(root, file))
    return sgy_files

def create_output_folder(folder_path):
    output_folder = folder_path + '_band'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def call_bandpass_script(sgy_file, output_folder, lowcut, highcut, current_sample_rate):
    script_path = r".\bandpass_sgy.py"
    output_file = os.path.join(output_folder, os.path.basename(sgy_file))
    subprocess.call(['python', script_path, sgy_file, output_file, str(lowcut), str(highcut), str(current_sample_rate)])

def main(folder_path, lowcut, highcut, current_sample_rate):
    sgy_files = find_sgy_files(folder_path)
    output_folder = create_output_folder(folder_path)
    for sgy_file in sgy_files:
        call_bandpass_script(sgy_file, output_folder, lowcut, highcut, current_sample_rate)

if __name__ == "__main__":
    folder_path = r"I:\diff_dis_to_cavity\17-19_3hours_downsampled"
    lowcut = 0.5  # Low cut frequency in Hz
    highcut = 50  # High cut frequency in Hz
    current_sample_rate = 100  # Specify the current sample rate in Hz
    main(folder_path, lowcut, highcut, current_sample_rate)