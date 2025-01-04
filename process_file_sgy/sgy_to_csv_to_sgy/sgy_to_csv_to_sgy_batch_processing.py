# -*- encoding: utf-8 -*-
'''
@File        :   sgy_to_csv_to_sgy_batch_processing.py
@Time        :   2025/01/03 22:45:11
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import re
import segyio
import csv
import numpy as np
import shutil
from segpy.dataset import Dataset
from segpy.binary_reel_header import BinaryReelHeader
from segpy.trace_header import TraceHeaderRev1
import segpy.writer

def segy_to_csv(sgy_file_path, csv_file_path):
    with segyio.open(sgy_file_path, "r", ignore_geometry=True) as src:
        sample_interval_us = int(src.bin[segyio.BinField.Interval])
        data = segyio.tools.collect(src.trace[:])
        with open(csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            for i in range(len(data[0])):
                row = [trace[i] for trace in data]
                csvwriter.writerow(row)
        return sample_interval_us

class CSV2SegyDataset(Dataset):
    def __init__(self, data, sample_interval_us, field_record_number):
        self._data = np.array(data).T
        self._sample_interval_us = sample_interval_us
        self._field_record_number = field_record_number

    def num_traces(self):
        return len(self._data)

    def num_samples(self):
        return len(self._data[0])

    def trace_samples(self, trace_index, start=None, stop=None):
        return self._data[trace_index][start:stop]

    def sample_interval(self):
        return self._sample_interval_us

    @property
    def binary_reel_header(self):
        header = BinaryReelHeader()
        header.num_traces = self.num_traces()
        header.num_samples = self.num_samples()
        header.sample_interval = self._sample_interval_us
        return header

    @property
    def extended_textual_header(self):
        return []  # Return an empty list if there's no extended header

    @property
    def textual_reel_header(self):
        return ['{:<80}'.format('Converted from CSV')] * 40  # Create a simple header

    def trace_header(self, trace_index):
        th = TraceHeaderRev1()
        th.trace_sequence_number_within_line = trace_index + 1
        th.field_record_num = self._field_record_number
        th.energy_source_point_num = self._field_record_number
        th.source_x = 0
        th.group_x = (trace_index + 1) * 3  # Setting group_x for 3m spacing
        return th

def csv_to_segy(csv_file_path, dst_segy_file_path, sample_interval_us, field_record_number):
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = [list(map(float, row)) for row in reader]

    dataset = CSV2SegyDataset(data, sample_interval_us, field_record_number)

    with open(dst_segy_file_path, 'wb') as out_file:
        segpy.writer.write_segy(out_file, dataset)

def convert_sgy_to_csv_and_back(sgy_file_path, output_folder, field_record_number):
    base_path, filename = os.path.split(sgy_file_path)
    basename, _ = os.path.splitext(filename)
    csv_file_path = os.path.join(base_path, f"{basename}.csv")
    sample_interval_us = segy_to_csv(sgy_file_path, csv_file_path)
    new_sgy_file_path = os.path.join(output_folder, f"{basename}_converted.sgy")
    
    # Use the provided field_record_number instead of the default value
    csv_to_segy(csv_file_path, new_sgy_file_path, sample_interval_us, field_record_number)
    
    os.remove(csv_file_path)  # Remove the temporary CSV file
    print(f"Processed {sgy_file_path} and saved to {new_sgy_file_path}")

def process_folder(input_folder):
    output_folder = f"{input_folder}_add_group_x"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.sgy'):
                sgy_file_path = os.path.join(root, file)
                # Extract field record number from the filename and pass it to convert_sgy_to_csv_and_back
                match = re.match(r"(\d+)_", file)
                if match:
                    field_record_number = int(match.group(1))
                else:
                    print(f"No field record number found in {file}. Using default value 101.")
                    field_record_number = 101  # Default to 101 if no number is found
                print(f"Processing {sgy_file_path} with field record number {field_record_number}...")
                convert_sgy_to_csv_and_back(sgy_file_path, output_folder, field_record_number)

# Set the input folder path
input_folder = r"E:\数据处理\active_source_surface_wave\Line3_p_wave\test_101_diff_process_method\test_57shot_previous_and_after\101\2nd\地面光纤：1519\d"

# Call the function to process the specified folder
process_folder(input_folder)
