# -*- encoding: utf-8 -*-
'''
@File        :   10_fk_filter.py
@Time        :   2025/01/03 22:52:45
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import numpy as np
import segyio
from scipy.fftpack import fft2, ifft2, fftshift, ifftshift
from scipy.ndimage import gaussian_filter
import os
import matplotlib
import matplotlib.pyplot as plt
import sys

# Ensure matplotlib works in headless environments
matplotlib.use('Agg')

def load_seismic_data_2d(file_path):
    """
    Load seismic data from a SEGY file.
    """
    with segyio.open(file_path, "r", ignore_geometry=True) as f:
        data = segyio.tools.collect(f.trace[:]).T
    return data

def define_filter_polygon(vmin, vmax, freq_min, freq_max, freqs, kx):
    nt = len(freqs)
    nx = len(kx)
    mask = np.zeros((nt, nx))
    for i, f in enumerate(freqs):
        for j, k in enumerate(kx):
            velocity = np.inf if k == 0 else np.abs(f / k)
            if vmin <= velocity <= vmax and freq_min <= np.abs(f) <= freq_max:
                mask[i, j] = 1
    return mask

def fk_transform_and_filter_using_predefined_mask(seismic_data, mask):
    nt, nx = seismic_data.shape
    fk_data = fftshift(fft2(seismic_data))
    fk_filtered = fk_data * mask
    seismic_filtered = np.real(ifft2(ifftshift(fk_filtered)))
    return seismic_filtered, fk_data, mask, fk_filtered

def normalize_traces(data):
    """
    Normalize each trace to its maximum absolute value.
    """
    normalized_data = np.zeros_like(data)
    for i in range(data.shape[1]):
        trace_max = np.max(np.abs(data[:, i]))
        if trace_max > 0:
            normalized_data[:, i] = data[:, i] / trace_max
    return normalized_data

def copy_trace_headers_to_filtered_sgy(original_file_path, filtered_sgy_path):
    """
    Copy trace headers (GroupX and SourceGroupScalar) from the original SEG-Y file
    to the filtered SEG-Y file.
    """
    with segyio.open(original_file_path, "r", ignore_geometry=True) as original, \
         segyio.open(filtered_sgy_path, "r+", ignore_geometry=True) as filtered:
        for orig_trace_index, filt_trace_index in zip(range(original.tracecount), range(filtered.tracecount)):
            group_x = original.header[orig_trace_index][segyio.TraceField.GroupX]
            source_group_scalar = original.header[orig_trace_index][segyio.TraceField.SourceGroupScalar]
            filtered.header[filt_trace_index].update({
                segyio.TraceField.GroupX: group_x,
                segyio.TraceField.SourceGroupScalar: source_group_scalar
            })
    print(f"Trace headers copied from '{original_file_path}' to '{filtered_sgy_path}'.")

def save_filtered_data_to_segy(original_file_path, filtered_data, segy_output_path, dx, dt):
    with segyio.open(original_file_path, 'r', ignore_geometry=True) as src:
        n_samples_expected = len(src.samples)
        print("Expected samples per trace:", n_samples_expected)
        print("Actual samples per trace in filtered data:", filtered_data.shape[0])

        if filtered_data.shape[0] != n_samples_expected:
            adjusted_filtered_data = filtered_data[:n_samples_expected, :]
        else:
            adjusted_filtered_data = filtered_data

        adjusted_filtered_data = adjusted_filtered_data.astype(np.float32)

        spec = segyio.spec()
        spec.sorting = src.sorting
        spec.format = src.format
        spec.samples = src.samples
        spec.tracecount = adjusted_filtered_data.shape[1]

        with segyio.create(segy_output_path, spec) as dst:
            for i in range(adjusted_filtered_data.shape[1]):
                dst.trace[i] = adjusted_filtered_data[:, i]
        print(f"Filtered SEG-Y file saved to: {segy_output_path}")

def plot_six_combined(seismic_data, seismic_filtered, fk_data, fk_filtered, mask, freqs, kx, input_file_base, fmax=200):
    """
    Plot six figures to demonstrate the effect of F-K filtering in both T-X and F-K domains.
    """
    fig, axs = plt.subplots(2, 3, figsize=(18, 12))
    nt, nx = seismic_data.shape
    extent_tx = [0, nx * dx, nt * dt * 1000, 0]

    fk_data_log = 20 * np.log10(np.abs(fk_data) + np.finfo(float).eps)
    fk_filtered_log = 20 * np.log10(np.abs(fk_filtered) + np.finfo(float).eps)

    vmin_fk, vmax_fk = np.percentile(fk_data_log, 5), np.percentile(fk_data_log, 95)

    freqs_limited_idx = np.abs(freqs) <= fmax
    fk_data_log_limited = fk_data_log[freqs_limited_idx, :]
    fk_filtered_log_limited = fk_filtered_log[freqs_limited_idx, :]
    mask_limited = mask[freqs_limited_idx, :]

    freqs_limited = freqs[freqs_limited_idx]
    extent_fk = [kx.min(), kx.max(), freqs_limited.min(), freqs_limited.max()]

    axs[0, 0].imshow(seismic_data, aspect='auto', cmap='gray', extent=extent_tx)
    axs[0, 0].set_title('Original Data (T-X Domain)')
    axs[0, 2].imshow(seismic_filtered, aspect='auto', cmap='gray', extent=extent_tx)
    axs[0, 2].set_title('Filtered Data (T-X Domain)')

    axs[1, 0].imshow(fk_data_log_limited, aspect='auto', cmap='jet', vmin=vmin_fk, vmax=vmax_fk, extent=extent_fk, origin='lower')
    axs[1, 0].set_title('Original F-K Domain')

    axs[0, 1].imshow(mask_limited, aspect='auto', cmap='gray', extent=extent_fk, origin='lower')
    axs[0, 1].set_title('F-K Filter Mask')

    mask_alpha_limited = np.where(mask_limited > 0, 0.5, 0)
    axs[1, 1].imshow(fk_data_log_limited, aspect='auto', cmap='jet', vmin=vmin_fk, vmax=vmax_fk, extent=extent_fk, origin='lower')
    axs[1, 1].imshow(mask_alpha_limited, aspect='auto', cmap='Reds', alpha=0.5, extent=extent_fk, origin='lower')
    axs[1, 1].set_title('Original F-K with Mask Overlay')

    axs[1, 2].imshow(fk_filtered_log_limited, aspect='auto', cmap='jet', vmin=vmin_fk, vmax=vmax_fk, extent=extent_fk, origin='lower')
    axs[1, 2].set_title('Filtered F-K Domain')

    for ax in axs.flat:
        ax.set(xlabel='Wavenumber k (1/m)', ylabel='Frequency f (Hz)')

    plt.tight_layout()
    combined_plot_path = f"{input_file_base}_Filtered_vs_Original.png"
    plt.savefig(combined_plot_path)
    plt.close()
    print(f"Combined plots saved to: {combined_plot_path}")

def apply_gaussian_decay(mask, sigma=10):
    """
    Smooth the mask boundaries using a Gaussian decay function.
    """
    smoothed_mask = gaussian_filter(mask.astype(float), sigma=sigma)
    smoothed_mask = np.clip(smoothed_mask, 0, 1)
    return smoothed_mask

# Main execution
original_file_path = sys.argv[1]
seismic_data = load_seismic_data_2d(original_file_path)
dx, dt = 0.5, 0.002
vmin, vmax = 50, 3000
freq_min, freq_max = 5, 85
sigma = 10
fmax = 100
nt, nx = seismic_data.shape
freqs = fftshift(np.fft.fftfreq(nt, dt))
kx = fftshift(np.fft.fftfreq(nx, dx))

mask = define_filter_polygon(vmin, vmax, freq_min, freq_max, freqs, kx)
smoothed_mask = apply_gaussian_decay(mask, sigma=sigma)
mask = smoothed_mask

seismic_filtered, fk_data, _, fk_filtered = fk_transform_and_filter_using_predefined_mask(seismic_data, mask)

seismic_data = normalize_traces(seismic_data)
seismic_filtered = normalize_traces(seismic_filtered)

segy_output_path = original_file_path.replace('.sgy', '_fk.sgy')
save_filtered_data_to_segy(original_file_path, seismic_filtered, segy_output_path, dx, dt)
print(f"Filtered SEGY file saved to: {segy_output_path}")

input_file_base = os.path.splitext(original_file_path)[0]
plot_six_combined(seismic_data, seismic_filtered, fk_data, fk_filtered, mask, freqs, kx, input_file_base, fmax=fmax)
copy_trace_headers_to_filtered_sgy(original_file_path, segy_output_path)
