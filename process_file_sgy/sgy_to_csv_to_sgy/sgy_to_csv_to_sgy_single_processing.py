# -*- encoding: utf-8 -*-
'''
@File        :   sgy_to_csv_to_sgy_single_processing.py
@Time        :   2025/01/03 22:45:16
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import segyio
import csv
import numpy as np
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
    def __init__(self, data, sample_interval_us, field_record_number, source_coordinates):
        self._data = np.array(data).T
        self._sample_interval_us = sample_interval_us
        self._field_record_number = field_record_number
        self._source_coordinates = source_coordinates

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
        return []

    @property
    def textual_reel_header(self):
        return ['{:<80}'.format('Converted from CSV')] * 40

    def trace_header(self, trace_index):
        th = TraceHeaderRev1()
        th.trace_sequence_number_within_line = trace_index + 1
        th.field_record_num = self._field_record_number
        th.energy_source_point_num = 101
        th.source_x = 0
        th.source_y = self._source_coordinates[0][1]
        th.group_x = (trace_index + 1) * 3
        return th

def csv_to_segy(csv_file_path, dst_segy_file_path, sample_interval_us, field_record_number, source_coordinates):
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = [list(map(float, row)) for row in reader]

    dataset = CSV2SegyDataset(data, sample_interval_us, field_record_number, source_coordinates)

    with open(dst_segy_file_path, 'wb') as out_file:
        segpy.writer.write_segy(out_file, dataset)

def convert_sgy_to_csv_and_back(sgy_file_path):
    base_path, filename = os.path.split(sgy_file_path)
    basename, _ = os.path.splitext(filename)
    csv_file_path = os.path.join(base_path, f"{basename}.csv")
    sample_interval_us = segy_to_csv(sgy_file_path, csv_file_path)
    new_sgy_file_path = os.path.join(base_path, f"{basename}_converted.sgy")

    field_record_number = 101

    with segyio.open(sgy_file_path, "r", ignore_geometry=True) as src:
        num_traces = src.tracecount
        source_coordinates = [(0, 0)] * num_traces

    csv_to_segy(csv_file_path, new_sgy_file_path, sample_interval_us, field_record_number, source_coordinates)

    print(f"Converted SGY to CSV: {csv_file_path}")
    print(f"Converted CSV back to SGY: {new_sgy_file_path}")

# Usage example
src_sgy_file_path = r"E:\240315\101_2nd_shot_trace_1508_filtered_cut_correlated_data_to913_reversed.sgy"
convert_sgy_to_csv_and_back(src_sgy_file_path)
