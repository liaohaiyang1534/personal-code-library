# -*- encoding: utf-8 -*-
'''
@File        :   single_frequency_energy_sgy.py
@Time        :   2025/01/03 22:51:22
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import numpy as np
import segyio
import shutil
import os
import matplotlib.pyplot as plt

def fourier_transform(traces):
    """Compute the Fourier transform of seismic traces."""
    return np.fft.rfft(traces, axis=0)

def inverse_fourier_transform(spectrum):
    """Compute the inverse Fourier transform."""
    return np.fft.irfft(spectrum, axis=0)

def normalize_frequency_energy(spectrum):
    """Normalize the energy of frequency components."""
    energy = np.sum(np.abs(spectrum)**2, axis=0, keepdims=True)
    normalized_spectrum = spectrum / np.sqrt(energy)
    return normalized_spectrum

def plot_waveforms(original_trace, normalized_trace, trace_index):
    """Plot original and normalized waveforms in time and frequency domains."""
    # Compute Fourier transform for original and normalized traces
    original_spectrum = fourier_transform(original_trace)
    normalized_spectrum = fourier_transform(normalized_trace)

    # Frequency axis
    freqs = np.fft.rfftfreq(len(original_trace), d=1)  # Assuming sampling interval is 1ms

    # Time domain comparison
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(original_trace, label="Original Trace", alpha=0.7)
    plt.plot(normalized_trace, label="Normalized Trace", alpha=0.7)
    plt.title(f"Trace {trace_index + 1} - Time Domain")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.legend()

    # Frequency domain comparison
    plt.subplot(2, 1, 2)
    plt.plot(freqs, np.abs(original_spectrum), label="Original Spectrum", alpha=0.7)
    plt.plot(freqs, np.abs(normalized_spectrum), label="Normalized Spectrum", alpha=0.7)
    plt.title(f"Trace {trace_index + 1} - Frequency Domain")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.legend()

    plt.tight_layout()
    plt.show()

def apply_frequency_energy_normalization(file_path, plot_trace_index=0):
    """Apply frequency energy normalization to seismic data and save the result."""
    # Generate a new file path with suffix _fre_ener.sgy
    output_file_path = file_path.replace('.sgy', '_fre_ener.sgy')
    
    # Copy the original file to the new path
    shutil.copy(file_path, output_file_path)
    
    with segyio.open(output_file_path, "r+", ignore_geometry=True) as f:
        # Extract and store a trace for visualization
        original_trace = np.copy(f.trace[plot_trace_index])
        
        for i in range(len(f.trace)):
            spectrum = fourier_transform(f.trace[i])
            normalized_spectrum = normalize_frequency_energy(spectrum)
            f.trace[i] = inverse_fourier_transform(normalized_spectrum).astype(np.float32)
        
        # Plot the original and normalized traces for the selected index
        normalized_trace = f.trace[plot_trace_index]
        plot_waveforms(original_trace, normalized_trace, plot_trace_index)

    print(f"Frequency energy normalization applied and saved to {output_file_path}")

# Input file path
file_path = r"H:\github\personal-code-library\SGY_process\2024-05-07-18-19-28.000_24.851_output.sgy"

# Apply frequency energy normalization and visualize
apply_frequency_energy_normalization(file_path, plot_trace_index=0)
