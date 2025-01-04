# -*- encoding: utf-8 -*-
'''
@File        :   plot_sac_frequency_one_sac_5s_each_plot.py
@Time        :   2025/01/03 22:43:41
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import numpy as np
import matplotlib.pyplot as plt
import obspy
import os

# Set matplotlib to use Agg backend to avoid errors in environments without a GUI
plt.switch_backend('agg')

def plot_segmented_sac_spectra(file_path):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.dirname(file_path)  # Get the directory of the SAC file

    # Read SAC file
    stream = obspy.read(file_path)

    # Prepare to find the global maximum amplitude
    global_max_amplitude = 0

    # First pass: compute max amplitude for consistent scaling
    for trace in stream:
        sampling_rate = trace.stats.sampling_rate
        segment_length = int(5 * sampling_rate)
        num_segments = int(np.ceil(len(trace.data) / segment_length))

        for segment_index in range(num_segments):
            start_sample = segment_index * segment_length
            end_sample = start_sample + segment_length
            segment_data = trace.data[start_sample:end_sample]

            fft = np.fft.rfft(segment_data)
            amplitude_spectrum = np.abs(fft)

            current_max = np.max(amplitude_spectrum)
            if current_max > global_max_amplitude:
                global_max_amplitude = current_max

    # Second pass: plot using the global maximum for scaling
    for trace_index, trace in enumerate(stream):
        sampling_rate = trace.stats.sampling_rate
        segment_length = int(5 * sampling_rate)
        num_segments = int(np.ceil(len(trace.data) / segment_length))

        for segment_index in range(num_segments):
            start_sample = segment_index * segment_length
            end_sample = start_sample + segment_length
            segment_data = trace.data[start_sample:end_sample]

            fft = np.fft.rfft(segment_data)
            amplitude_spectrum = np.abs(fft)
            
            nyquist = 0.5 * sampling_rate
            freq = np.linspace(0, nyquist, len(amplitude_spectrum))
            
            mask = (freq >= 1) & (freq <= 1000)
            freq = freq[mask]
            amplitude_spectrum = amplitude_spectrum[mask]
            
            plt.figure(figsize=(10, 6))
            plt.plot(freq, amplitude_spectrum)
            plt.title(f"Spectrum of {base_name} Segment {segment_index + 1}")
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Amplitude")
            # plt.ylim(0, global_max_amplitude)  # Set uniform scale
            plt.ylim(0, 10)  # Set uniform scale
            plt.grid(True)
            
            image_name = f"{base_name}_segment_{segment_index + 1}_spectra.png"
            image_path = os.path.join(output_dir, image_name)
            plt.savefig(image_path)
            plt.close()
            print(f"Spectrum plot saved as {image_path}")

# Use the function
file_path = r"H:\github\personal-code-library\SAC_process\2024-01-24-11-17-19-out0012.sac"
plot_segmented_sac_spectra(file_path)
