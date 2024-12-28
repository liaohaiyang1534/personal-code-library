import numpy as np
import segyio
import matplotlib.pyplot as plt
from scipy.signal import welch, periodogram
import os
import shutil

# Set matplotlib to use the Agg backend
plt.switch_backend('agg')

def plot_segy_spectra_and_save(file_path, analyze_whole_sgy=True, analyze_by_trace_group=False, trace_group_size=2):
    base_name_with_extension = os.path.basename(file_path)
    base_name = os.path.splitext(base_name_with_extension)[0]
    dir_name = os.path.join(os.path.dirname(file_path), f"{base_name}_fre_analysis")
    
    # Clear the folder
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)

    with segyio.open(file_path, "r", ignore_geometry=True) as f:
        sample_rate = segyio.tools.dt(f) / 1e6  # Sample rate in seconds
        sample_rate_hz = 1 / sample_rate  # Sample rate in Hz
        print(f"Sample rate: {sample_rate_hz} Hz")

        total_traces = f.tracecount
        spectra_sum = np.zeros(int(f.trace[0].size / 2) + 1)
        
        for trace in f.trace:
            fft = np.fft.rfft(trace)
            amplitude_spectrum = np.abs(fft)
            spectra_sum += amplitude_spectrum

        avg_spectra = spectra_sum / total_traces
        
        # Compute Nyquist frequency
        nyquist = 0.5 * sample_rate_hz
        freq = np.linspace(0, nyquist, len(avg_spectra))
        
        # Full frequency range
        mask_full = freq <= 500
        freq_full = freq[mask_full]
        avg_spectra_full = avg_spectra[mask_full]
        
        # 0-100Hz range
        mask_100 = freq <= 100
        freq_100 = freq[mask_100]
        avg_spectra_100 = avg_spectra[mask_100]

        if analyze_whole_sgy:
            # Frequency analysis for the whole SGY file
            # Plot 1: Direct frequency representation (full frequency range)
            plt.figure(figsize=(10, 6))
            plt.plot(freq_full, avg_spectra_full)
            plt.title(f"Direct Frequency Spectrum of {base_name_with_extension}", fontsize=12, fontname='Times New Roman')
            plt.xlabel("Frequency (Hz)", fontsize=12, fontname='Times New Roman')
            plt.ylabel("Amplitude", fontsize=12, fontname='Times New Roman')
            plt.grid(True)
            plt.savefig(os.path.join(dir_name, f"full_direct_spectrum_{base_name}.png"))
            plt.close()
            
            # Plot 2: Direct frequency representation (0-100Hz range)
            plt.figure(figsize=(10, 6))
            plt.plot(freq_100, avg_spectra_100)
            plt.title(f"Direct Frequency Spectrum (0-100Hz) of {base_name_with_extension}", fontsize=12, fontname='Times New Roman')
            plt.xlabel("Frequency (Hz)", fontsize=12, fontname='Times New Roman')
            plt.ylabel("Amplitude", fontsize=12, fontname='Times New Roman')
            plt.grid(True)
            plt.savefig(os.path.join(dir_name, f"0-100Hz_direct_spectrum_{base_name}.png"))
            plt.close()
            
            # Plot 3: Normalized frequency representation (full frequency range)
            norm_spectra_full = avg_spectra_full / np.max(avg_spectra_full)
            plt.figure(figsize=(10, 6))
            plt.plot(freq_full, norm_spectra_full)
            plt.title(f"Normalized Frequency Spectrum of {base_name_with_extension}", fontsize=12, fontname='Times New Roman')
            plt.xlabel("Frequency (Hz)", fontsize=12, fontname='Times New Roman')
            plt.ylabel("Normalized Amplitude", fontsize=12, fontname='Times New Roman')
            plt.grid(True)
            plt.savefig(os.path.join(dir_name, f"full_normalized_spectrum_{base_name}.png"))
            plt.close()
            
            # Plot 4: Normalized frequency representation (0-100Hz range)
            norm_spectra_100 = avg_spectra_100 / np.max(avg_spectra_100)
            plt.figure(figsize=(10, 6))
            plt.plot(freq_100, norm_spectra_100)
            plt.title(f"Normalized Frequency Spectrum (0-100Hz) of {base_name_with_extension}", fontsize=12, fontname='Times New Roman')
            plt.xlabel("Frequency (Hz)", fontsize=12, fontname='Times New Roman')
            plt.ylabel("Normalized Amplitude", fontsize=12, fontname='Times New Roman')
            plt.grid(True)
            plt.savefig(os.path.join(dir_name, f"0-100Hz_normalized_spectrum_{base_name}.png"))
            plt.close()
            
            # Plot 5: Min-Max normalized frequency representation (full frequency range)
            min_max_norm_spectra_full = (avg_spectra_full - np.min(avg_spectra_full)) / (np.max(avg_spectra_full) - np.min(avg_spectra_full))
            plt.figure(figsize=(10, 6))
            plt.plot(freq_full, min_max_norm_spectra_full)
            plt.title(f"Min-Max Normalized Spectrum of {base_name_with_extension}", fontsize=12, fontname='Times New Roman')
            plt.xlabel("Frequency (Hz)", fontsize=12, fontname='Times New Roman')
            plt.ylabel("Min-Max Normalized Amplitude", fontsize=12, fontname='Times New Roman')
            plt.grid(True)
            plt.savefig(os.path.join(dir_name, f"full_min_max_normalized_spectrum_{base_name}.png"))
            plt.close()
            
            # Plot 6: Min-Max normalized frequency representation (0-100Hz range)
            min_max_norm_spectra_100 = (avg_spectra_100 - np.min(avg_spectra_100)) / (np.max(avg_spectra_100) - np.min(avg_spectra_100))
            plt.figure(figsize=(10, 6))
            plt.plot(freq_100, min_max_norm_spectra_100)
            plt.title(f"Min-Max Normalized Spectrum (0-100Hz) of {base_name_with_extension}", fontsize=12, fontname='Times New Roman')
            plt.xlabel("Frequency (Hz)", fontsize=12, fontname='Times New Roman')
            plt.ylabel("Min-Max Normalized Amplitude", fontsize=12, fontname='Times New Roman')
            plt.grid(True)
            plt.savefig(os.path.join(dir_name, f"0-100Hz_min_max_normalized_spectrum_{base_name}.png"))
            plt.close()
            
            # Plot 7: PSD analysis using Welch method (full frequency range)
            f_welch_full, Pxx_welch_full = welch(avg_spectra_full, fs=sample_rate_hz)
            plt.figure(figsize=(10, 6))
            plt.semilogy(f_welch_full, Pxx_welch_full)
            plt.title(f"PSD Analysis (Welch Method) of {base_name_with_extension}", fontsize=12, fontname='Times New Roman')
            plt.xlabel("Frequency (Hz)", fontsize=12, fontname='Times New Roman')
            plt.ylabel("Power Spectral Density (PSD)", fontsize=12, fontname='Times New Roman')
            plt.grid(True)
            plt.savefig(os.path.join(dir_name, f"full_psd_analysis_welch_{base_name}.png"))
            plt.close()

            # Plot 8: PSD analysis using Welch method (0-100Hz range)
            f_welch_100, Pxx_welch_100 = welch(avg_spectra, fs=sample_rate_hz, nperseg=len(avg_spectra))
            mask_welch_100 = f_welch_100 <= 100
            plt.figure(figsize=(10, 6))
            plt.semilogy(f_welch_100[mask_welch_100], Pxx_welch_100[mask_welch_100])
            plt.title(f"PSD Analysis (Welch Method, 0-100Hz) of {base_name_with_extension}", fontsize=12, fontname='Times New Roman')
            plt.xlabel("Frequency (Hz)", fontsize=12, fontname='Times New Roman')
            plt.ylabel("Power Spectral Density (PSD)", fontsize=12, fontname='Times New Roman')
            plt.grid(True)
            plt.xlim(0, 100)  # Set x-axis range to 0-100Hz
            plt.savefig(os.path.join(dir_name, f"0-100Hz_psd_analysis_welch_{base_name}.png"))
            plt.close()

# Example usage
file_path = r"H:\TEMP\example_segy.sgy"
plot_segy_spectra_and_save(file_path, analyze_whole_sgy=True, analyze_by_trace_group=True, trace_group_size=2)
