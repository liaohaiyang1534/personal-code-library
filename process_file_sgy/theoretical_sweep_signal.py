import numpy as np
from scipy.signal import chirp
import matplotlib.pyplot as plt
from obspy.core import Trace, Stream, UTCDateTime
from obspy import read

def generate_sweep_signal(freq_start, freq_end, duration, sampling_rate):
    """Generate sweep signal."""
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    signal = chirp(t, f0=freq_start, f1=freq_end, t1=duration, method='linear')
    return t, signal

def save_to_sac(signal, sampling_rate, file_name):
    """Save signal to SAC file."""
    header = {
        'delta': 1 / sampling_rate,
        'npts': len(signal),
        'station': 'TEST',
        'starttime': UTCDateTime(2023, 1, 1)
    }
    tr = Trace(data=signal, header=header)
    st = Stream(traces=[tr])
    st.write(file_name, format='SAC')

# Parameters
freq_start = 20  # Start frequency 20 Hz
freq_end = 80    # End frequency 80 Hz
duration = 10    # Duration 10 seconds
sampling_rate = 500  # Sampling rate 500 Hz

# Generate sweep signal
t, signal = generate_sweep_signal(freq_start, freq_end, duration, sampling_rate)

# Save to SAC file
sac_file_name = r"H:\github\personal-code-library\SAC_process\2024-01-24-11-17-19-out0012.sac"
save_to_sac(signal, sampling_rate, sac_file_name)

def plot_saved_sac(file_name):
    """Read and plot signal from SAC file."""
    st = read(file_name)
    tr = st[0]
    data = tr.data
    sampling_rate = tr.stats.sampling_rate
    t = np.arange(0, len(data)) / sampling_rate

    plt.figure(figsize=(10, 5))
    plt.plot(t, data)
    plt.title('Sweep Signal from SAC File')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()

# Example usage
sac_file_path = sac_file_name
plot_saved_sac(sac_file_path)
