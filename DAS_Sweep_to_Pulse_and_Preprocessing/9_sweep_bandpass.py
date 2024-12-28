import segyio
import numpy as np
from scipy.signal import butter, filtfilt
import sys
import shutil
import os

# Check for required command-line arguments
if len(sys.argv) < 5:
    print("Error: Insufficient arguments. Required: file_path, lowcut, highcut, fs, order")
    sys.exit(1)

file_path = sys.argv[1]
lowcut = float(sys.argv[2])
highcut = float(sys.argv[3])
fs = float(sys.argv[4])  # Sampling rate provided as an argument
order = 3  # Default filter order

# Butterworth bandpass filter
def bandpass_filter(data, lowcut, highcut, fs, order=3):
    """
    Apply a Butterworth bandpass filter to the data.

    Args:
        data (array): The seismic trace data to filter.
        lowcut (float): Low cut-off frequency (Hz).
        highcut (float): High cut-off frequency (Hz).
        fs (float): Sampling rate (Hz).
        order (int): Order of the Butterworth filter.

    Returns:
        array: Filtered data.
    """
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

def process_sgy_file(original_file_path, lowcut, highcut, fs):
    """
    Apply a bandpass filter to all traces in a SEG-Y file.

    Args:
        original_file_path (str): Path to the original SEG-Y file.
        lowcut (float): Low cut-off frequency (Hz).
        highcut (float): High cut-off frequency (Hz).
        fs (float): Sampling rate (Hz).
    """
    # Construct new file name by appending '_band' and copy the original file
    new_file_path = original_file_path.rsplit('.', 1)[0] + '_band.sgy'
    shutil.copy(original_file_path, new_file_path)

    with segyio.open(new_file_path, "r+", ignore_geometry=True) as f:
        # Apply the bandpass filter to each trace
        for trace_index in range(len(f.trace)):
            f.trace[trace_index] = bandpass_filter(f.trace[trace_index], lowcut, highcut, fs)
        print(f"Processed {len(f.trace)} traces in the file.")

    print(f"Processed file saved as: {new_file_path}")

# Call the processing function
process_sgy_file(file_path, lowcut, highcut, fs)
