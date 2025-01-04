# -*- encoding: utf-8 -*-
'''
@File        :   sgy_to_txt.py
@Time        :   2025/01/03 22:51:16
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import segyio
import os

def segy_to_txt(sgy_file_path):
    # Use segyio to read the SGY file
    with segyio.open(sgy_file_path, "r", ignore_geometry=True) as src:
        # Get the sample rate in microseconds
        sample_interval = src.bin[segyio.BinField.Interval]
        # Convert the sample rate to milliseconds
        sample_rate_ms = sample_interval / 1000.0

        # Collect all trace data using segyio tools
        data = segyio.tools.collect(src.trace[:])

        # Build the TXT file path, using the same name as the SGY file but with a .txt extension
        txt_file_path = os.path.splitext(sgy_file_path)[0] + '.txt'

        # Open a new TXT file to write the data
        with open(txt_file_path, 'w') as txtfile:
            # Iterate through the data and write each row, with each column representing a trace
            for trace in data.T:  # Use .T to transpose the matrix so each row represents one trace's data
                trace_line = ' '.join(map(str, trace))  # Convert values to strings and separate with spaces
                txtfile.write(trace_line + '\n')

    print(f"Trace data has been exported to {txt_file_path}, sample rate is {sample_rate_ms} ms.")

def process_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.sgy') or file_name.endswith('.segy'):
            sgy_file_path = os.path.join(folder_path, file_name)
            segy_to_txt(sgy_file_path)

# Use the function
folder_path = r"E:\liaohaiyang\research_project_shangyuanmen\2401_可控震源车井地联采测试\数据处理\active_source_surface_wave\Line3_p_wave\分炮点_对应编号_240318\101\2nd\地面光纤：1519\processed_20240318214536\processed_20240318234213"
process_folder(folder_path)
