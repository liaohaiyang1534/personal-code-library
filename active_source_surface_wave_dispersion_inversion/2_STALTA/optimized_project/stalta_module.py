import os
import numpy as np
import matplotlib.pyplot as plt
import segyio
from obspy.signal.trigger import classic_sta_lta
from utils import create_output_folder

def process_sgy(file_path, output_folder, params):
    """
    Process SEG-Y file to detect trigger events using STA/LTA and save results.

    Args:
        file_path (str): Path to the input SEG-Y file.
        output_folder (str): Folder to save output.
        params (dict): STA/LTA parameters (threshold, duration, etc.).

    Returns:
        None
    """
    threshold = params["threshold"]
    duration = params["duration"]

    with segyio.open(file_path, "r", ignore_geometry=True) as f:
        sample_interval = f.bin[segyio.BinField.Interval] / 1_000_000
        num_samples = f.bin[segyio.BinField.Samples]
        trace_count = f.tracecount

        sta_lta_all = np.zeros((trace_count, num_samples))
        nsta = 1
        nlta = 1000

        for i in range(trace_count):
            trace = f.trace[i]
            sta_lta_all[i] = classic_sta_lta(trace, nsta, nlta)

        sta_lta_mean = np.mean(sta_lta_all, axis=0)
        trigger_indices = np.where(sta_lta_mean > threshold)[0]
        trigger_times = trigger_indices / (1 / sample_interval)

        time_axis = np.arange(len(sta_lta_mean)) * sample_interval * 1000
        plt.plot(time_axis, sta_lta_mean)
        plt.axhline(y=threshold, color='green', linestyle='--')
        plt.savefig(os.path.join(output_folder, f"{os.path.basename(file_path)}_stalta.png"))
        plt.close()

    print(f"Triggers detected in {file_path}: {trigger_times}")

    # Call copy_time_range (logic encapsulated separately)
    for time in trigger_times:
        copy_time_range(file_path, time, duration, output_folder)


def copy_time_range(file_path, start_time, duration, output_folder):
    """
    Copy a time range from a SEG-Y file.

    Args:
        file_path (str): Path to the input SEG-Y file.
        start_time (float): Start time in seconds.
        duration (float): Duration in seconds.
        output_folder (str): Folder to save output.

    Returns:
        None
    """
    with segyio.open(file_path, "r", ignore_geometry=True) as src:
        sample_interval = src.bin[segyio.BinField.Interval] / 1_000_000
        start_sample = int(start_time / sample_interval)
        end_sample = start_sample + int(duration / sample_interval)

        output_file = os.path.join(output_folder, f"extracted_{start_time:.2f}.sgy")
        with segyio.create(output_file, segyio.tools.metadata(src)) as dst:
            dst.text[0] = src.text[0]
            dst.bin = src.bin
            for i in range(src.tracecount):
                dst.trace[i] = src.trace[i][start_sample:end_sample]

        print(f"Time range extracted and saved to {output_file}.")
