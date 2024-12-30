from segpy.dataset import Dataset
from segpy.binary_reel_header import BinaryReelHeader
from segpy.field_types import Int32
from segpy.trace_header import TraceHeaderRev1
import numpy as np
import csv
import re
import segpy.writer

class CSV2SegyDataset(Dataset):
    def __init__(self, data, sample_interval_us):
        self._data = np.array(data).T
        self._sample_interval_us = sample_interval_us

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
        return th

def csv_to_segy(csv_file_path, dst_segy_file_path):
    match = re.search(r"sr(\d+)fs", csv_file_path)
    if match:
        sample_rate_hz = int(match.group(1))
        sample_interval_us = int(1e6 / sample_rate_hz)
    else:
        raise ValueError("Unable to extract sampling rate from the file name.")

    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = [list(map(float, row)) for row in reader]

    dataset = CSV2SegyDataset(data, sample_interval_us)

    with open(dst_segy_file_path, 'wb') as out_file:
        segpy.writer.write_segy(out_file, dataset)

# Execute the function
csv_file_path = r"E:\StudentsWork\lhy\onedrive\OneDrive - Nanjing University\Desktop\TEMP\240315\101_2nd_shot_trace_1508_filtered_cut_correlated_data_to913_reversed_sr500fs.csv"
dst_segy_file_path = r"E:\StudentsWork\lhy\onedrive\OneDrive - Nanjing University\Desktop\TEMP\240315\101_2nd_shot_trace_1508_filtered_cut_correlated_data_to913_reversed_sr500fs.sgy"
csv_to_segy(csv_file_path, dst_segy_file_path)
