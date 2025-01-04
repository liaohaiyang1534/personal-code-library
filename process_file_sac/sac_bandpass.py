# -*- encoding: utf-8 -*-
'''
@File        :   sac_bandpass.py
@Time        :   2025/01/03 22:44:08
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import numpy as np
import matplotlib.pyplot as plt
import obspy
import os

# Set matplotlib to use Agg backend to avoid errors in non-GUI environments
plt.switch_backend('agg')

def compute_spectrum(stream):
    spectra_sum = None

    # Iterate through all traces
    for trace in stream:
        # Perform Fast Fourier Transform
        fft = np.fft.rfft(trace.data)
        amplitude_spectrum = np.abs(fft)
        
        # Accumulate amplitude spectra
        if spectra_sum is None:
            spectra_sum = amplitude_spectrum
        else:
            spectra_sum += amplitude_spectrum
    
    # Compute average spectrum
    avg_spectra = spectra_sum / len(stream)
    return avg_spectra, stream[0].stats.sampling_rate

def plot_sac_spectra_and_save(file_path, low_freq, high_freq):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.dirname(file_path)  # Get the directory of the SAC file
    image_path = os.path.join(output_dir, f'{base_name}_spectra_comparison_{low_freq}-{high_freq}Hz.png')  # Construct full path for the PNG file

    # Read the SAC file
    stream = obspy.read(file_path)

    # Compute spectrum before filtering
    avg_spectra_before, sampling_rate = compute_spectrum(stream)

    # Apply bandpass filter
    filtered_stream = stream.copy()
    for trace in filtered_stream:
        trace.filter("bandpass", freqmin=low_freq, freqmax=high_freq)
    
    # Compute spectrum after filtering
    avg_spectra_after, _ = compute_spectrum(filtered_stream)

    # Calculate frequency
    nyquist = 0.5 * sampling_rate
    freq = np.linspace(0, nyquist, len(avg_spectra_before))
    
    # Get the maximum frequency range before and after filtering
    mask_before = (freq >= low_freq) & (freq <= nyquist)
    mask_after = (freq >= low_freq) & (freq <= high_freq)
    mask = mask_before | mask_after
    
    freq = freq[mask]
    avg_spectra_before = avg_spectra_before[mask]
    avg_spectra_after = avg_spectra_after[mask]

    # Plot spectrum comparison
    plt.figure(figsize=(10, 6))
    plt.plot(freq, avg_spectra_before, label='Before Filtering')
    plt.plot(freq, avg_spectra_after, label='After Filtering')
    plt.title(f"Amplitude Spectrum Comparison of {base_name} ({low_freq}-{high_freq} Hz)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.savefig(image_path)
    plt.close()
    print(f"Spectrum comparison plot saved as {image_path}")

def filter_and_save_sac(file_path, low_freq, high_freq):
    # Read the SAC file
    stream = obspy.read(file_path)
    filtered_stream = stream.copy()

    # Iterate through all traces and apply bandpass filter
    for trace in filtered_stream:
        trace.filter("bandpass", freqmin=low_freq, freqmax=high_freq)

    # Construct new file name and save
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.dirname(file_path)  # Get the directory of the SAC file
    filtered_file_path = os.path.join(output_dir, f'{base_name}_filtered_{low_freq}-{high_freq}Hz.sac')
    
    filtered_stream.write(filtered_file_path, format='SAC')
    print(f"Filtered SAC file saved as {filtered_file_path}")

# Usage
file_path = r"H:\github\personal-code-library\SAC_process\2024-01-24-11-17-19-out0012.sac"
low_freq = 40
high_freq = 50

filter_and_save_sac(file_path, low_freq, high_freq)
plot_sac_spectra_and_save(file_path, low_freq, high_freq)
