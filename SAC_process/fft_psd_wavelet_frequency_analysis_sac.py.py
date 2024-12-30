import os
import numpy as np
import matplotlib.pyplot as plt
import pywt
from scipy import signal
from obspy import read
from scipy.signal import welch, butter, sosfilt
from scipy.interpolate import interp1d

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], analog=False, btype='band', output='sos')
    y = sosfilt(sos, data)
    return y

def compute_spectrum(tr):
    npts = tr.stats.npts
    dt = tr.stats.delta
    spectrum = np.abs(np.fft.rfft(tr.data))
    frequencies = np.fft.rfftfreq(npts, dt)
    return frequencies, spectrum

def spectral_subtraction(tr, noise_spectrum, noise_freqs):
    signal_spectrum = np.fft.rfft(tr.data)
    signal_freqs = np.fft.rfftfreq(tr.stats.npts, tr.stats.delta)
    interpolator = interp1d(noise_freqs, noise_spectrum, bounds_error=False, fill_value=0)
    interpolated_noise_spectrum = interpolator(signal_freqs)
    reduced_spectrum = signal_spectrum - interpolated_noise_spectrum
    reduced_spectrum[reduced_spectrum < 0] = 0
    denoised_data = np.fft.irfft(reduced_spectrum)
    return denoised_data

def plot_psd(tr, fs, ax, title='Power Spectral Density'):
    nperseg = len(tr) if len(tr) < 1024 else 1024
    noverlap = nperseg // 2
    f, Pxx = welch(tr, fs=fs, nperseg=nperseg, noverlap=noverlap)
    ax.semilogy(f, Pxx)
    ax.set_title(title)
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('PSD [V**2/Hz]')

def wavelet_denoising(data, wavelet='sym4', maxlev=None, threshold_factor=0.04):
    w = pywt.Wavelet(wavelet)
    maxlev = maxlev if maxlev is not None else pywt.dwt_max_level(len(data), w.dec_len)
    coeffs = pywt.wavedec(data, wavelet, level=maxlev)
    threshold = threshold_factor * max([max(c) for c in coeffs[1:]])
    for i in range(1, len(coeffs)):
        coeffs[i] = pywt.threshold(coeffs[i], threshold)
    return pywt.waverec(coeffs, wavelet)

def plot_waveforms_and_spectra(sac_file_path, low_frequency, high_frequency, noise_start, noise_end, start_time, end_time):
    st = read(sac_file_path)
    tr_original = st[0].copy()
    tr_original.data = tr_original.data - np.mean(tr_original.data)
    fs = 1 / tr_original.stats.delta

    filtered_data = bandpass_filter(tr_original.data, low_frequency, high_frequency, fs)
    tr_filtered = tr_original.copy()
    tr_filtered.data = filtered_data

    noise_tr = tr_original.slice(starttime=tr_original.stats.starttime + noise_start, 
                                 endtime=tr_original.stats.starttime + noise_end)
    noise_freqs, noise_spectrum = compute_spectrum(noise_tr)

    denoised_data = spectral_subtraction(tr_original, noise_spectrum, noise_freqs)
    tr_denoised = tr_original.copy()
    tr_denoised.data = denoised_data

    tr_wavelet_denoised = tr_original.copy()
    tr_wavelet_denoised.data = wavelet_denoising(tr_original.data)

    start = tr_original.stats.starttime + start_time
    end = tr_original.stats.starttime + end_time
    tr_sliced = tr_denoised.slice(starttime=start, endtime=end)

    actual_times = tr_sliced.times() + start_time

    # Plotting section
    fig, axs = plt.subplots(4, 3, figsize=(20, 25))

    # Original signal plots
    axs[0,0].plot(tr_original.times(), tr_original.data)
    axs[0,0].set_title('Original Waveform')
    frequencies_orig, spectrum_orig = compute_spectrum(tr_original)
    axs[0,1].plot(frequencies_orig, spectrum_orig)
    axs[0,1].set_title('Original Spectrum')
    plot_psd(tr_original.data, fs, axs[0,2], title='Original Signal PSD')

    # Bandpass filtered signal plots
    axs[1,0].plot(tr_filtered.times(), tr_filtered.data)
    axs[1,0].set_title(f'Band-Pass Filtered Waveform ({low_frequency}Hz-{high_frequency}Hz)')
    frequencies_filtered, spectrum_filtered = compute_spectrum(tr_filtered)
    axs[1,1].plot(frequencies_filtered, spectrum_filtered)
    axs[1,1].set_title(f'Filtered Spectrum ({low_frequency}-{high_frequency}Hz)')
    plot_psd(tr_filtered.data, fs, axs[1,2], title=f'Filtered Signal PSD ({low_frequency}-{high_frequency}Hz)')

    # Denoised signal plots
    axs[2,0].plot(tr_denoised.times(), tr_denoised.data)
    axs[2,0].set_title('Spectral Subtraction Denoised Waveform')
    frequencies_denoised, spectrum_denoised = compute_spectrum(tr_denoised)
    axs[2,1].plot(frequencies_denoised, spectrum_denoised)
    axs[2,1].set_title('Denoised Spectrum')
    plot_psd(tr_denoised.data, fs, axs[2,2], title='Denoised Signal PSD')

    # Wavelet denoised signal plots
    axs[3,0].plot(tr_wavelet_denoised.times(), tr_wavelet_denoised.data)
    axs[3,0].set_title('Wavelet Denoised Waveform')
    frequencies_wavelet_denoised, spectrum_wavelet_denoised = compute_spectrum(tr_wavelet_denoised)
    axs[3,1].plot(frequencies_wavelet_denoised, spectrum_wavelet_denoised)
    axs[3,1].set_title('Wavelet Denoised Spectrum')
    plot_psd(tr_wavelet_denoised.data, fs, axs[3,2], title='Wavelet Denoised Signal PSD')

    plt.tight_layout()
    plt.show()

# Parameters for the analysis
sac_file_path = r"E:\lhyonedrive\OneDrive\Desktop\baiyi\2024-07-11-00-00-33-out\2024-07-11-00-00-33-out0101.sac"
low_frequency = 20
high_frequency = 80
noise_start = 0
noise_end = 3
start_time = 3.83
end_time = 3.9

# Run the analysis
plot_waveforms_and_spectra(sac_file_path, low_frequency, high_frequency, noise_start, noise_end, start_time, end_time)
