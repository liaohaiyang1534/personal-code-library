import segyio
import os
import numpy as np
import sys

# Get the directory path and time range from command line arguments
if len(sys.argv) > 3:
    root_folder = sys.argv[1]
    start_time = float(sys.argv[2])
    end_time = float(sys.argv[3])
else:
    print("Error: Directory path and time range not provided.")
    sys.exit(1)

print(f"Processing directory: {root_folder}")

max_depth = 4

def copy_time_range(src_filename, dst_filename, start_time, end_time):
    with segyio.open(src_filename, "r", ignore_geometry=True) as src:
        # Time-related information
        sample_interval = src.bin[segyio.BinField.Interval] / 1_000_000  # Convert microseconds to seconds
        num_samples = src.bin[segyio.BinField.Samples]
        recording_length = num_samples * sample_interval  # Total recording length in seconds

        if start_time < 0 or end_time > recording_length:
            print(f"Invalid time range. Data contains {recording_length} seconds.")
            return

        # Round start_time and end_time to the nearest sample interval
        start_time = round(start_time / sample_interval) * sample_interval
        end_time = round(end_time / sample_interval) * sample_interval

        # Recalculate the start and end sample indices
        start_sample = int(start_time / sample_interval)
        end_sample = int(end_time / sample_interval)
        num_output_samples = end_sample - start_sample

        # Update metadata
        spec = segyio.tools.metadata(src)
        spec.samples = np.linspace(start_time, end_time, num_output_samples, endpoint=False)
        spec.tracecount = src.tracecount

        with segyio.create(dst_filename, spec) as dst:
            dst.text[0] = src.text[0]
            dst.bin = src.bin
            dst.bin[segyio.BinField.Samples] = len(spec.samples)

            for i in range(src.tracecount):
                dst.trace[i] = src.trace[i][start_sample:end_sample]
                dst.header[i] = src.header[i]
                dst.header[i][segyio.TraceField.TRACE_SEQUENCE_LINE] = i + 1

        print(f"Copied all traces from {src_filename} to {dst_filename} within time range {start_time} to {end_time} seconds.")

def process_sgy_file(sgy_file_path, start_time, end_time):
    # Define the output filename based on the input path
    src_dir, src_basename = os.path.split(sgy_file_path)
    src_name_without_ext, ext = os.path.splitext(src_basename)
    dst_basename = f"{src_name_without_ext}_time_cropped{ext}"
    dst_filename = os.path.join(src_dir, dst_basename)

    # Perform the time range extraction
    copy_time_range(sgy_file_path, dst_filename, start_time, end_time)

def process_folder(root_folder, max_depth):
    for subdir, dirs, files in os.walk(root_folder):
        if subdir.count(os.sep) - root_folder.count(os.sep) >= max_depth:
            continue
        for file in files:
            if file == "to_1028_reversed.sgy":
                original_file_path = os.path.join(subdir, file)
                process_sgy_file(original_file_path, start_time, end_time)

    for subdir, dirs, files in os.walk(root_folder):
        if subdir.count(os.sep) - root_folder.count(os.sep) >= max_depth:
            continue
        for file in files:
            if file == "to_1267.sgy":
                original_file_path = os.path.join(subdir, file)
                process_sgy_file(original_file_path, start_time, end_time)

# Main logic
process_folder(root_folder, max_depth)
