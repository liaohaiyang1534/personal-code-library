# -*- encoding: utf-8 -*-
'''
@File        :   sac_downsample.py
@Time        :   2025/01/03 22:44:13
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import obspy
import os

def downsample_and_save(file_path, target_rate):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.dirname(file_path)  # Get the directory of the SAC file
    downsampled_file_path = os.path.join(output_dir, f'{base_name}_downsampled_{target_rate}Hz.sac')  # Construct the full path for the new SAC file

    # Read the SAC file
    stream = obspy.read(file_path)
    for trace in stream:
        trace.decimate(int(trace.stats.sampling_rate / target_rate), no_filter=True)
    
    # Save as a new SAC file
    stream.write(downsampled_file_path, format='SAC')
    print(f"Downsampled SAC file saved as {downsampled_file_path}")

# Usage
file_path = r"H:\lhyonedrive\OneDrive\sym\paper\docs\pics_plot_pics_codes\背景噪声能量白天黑夜对比_20240710\G2024-07-02_sac_550_merged_output.sac"
target_rate = 100

downsample_and_save(file_path, target_rate)
