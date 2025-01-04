# -*- encoding: utf-8 -*-
'''
@File        :   txt_to_sac.py
@Time        :   2025/01/03 22:44:27
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import numpy as np
from obspy import UTCDateTime, Trace, Stream

def txt_to_sac(input_file, output_file, delta=1/500.0):
    # Read data
    data = np.loadtxt(input_file)
    
    # Assume the first column is time (seconds), the second column is seismic waveform data
    times = data[:, 0]
    waveform = data[:, 1]

    # Calculate start time
    start_time = UTCDateTime() + times[0]
    
    # Create Trace object
    trace = Trace(data=waveform)
    trace.stats.starttime = start_time
    trace.stats.delta = delta
    trace.stats.network = 'XX'  # Example network code
    trace.stats.station = 'XXXX'  # Example station code
    trace.stats.channel = 'HHZ'  # Example channel code

    # Create Stream object and write to SAC file
    stream = Stream(traces=[trace])
    stream.write(output_file, format='SAC')

# Specify input and output files
input_file = r"I:\阴井\data_20240627-0706\2024-0628-0630-0701-0704-0705-combined_output平均.txt"
output_file = r"I:\阴井\data_20240627-0706\2024-0628-0630-0701-0704-0705-combined_output平均.sac"

# Call the function
txt_to_sac(input_file, output_file)
