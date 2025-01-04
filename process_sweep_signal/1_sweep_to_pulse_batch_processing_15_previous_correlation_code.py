# -*- encoding: utf-8 -*-
'''
@File        :   1_sweep_to_pulse_batch_processing_15_previous_correlation_code.py
@Time        :   2025/01/03 22:51:37
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import segyio
import numpy as np
import shutil
import os
import re
import sys
import obspy
from obspy import Trace, Stream
from obspy import UTCDateTime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')

from scipy.signal import stft
from obspy import read

if len(sys.argv) > 1:
    root_folder = sys.argv[1]
else:
    print("Error: No directory path provided.")
    sys.exit(1)

print(f"Processing directory: {root_folder}")

def process_sgy_file(sgy_file_path, output_folder, reference_trace):
    start_time = 0.0
    end_time = 13000.0

    x0 = reference_trace

    x1 = 1028
    x2 = 1280

    original_filename = sgy_file_path
    base_filename = os.path.basename(original_filename)
    new_filename = os.path.join(output_folder, base_filename)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if not os.path.exists(new_filename):
        shutil.copyfile(original_filename, new_filename)

    sample_interval_ms = 2
    sample_interval = sample_interval_ms / 1000.0

    with segyio.open(new_filename, "r", ignore_geometry=True) as f:
        data = segyio.tools.collect(f.trace[:])
        times = f.samples

        if sample_interval <= 0:
            sample_interval = 1000

        start_sample = int(start_time / sample_interval)
        end_sample = int(end_time / sample_interval)

        data_extracted = data[:, start_sample:end_sample]
        times_extracted = times[start_sample:end_sample]

    extracted_filename = os.path.join(output_folder, "extracted_data.sgy")
    with segyio.open(new_filename, "r+", ignore_geometry=True) as src:
        spec = segyio.spec()
        spec.sorting = src.sorting
        spec.format = src.format
        spec.samples = times_extracted
        spec.tracecount = len(data_extracted)

        with segyio.create(extracted_filename, spec) as dst:
            for i, trace in enumerate(data_extracted):
                dst.trace[i] = trace

    max_amplitude_all_traces = np.max(np.abs(data))

    selected_traces = data[x1:x2+1]
    if len(selected_traces) == 0:
        return

    selected_filename = os.path.join(output_folder, "selected_data.sgy")
    with segyio.open(extracted_filename, "r", ignore_geometry=True) as src:
        spec = segyio.spec()
        spec.sorting = src.sorting
        spec.format = src.format
        spec.samples = src.samples
        spec.tracecount = len(selected_traces)

        with segyio.create(selected_filename, spec) as dst:
            for i, trace in enumerate(selected_traces):
                dst.trace[i] = trace

    mode = 'full'
    correlated_data = []
    for i in range(x1, x2+1):
        correlated_trace = np.correlate(data[i], data[x0], mode=mode)
        correlated_data.append(correlated_trace)

    zero_point = len(correlated_data[0]) // 2

    correlated_samples_count = (len(data[0]) * 2) - 1
    correlated_data_length_ms = correlated_samples_count * sample_interval_ms

    full_filename = os.path.join(output_folder, "correlated_full.sgy")
    with segyio.open(extracted_filename, "r", ignore_geometry=True) as src:
        spec = segyio.spec()
        spec.sorting = src.sorting
        spec.format = src.format
        spec.samples = np.arange(0, correlated_data_length_ms, 2)
        spec.interval = 2000
        spec.tracecount = len(correlated_data)

        with segyio.create(full_filename, spec) as dst:
            for i, trace in enumerate(correlated_data):
                dst.trace[i] = trace

    correlated_before_zero = [trace[:zero_point] for trace in correlated_data]
    correlated_after_zero = [trace[zero_point:] for trace in correlated_data]

    before_zero_filename = os.path.join(output_folder, "correlated_before_zero.sgy")
    with segyio.open(extracted_filename, "r", ignore_geometry=True) as src:
        spec = segyio.spec()
        spec.sorting = src.sorting
        spec.format = src.format
        spec.samples = np.arange(zero_point) * 2
        spec.tracecount = len(correlated_before_zero)
        spec.interval = 2000

        with segyio.create(before_zero_filename, spec) as dst:
            for i, trace in enumerate(correlated_before_zero):
                dst.trace[i] = trace

    after_zero_filename = os.path.join(output_folder, "correlated_after_zero.sgy")
    with segyio.open(extracted_filename, "r", ignore_geometry=True) as src:
        spec = segyio.spec()
        spec.sorting = src.sorting
        spec.format = src.format
        spec.samples = np.arange(len(correlated_data[0]) - zero_point) * 2
        spec.tracecount = len(correlated_after_zero)
        spec.interval = 2000

        with segyio.create(after_zero_filename, spec) as dst:
            for i, trace in enumerate(correlated_after_zero):
                dst.trace[i] = trace

    x_plot = reference_trace
    sample_interval = 1 / 500

    trace = Trace(data[x_plot])
    trace.stats.starttime = UTCDateTime()
    trace.stats.sampling_rate = 1 / sample_interval
    stream = Stream(traces=[trace])
    sac_filename = os.path.join(output_folder, "x_plot.sac")
    stream.write(sac_filename, format='SAC')

    print(f'Sample rate: {trace.stats.sampling_rate} Hz')
    print(f'Number of samples: {len(data[x_plot])}')
    print(f'Sample interval: {sample_interval} s')

    time_axis = np.arange(len(data[x_plot])) * sample_interval * 1000
    plt.figure(figsize=(20, 5), dpi=50)
    plt.plot(time_axis, data[x_plot])
    plt.title(f'Trace Index : {x_plot} - Waveform - Fs: {1/sample_interval:.2f} Hz')
    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude')
    plt.savefig(os.path.join(output_folder, 'x_plot_waveform.png'))
    plt.close()

    freqs = np.fft.rfftfreq(len(data[x_plot]), d=sample_interval)
    spectrum = np.fft.rfft(data[x_plot])
    plt.figure(figsize=(10, 5), dpi=50)
    plt.plot(freqs, np.abs(spectrum))
    plt.title(f'Trace Index : {x_plot} - Frequency Spectrum - Fs: {1/sample_interval:.2f} Hz')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim([0, 100])
    plt.savefig(os.path.join(output_folder, 'x_plot_spectrum.png'))
    plt.close()

    def plot_stft(sac_file, x_plot, window='hann', nperseg=256, noverlap=128, time_range=None, freq_range=None):
        st = read(sac_file)
        tr = st[0]
        print(f'Reading SAC file: {sac_file}')
        print(f'Sampling rate from SAC: {tr.stats.sampling_rate} Hz, Number of samples: {len(tr.data)}')

        f, t, Zxx = stft(tr.data, fs=tr.stats.sampling_rate, window=window, nperseg=nperseg, noverlap=noverlap)
        fig, ax = plt.subplots(figsize=(10, 6))
        c = ax.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
        plt.title(f'Trace Index : {x_plot} - STFT Magnitude')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        if time_range:
            plt.xlim(time_range)
        if freq_range:
            plt.ylim(freq_range)
        cb = plt.colorbar(c, label='Magnitude')
        plt.savefig(os.path.join(output_folder, 'x_plot_time_and_frequency_analysis.png'))
        plt.close()

    sac_file_path = sac_filename
    plot_stft(sac_file_path, x_plot, window='hann', nperseg=256, noverlap=128, time_range=None, freq_range=(1, 100))

def extract_numbers_from_parent_folder_name(folder_path):
    parent_folder_name = os.path.basename(os.path.dirname(folder_path))
    return re.findall(r'\d+', parent_folder_name)

def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

def process_folder(root_folder, max_depth=1):
    root_depth = root_folder.rstrip(os.sep).count(os.sep)
    for subdir, dirs, files in os.walk(root_folder):
        current_depth = subdir.rstrip(os.sep).count(os.sep)
        if current_depth - root_depth >= max_depth:
            continue

        numbers = extract_numbers_from_parent_folder_name(subdir)
        if numbers:
            shot_number = int(numbers[0])
            reference_trace = ((shot_number - 1) * 6 + 1029) + (14.0540541 - 0.35135135 * shot_number)
            reference_trace = 0.11428571 * shot_number + reference_trace
            reference_trace = reference_trace + 26
            reference_trace = int(reference_trace)
        else:
            shot_number = "Unknown"
            reference_trace = 1

        new_folder_name = f"ground_fiber_{reference_trace}"
        output_folder = os.path.join(subdir, new_folder_name)

        clear_folder(output_folder)

        for file in files:
            if file.lower().endswith('.sgy'):
                sgy_file_path = os.path.join(subdir, file)
                process_sgy_file(sgy_file_path, output_folder, reference_trace)
                print(f"Processed file: {sgy_file_path}")

process_folder(root_folder, max_depth=3)
