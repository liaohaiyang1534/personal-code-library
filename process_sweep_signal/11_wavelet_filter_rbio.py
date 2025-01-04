# -*- encoding: utf-8 -*-
'''
@File        :   11_wavelet_filter_rbio.py
@Time        :   2025/01/03 22:52:51
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import segyio
import numpy as np
import matplotlib.pyplot as plt
import pywt
import shutil
import matplotlib
matplotlib.use('agg')
import sys

# Define file paths
input_file_path = sys.argv[1]
output_file_path = input_file_path.replace('.sgy', '_wavelet.sgy')

# Read SEG-Y file
def read_segy(file_path):
    with segyio.open(file_path, "r", ignore_geometry=True) as segyfile:
        segyfile.mmap()
        data = segyio.tools.collect(segyfile.trace[:])
        return np.array(data)

# Apply wavelet filtering
def wavelet_filter(data, wavelet='rbio1.1', level=6, mode='soft', method='universal'):
    coeffs = pywt.wavedec2(data, wavelet, level=level)
    thresholded_coeffs = []
    
    for i, coeff in enumerate(coeffs):
        if i == 0:
            sigma = np.median(np.abs(coeff)) / 0.6745
            threshold = sigma * np.sqrt(2 * np.log(data.size))
        else:
            sigma = np.median(np.abs(coeff[2])) / 0.6745
            threshold = sigma * (np.sqrt(2 * np.log(data.size)) / (i**2))
        
        if isinstance(coeff, tuple):
            cH, cV, cD = coeff
            cH_t = pywt.threshold(cH, threshold, mode=mode)
            cV_t = pywt.threshold(cV, threshold, mode=mode)
            cD_t = pywt.threshold(cD, threshold, mode=mode)
            thresholded_coeffs.append((cH_t, cV_t, cD_t))
        else:
            cA_t = pywt.threshold(coeff, threshold, mode=mode)
            thresholded_coeffs.append(cA_t)
    
    filtered_data = pywt.waverec2(thresholded_coeffs, wavelet)
    return filtered_data

# Save filtered data to a new SEG-Y file
def save_filtered_segy(input_file, output_file, filtered_data):
    shutil.copy(input_file, output_file)

    with segyio.open(output_file, "r+", ignore_geometry=True) as segyfile:
        segyfile.mmap()
        for i, trace in enumerate(filtered_data):
            segyfile.trace[i] = trace

# Plot TX domain data
def plot_tx_data(original_data, filtered_data):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
    ax1.imshow(original_data.T, cmap='gray', aspect='auto')
    ax1.set_title('Original Data')
    ax1.set_xlabel('Trace')
    ax1.set_ylabel('Time Sample')
    ax2.imshow(filtered_data.T, cmap='gray', aspect='auto')
    ax2.set_title('Wavelet Filtered Data')
    ax2.set_xlabel('Trace')
    plt.savefig('TX_plots.png')

# Normalize function
def normalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

# Plot normalized wavelet coefficients (2x2 layout)
def plot_wavelet_coeffs(data, wavelet='rbio1.1', level=3):
    coeffs = pywt.wavedec2(data.T, wavelet, level=level)
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
    cmap = plt.get_cmap('gray')
    for i, coeff in enumerate(coeffs):
        if i > 3:
            break
        row, col = divmod(i, 2)
        if i == 0:
            coeff_norm = normalize(coeff)
            axes[row, col].imshow(coeff_norm, cmap=cmap, aspect='auto')
            axes[row, col].set_title(f'Normalized Approximation Coefficients at Level {i}')
        else:
            cH, cV, cD = coeff
            coeff_norm = normalize(np.hstack((cH, cV, cD)))
            axes[row, col].imshow(coeff_norm, cmap=cmap, aspect='auto')
            axes[row, col].set_title(f'Normalized Detail Coefficients at Level {i}')
    plt.tight_layout()
    plt.savefig('normalized_wavelet_coeffs.png')

# Plot normalized thresholded wavelet coefficients (2x2 layout)
def plot_thresholded_wavelet_coeffs(data, wavelet='rbio1.1', level=3, mode='soft', method='universal'):
    coeffs = pywt.wavedec2(data.T, wavelet, level=level)
    thresholded_coeffs = []
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
    cmap = plt.get_cmap('gray')
    for i, coeff in enumerate(coeffs):
        if i > 3:
            break
        row, col = divmod(i, 2)
        if i == 0:
            sigma = np.median(np.abs(coeff)) / 0.6745
            threshold = sigma * np.sqrt(2 * np.log(data.size))
        else:
            sigma = np.median(np.abs(coeff[2])) / 0.6745
            threshold = sigma * (np.sqrt(2 * np.log(data.size)) / (i**2))
        if isinstance(coeff, tuple):
            cH, cV, cD = coeff
            cH_t = pywt.threshold(cH, threshold, mode=mode)
            cV_t = pywt.threshold(cV, threshold, mode=mode)
            cD_t = pywt.threshold(cD, threshold, mode=mode)
            thresholded_coeffs.append((cH_t, cV_t, cD_t))
            coeff_norm = normalize(np.hstack((cH_t, cV_t, cD_t)))
            axes[row, col].imshow(coeff_norm, cmap=cmap, aspect='auto')
        else:
            cA_t = pywt.threshold(coeff, threshold, mode=mode)
            thresholded_coeffs.append(cA_t)
            coeff_norm = normalize(cA_t)
            axes[row, col].imshow(coeff_norm, cmap=cmap, aspect='auto')
        axes[row, col].set_title(f'Normalized Thresholded Coefficients at Level {i}')
    plt.tight_layout()
    plt.savefig('normalized_thresholded_coeffs.png')

# Read data
seismic_data = read_segy(input_file_path)

# Apply wavelet filtering
filtered_seismic_data = wavelet_filter(seismic_data)

# Save filtered data to a new SEG-Y file
save_filtered_segy(input_file_path, output_file_path, filtered_seismic_data)

# Output result
print("Output file saved as:", output_file_path)
