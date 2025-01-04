# -*- encoding: utf-8 -*-
'''
@File        :   sgy_to_sac.py
@Time        :   2025/01/03 22:51:06
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import segyio
import obspy
import os

def segy_trace_to_sac(sgy_file_path, output_dir):
    with segyio.open(sgy_file_path, "r", ignore_geometry=True) as src:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Iterate through each trace and convert it to SAC format
        for index, trace in enumerate(src.trace):
            # Calculate sample rate
            sample_interval = src.bin[segyio.BinField.Interval] / 1000000.0  # Convert to seconds

            # Create an obspy Trace object
            tr = obspy.Trace(data=trace)

            # Set necessary header information
            tr.stats.delta = sample_interval
            tr.stats.station = str(index + 1)
            tr.stats.network = "XX"
            tr.stats.location = ""
            tr.stats.channel = "Z"

            # Calculate and set dist
            dist = (index + 1) * 2  # Each trace increases by 2 meters
            print(f"Trace {index + 1} dist: {dist}")  # Output dist for each trace

            tr.stats.sac = {'dist': dist}

            # Write to SAC file
            sac_file_name = f"{index + 1}.sac"
            sac_file_path = os.path.join(output_dir, sac_file_name)
            tr.write(sac_file_path, format='SAC')

        print(f"Conversion completed: {sgy_file_path} -> {output_dir}")

def process_single_sgy(sgy_file_path):
    base_name = os.path.splitext(os.path.basename(sgy_file_path))[0]  # Extract file name without extension
    output_dir = os.path.join(os.path.dirname(sgy_file_path), base_name)  # Create a folder with the same name
    segy_trace_to_sac(sgy_file_path, output_dir)

# Input SGY file path
sgy_file_path = r"D:\学生工作\罗淇\cejing\2024-05-02_sgy\2024-05-02-17-19-45-out.sgy"

# Use the function
process_single_sgy(sgy_file_path)
