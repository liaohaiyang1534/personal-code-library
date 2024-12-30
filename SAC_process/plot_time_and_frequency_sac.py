import os
import numpy as np
import matplotlib.pyplot as plt
from obspy import read

plt.switch_backend('agg')

def plot_waveform_and_spectrum(sac_file_path):
    base_name = os.path.splitext(os.path.basename(sac_file_path))[0]
    output_dir = os.path.dirname(sac_file_path)
    image_path = os.path.join(output_dir, f'{base_name}_spectra.png')

    stream = read(sac_file_path)
    trace = stream[0]

    spectra_sum = None

    for tr in stream:
        fft = np.fft.rfft(tr.data)
        amplitude_spectrum = np.abs(fft)

        if spectra_sum is None:
            spectra_sum = amplitude_spectrum
        else:
            spectra_sum += amplitude_spectrum

    avg_spectra = spectra_sum / len(stream)
    freq = np.fft.rfftfreq(len(trace.data), d=trace.stats.delta)

    mask = (freq >= 1) & (freq <= 100)
    freq = freq[mask]
    avg_spectra = avg_spectra[mask]

    fig, axs = plt.subplots(2, 1, figsize=(20, 18))

    axs[0].plot(trace.times(), trace.data)
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Amplitude')
    axs[0].set_title('Original Waveform')
    axs[0].set_xlim([0, 1])

    axs[1].plot(freq, avg_spectra)
    axs[1].set_xlabel('Frequency (Hz)')
    axs[1].set_ylabel('Amplitude')
    axs[1].set_title('Frequency Spectrum')

    plt.tight_layout()
    plt.savefig(image_path)
    plt.close()

    print("\nSAC Header Information:")
    for key, value in trace.stats.sac.items():
        print(f"{key}: {value}")

    print(f"Spectrum plot saved as {image_path}")

sac_file_path = r"H:\\sym\\raw_data\\2024-01-24\\2024-01-24-11-07-19-out\\2024-01-24-11-07-19-out0005.sac"
plot_waveform_and_spectrum(sac_file_path)
