# -*- encoding: utf-8 -*-
'''
@File        :   dat to sac.py
@Time        :   2025/01/03 22:43:00
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import sys
import os
import numpy as np
import obspy
import shutil
import threading
import multiprocessing  # To determine the number of available CPU cores

input_dir = r"F:\diff_distance_to_cavity\noise_data\raw_data"  # Input directory

output_dir = r"F:\diff_distance_to_cavity\noise_data\processed_sac"  # Output directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Dynamically determine the number of threads based on CPU cores
num_threads = multiprocessing.cpu_count()  # Number of available CPU cores
file_list = os.listdir(input_dir)
total_files = len(file_list)

# Automatically calculate the number of files each thread should process
files_per_thread = max(1, total_files // num_threads)  # Ensure at least 1 file per thread

def process_files(file_list):
    for file_name in file_list:
        try:
            input_file_path = os.path.join(input_dir, file_name)
            with open(input_file_path, 'rb') as f:
                raw_data = np.fromfile(f, dtype=np.float32)
                header = raw_data[:64]  # File header
                waveform_data = raw_data[64:]  # Signal data
                sampling_rate = header[10]  # Sampling rate
                num_channels = int(header[16])  # Number of channels
                samples_per_channel = int(header[10] * header[17])  # Samples per channel
                
                # Reshape waveform data into a 2D array: [num_channels, samples_per_channel]
                reshaped_data = waveform_data.reshape(samples_per_channel, num_channels).T
                
                # Define output path for the current file
                file_output_dir = os.path.join(output_dir, file_name[:-4])  # Directory per file
                if not os.path.exists(file_output_dir):
                    os.makedirs(file_output_dir)
                else:
                    shutil.rmtree(file_output_dir)
                    os.makedirs(file_output_dir)
                
                # Process each channel and save as SAC file
                for channel_idx in range(num_channels):
                    channel_data = reshaped_data[channel_idx, :]
                    channel_number = f"{channel_idx + 1:04}"  # Format as 4-digit number
                    sac_filename = f"{file_name[:-12]}{file_name[-8:-4]}{channel_number}.sac"
                    sac_file_path = os.path.join(file_output_dir, sac_filename)
                    
                    trace = obspy.Trace()
                    trace.stats.network = "NJU"
                    trace.stats.station = "STA"
                    trace.stats.channel = "BHZ"
                    trace.stats.sampling_rate = sampling_rate
                    trace.stats.starttime = obspy.UTCDateTime(
                        file_name[0:10] + 'T' + file_name[11:13] + ':' + file_name[14:16] + ':' + file_name[17:19]
                    )
                    trace.data = channel_data
                    trace.write(sac_file_path, format='sac')
            print(f"Processed: {file_name}")
        except (ValueError, FileNotFoundError) as e:
            print(f"Error processing {file_name}: {e}")
            continue

# Divide file list among threads
threads = []

for i in range(0, total_files, files_per_thread):
    files_chunk = file_list[i:i + files_per_thread]
    t = threading.Thread(target=process_files, args=(files_chunk,))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()
