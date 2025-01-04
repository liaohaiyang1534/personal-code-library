# -*- encoding: utf-8 -*-
'''
@File        :   extra_specific_time_and_trace_of_sgy.py
@Time        :   2025/01/03 22:45:26
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import segyio
import matplotlib.pyplot as plt
import numpy as np
import os


def plot_segy(filename, title):
    with segyio.open(filename, "r", ignore_geometry=True) as f:
        data = segyio.tools.collect(f.trace[:])
        times = f.samples
        trace_indexes = np.arange(1, f.tracecount + 1)  # Actual trace numbers

    fig, ax = plt.subplots(figsize=(10, 6))
    trace_spacing = 2  # Adjust trace offset as needed

    for idx, trace in enumerate(data):
        actual_trace_number = trace_indexes[idx]
        ax.plot(trace + actual_trace_number * trace_spacing, times, '-k', lw=0.5)

    ax.set_ylim(times[-1], times[0])  # Reverse the y-axis
    ax.set_title(title)
    ax.set_xlabel('Actual Trace Number')
    ax.set_ylabel('Time (ms)')

    # Select trace numbers ending in 5 or 0, also include the first and last trace
    ticks_to_show = [num for num in trace_indexes if num % 10 == 5 or num % 10 == 0 or num == 1 or num == f.tracecount]

    # Ensure the last trace is included if not already
    if f.tracecount not in ticks_to_show:
        ticks_to_show.append(f.tracecount)

    ax.set_xticks([x * trace_spacing for x in ticks_to_show])
    ax.set_xticklabels(ticks_to_show)

    plt.tight_layout()
    plt.show()


def copy_trace_time_range(src_filename, dst_filename, start_trace, end_trace, start_time, end_time):
    if start_trace > end_trace:
        print("Start trace must be less than or equal to end trace.")
        return

    if start_time > end_time:
        print("Start time must be less than or equal to end time.")
        return

    with segyio.open(src_filename, "r", ignore_geometry=True) as src:
        if start_trace < 1 or end_trace > src.tracecount:
            print(f"Invalid trace range. File contains {src.tracecount} traces.")
            return

        # Get time-related information
        sample_interval = src.bin[segyio.BinField.Interval] / 1_000_000  # Convert microseconds to seconds
        num_samples = src.bin[segyio.BinField.Samples]
        recording_length = num_samples * sample_interval  # Total recording length in seconds

        if start_time < 0 or end_time > recording_length:
            print(f"Invalid time range. Data contains {recording_length} seconds.")
            return

        # Round start_time and end_time to the nearest sampling interval
        start_time = round(start_time / sample_interval) * sample_interval
        end_time = round(end_time / sample_interval) * sample_interval

        # Recalculate start and end sample indices
        start_sample = int(start_time / sample_interval)
        end_sample = int(end_time / sample_interval)
        num_output_samples = end_sample - start_sample

        # Update metadata
        spec = segyio.tools.metadata(src)
        # Use np.linspace to ensure start and end samples are included
        spec.samples = np.linspace(start_time, end_time, num_output_samples, endpoint=False)
        spec.tracecount = end_trace - start_trace + 1

        with segyio.create(dst_filename, spec) as dst:
            dst.text[0] = src.text[0]
            dst.bin = src.bin
            dst.bin[segyio.BinField.Samples] = len(spec.samples)

            for i in range(start_trace - 1, end_trace):
                # Extract and save trace data for the specified time range
                dst.trace[i - start_trace + 1] = src.trace[i][start_sample:end_sample]
                dst.header[i - start_trace + 1] = src.header[i]
                dst.header[i - start_trace + 1] = {segyio.TraceField.TRACE_SEQUENCE_LINE: i - start_trace + 2}

    print(f"Copied traces {start_trace} to {end_trace} from {src_filename} to {dst_filename} within time range {start_time} to {end_time} seconds.")


# Source file path
src_filename = r"H:\github\personal-code-library\SGY_process\2024-05-07-18-19-28.000_24.851_output.sgy"

# Extract directory and base name of the source file
src_dir, src_basename = os.path.split(src_filename)
src_name_without_ext, ext = os.path.splitext(src_basename)

# Generate a new file name and construct the full path
dst_basename = f"{src_name_without_ext}_modified{ext}"
dst_filename = os.path.join(src_dir, dst_basename)

# Define the range of traces to copy
start_trace = 1
end_trace = 10

# Define the time range to copy (in seconds)
start_time = 0
end_time = 0.1

# Call the function
copy_trace_time_range(src_filename, dst_filename, start_trace, end_trace, start_time, end_time)

# Plot the original and cropped SEGY files
plot_segy(src_filename, 'Original SEGY')
plot_segy(dst_filename, 'Modified SEGY (Time and Trace Cropped)')
