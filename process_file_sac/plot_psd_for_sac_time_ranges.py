# -*- encoding: utf-8 -*-
'''
@File        :   plot_psd_for_sac_time_ranges.py
@Time        :   2025/01/03 22:43:36
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import matplotlib.pyplot as plt
import numpy as np
from obspy import read
from scipy.signal import welch
from datetime import datetime

def generate_time_ranges(trace, num_segments=2, percentage=5):
    """
    Automatically generate time ranges based on percentage of total trace time.
    
    Parameters:
        trace: ObsPy trace object.
        num_segments: Number of segments to select from the beginning and end.
        percentage: Percentage of total time for each segment.
    
    Returns:
        A list of time ranges (start, end).
    """
    total_time = trace.stats.npts / trace.stats.sampling_rate  # Total time in seconds
    segment_duration = total_time * (percentage / 100)  # Duration of each segment
    time_ranges = []
    
    # Generate start and end times for the first few segments
    for i in range(num_segments):
        start = i * segment_duration / 3600  # Convert seconds to hours
        end = (i + 1) * segment_duration / 3600
        time_ranges.append((start, end))
    
    # Generate start and end times for the last few segments
    for i in range(num_segments):
        start = (total_time - (i + 1) * segment_duration) / 3600
        end = (total_time - i * segment_duration) / 3600
        time_ranges.insert(0, (start, end))  # Insert at the beginning for proper order
    
    return time_ranges

def plot_psd_for_time_ranges(sac_file_path, time_ranges=None, num_segments=2, percentage=5, 
                            nperseg=100000, freq_min=0.1, freq_max=45, savefig=True):
    """
    Compute and plot the Power Spectral Density (PSD) for given time ranges.
    
    Parameters:
        sac_file_path: Path to the SAC file.
        time_ranges: A list of tuples with start and end times, e.g., [(6, 7), (12, 13)].
        num_segments: Number of segments to select from the beginning and end (if time_ranges is None).
        percentage: Percentage of total time for each segment (if time_ranges is None).
        nperseg: Length of each segment for the Welch method.
        freq_min: Minimum frequency of the range.
        freq_max: Maximum frequency of the range.
        savefig: Whether to save the figure.
    """
    st = read(sac_file_path)
    trace = st[0]

    # Automatically generate time ranges if not provided
    if time_ranges is None:
        time_ranges = generate_time_ranges(trace, num_segments=num_segments, percentage=percentage)

    fig, ax = plt.subplots(figsize=(8, 4.8))

    # Initialize min and max PSD values
    min_psd = float('inf')
    max_psd = float('-inf')

    for start, end in time_ranges:
        # Validate time range
        if start < 0 or end > 24 or start >= end:
            raise ValueError("Invalid time range. Please check the input.")

        # Calculate start and end sample indices
        start_sample = int((start * 3600) * trace.stats.sampling_rate)
        end_sample = int((end * 3600) * trace.stats.sampling_rate)

        # Extract data for the corresponding time range
        data_segment = trace.data[start_sample:end_sample]

        # Compute Power Spectral Density
        freqs, psd = welch(data_segment, fs=trace.stats.sampling_rate, nperseg=nperseg)

        # Filter the PSD data within the given frequency range
        mask = (freqs >= freq_min) & (freqs <= freq_max)
        if np.sum(mask) == 0:
            # Skip this range if no frequencies are in the specified range
            print(f"Warning: No data within frequency range {freq_min}-{freq_max} Hz for time range {start}:00-{end}:00")
            continue

        # Update global min and max PSD values
        current_min_psd = np.min(psd[mask])
        current_max_psd = np.max(psd[mask])
        min_psd = min(min_psd, current_min_psd)
        max_psd = max(max_psd, current_max_psd)

        # Plot the PSD curve
        ax.plot(freqs[mask], psd[mask], label=f"{start:.2f}h-{end:.2f}h")

    # Set axis labels and limits
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('PSD (Count^2/Hz)')
    ax.set_xlim(freq_min, freq_max)
    if min_psd < max_psd:  # Only set limits if valid data exists
        ax.set_ylim(min_psd, max_psd)
    else:
        print("Warning: No valid PSD data to plot.")

    ax.set_yscale('log')  # Set y-axis to logarithmic scale
    ax.legend()

    # Set title
    plt.title(f"{os.path.basename(sac_file_path)} Power Spectral Density")

    if savefig:
        # Extract the input filename for the output file and add a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = os.path.splitext(os.path.basename(sac_file_path))[0] + "_" + timestamp + ".png"
        output_path = os.path.join(os.path.dirname(sac_file_path), output_filename)
        plt.savefig(output_path, dpi=1000)
        print(f"Figure saved at {output_path}")

    plt.show()

# Example usage
sac_file_path = r"H:\github\personal-code-library\SAC_process\2024-01-24-11-17-19-out0012.sac"

# Example with auto-generated time ranges
plot_psd_for_time_ranges(sac_file_path, num_segments=2, percentage=5, freq_min=0.1, freq_max=45)

# Example with manually specified time ranges
manual_time_ranges = [(6, 7), (12, 13)]
plot_psd_for_time_ranges(sac_file_path, time_ranges=manual_time_ranges, freq_min=0.1, freq_max=45)
