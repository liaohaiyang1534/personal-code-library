# -*- encoding: utf-8 -*-
'''
@File        :   wavelet_transform_of_sac.py
@Time        :   2025/01/03 22:44:36
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import numpy as np
import matplotlib.pyplot as plt
import pywt
from obspy import read

def scale_to_frequency(scales, wavelet='morl', sampling_rate=1.0):
    """Convert wavelet scales to frequencies."""
    return pywt.scale2frequency(wavelet, scales) / (1.0 / sampling_rate)

def plot_wavelet_function(wavelet='morl'):
    """Plot the selected wavelet function."""
    wavelet_function = pywt.ContinuousWavelet(wavelet)
    psi, x = wavelet_function.wavefun(level=5)
    
    plt.figure(figsize=(10, 3))
    plt.plot(x, psi.real, label='Real Part')
    plt.plot(x, psi.imag, linestyle='--', label='Imaginary Part')
    plt.title(f'{wavelet} Wavelet Function')
    plt.legend()
    plt.grid()
    plt.show()

def load_sac_file(sac_file):
    """Load SAC file and return data and sampling rate."""
    st = read(sac_file)
    tr = st[0]
    data = tr.data
    sampling_rate = tr.stats.sampling_rate
    return data, sampling_rate

def plot_waveform(data, sampling_rate):
    """Plot the waveform of the data."""
    time = np.arange(len(data)) / sampling_rate
    plt.figure(figsize=(10, 4))
    plt.plot(time, data)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Original Waveform')
    plt.grid()
    plt.show()

def compute_wavelet_transform(data, sampling_rate, wavelet, scales_range):
    """Compute the wavelet transform and return coefficients and frequencies."""
    scales = np.arange(scales_range[0], scales_range[1])
    coefficients, _ = pywt.cwt(data, scales, wavelet, 1.0 / sampling_rate)
    frequencies = scale_to_frequency(scales, wavelet, sampling_rate)
    return coefficients, frequencies

def plot_wavelet_transform(coefficients, frequencies, sampling_rate, data_length):
    """Plot the wavelet transform as a power spectrum."""
    plt.figure(figsize=(10, 6))
    plt.imshow(
        np.abs(coefficients),
        extent=[0, data_length / sampling_rate, frequencies[-1], frequencies[0]],
        cmap='seismic',
        aspect='auto',
        interpolation='bilinear'
    )
    plt.colorbar(label='Energy')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Wavelet Transform (Power Spectrum)')
    plt.grid()
    plt.show()

def plot_wavelet_spectrum(coefficients, frequencies):
    """Plot the average wavelet power spectrum."""
    power = np.abs(coefficients) ** 2
    mean_power = np.mean(power, axis=1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, mean_power)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Energy')
    plt.title('Wavelet Power Spectrum')
    plt.grid()
    plt.show()

def analyze_sac_wavelet(sac_file, wavelet='morl', scales_range=(1, 100)):
    """Main function to load, analyze, and plot SAC waveform and wavelet transform."""
    data, sampling_rate = load_sac_file(sac_file)
    
    # Plot original waveform
    plot_waveform(data, sampling_rate)
    
    # Compute wavelet transform
    coefficients, frequencies = compute_wavelet_transform(data, sampling_rate, wavelet, scales_range)
    
    # Plot wavelet transform
    plot_wavelet_transform(coefficients, frequencies, sampling_rate, len(data))
    
    # Plot wavelet power spectrum
    plot_wavelet_spectrum(coefficients, frequencies)

# Example usage
sac_file_path = r"H:\github\personal-code-library\SAC_process\2024-01-24-11-17-19-out0012.sac"

# Plot wavelet function
plot_wavelet_function(wavelet='morl')

# Analyze SAC file with wavelet transform
analyze_sac_wavelet(sac_file_path, wavelet='morl', scales_range=(1, 100))
