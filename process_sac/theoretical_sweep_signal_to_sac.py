import numpy as np
from scipy.signal import chirp, stft
import matplotlib.pyplot as plt
from obspy.core import Trace, Stream, UTCDateTime
from obspy import read
import os
import matplotlib

# Set non-interactive backend for matplotlib
matplotlib.use('agg')

def generate_sweep_signal(freq_start, freq_end, duration, sampling_rate):
    """Generate a sweep signal."""
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    signal = chirp(t, f0=freq_start, f1=freq_end, t1=duration, method='linear')
    return t, signal

def save_to_sac(signal, sampling_rate, file_name):
    """Save signal to a SAC file."""
    header = {
        'delta': 1 / sampling_rate,
        'npts': len(signal),
        'station': 'TEST',
        'starttime': UTCDateTime(2023, 1, 1)
    }
    tr = Trace(data=signal, header=header)
    st = Stream(traces=[tr])
    st.write(file_name, format='SAC')

def plot_stft(sac_file, window='hann', nperseg=256, noverlap=128, time_range=None, freq_range=None):
    """Plot the short-time Fourier transform (STFT) of the signal."""
    st = read(sac_file)
    tr = st[0]
    data = tr.data
    sampling_rate = tr.stats.sampling_rate

    f, t, Zxx = stft(data, fs=sampling_rate, window=window, nperseg=nperseg, noverlap=noverlap)

    plt.figure(figsize=(10, 6))
    plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
    plt.title('STFT Magnitude')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [s]')
    if time_range:
        plt.xlim(time_range)
    if freq_range:
        plt.ylim(freq_range)
    plt.colorbar(label='Magnitude')

    folder_path = os.path.dirname(sac_file)
    plt.savefig(os.path.join(folder_path, 'time_and_frequency_analysis.png'))
    plt.close()

def plot_waveform_and_spectrum(sac_file):
    """Plot the waveform and frequency spectrum of the signal."""
    st = read(sac_file)
    tr = st[0]
    data = tr.data
    npts = tr.stats.npts
    sampling_rate = tr.stats.sampling_rate
    sample_interval = 1 / sampling_rate
    folder_path = os.path.dirname(sac_file)

    # Plot waveform
    time = np.arange(0, npts) / sampling_rate
    plt.figure(figsize=(20, 5), dpi=50)
    plt.plot(time * 1000, data)  # Convert time to milliseconds
    plt.title(f'Waveform - Fs: {sampling_rate:.2f} Hz')
    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude')
    plt.savefig(os.path.join(folder_path, 'waveform.png'))
    plt.close()

    # Compute frequency spectrum
    freqs = np.fft.rfftfreq(npts, d=sample_interval)
    spectrum = np.fft.rfft(data)

    # Plot frequency spectrum
    plt.figure(figsize=(10, 5), dpi=50)
    plt.plot(freqs, np.abs(spectrum))
    plt.title(f'Frequency Spectrum - Fs: {sampling_rate:.2f} Hz')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim([0, 100])  # Limit X-axis to 100 Hz
    plt.savefig(os.path.join(folder_path, 'spectrum.png'))
    plt.close()

# Parameters
freq_start = 20  # Start frequency (Hz)
freq_end = 80    # End frequency (Hz)
duration = 10    # Duration (seconds)
sampling_rate = 500  # Sampling rate (Hz)

# Generate sweep signal
t, signal = generate_sweep_signal(freq_start, freq_end, duration, sampling_rate)

# Save to SAC file
sac_file_name = r"E:\student_work\lhy\onedrive\OneDrive - Nanjing University\Masters\code\TEMP files\sweep_signal.sac"
save_to_sac(signal, sampling_rate, sac_file_name)

# Perform time-frequency analysis and plot
sac_file_path = sac_file_name
time_range = None  # Set to None to disable time range restriction
freq_range = (1, 100)  # Restrict frequency range to 1-100 Hz
plot_stft(sac_file_path, time_range=time_range, freq_range=freq_range)

# Plot waveform and spectrum
plot_waveform_and_spectrum(sac_file_path)







