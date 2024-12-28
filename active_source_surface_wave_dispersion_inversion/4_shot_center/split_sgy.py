import segyio
import os
import sys

def copy_trace_range(src_filename, dst_filename, start_trace, end_trace):
    """
    Copy a range of traces from a source SEG-Y file to a new destination SEG-Y file.

    Parameters:
        src_filename (str): Path to the source SEG-Y file.
        dst_filename (str): Path to the destination SEG-Y file.
        start_trace (int): Starting trace index (1-based).
        end_trace (int): Ending trace index (1-based).
    """
    try:
        with segyio.open(src_filename, "r", ignore_geometry=True) as src:
            trace_count = src.tracecount
            if start_trace < 1 or end_trace > trace_count:
                print(f"Invalid trace range. The file contains {trace_count} traces.")
                return

            print(f"Copying traces from {start_trace} to {end_trace} from {src_filename} to {dst_filename}")
            
            # Define the metadata for the new SEG-Y file
            spec = segyio.tools.metadata(src)
            spec.tracecount = end_trace - start_trace + 1

            with segyio.create(dst_filename, spec) as dst:
                dst.text[0] = src.text[0]
                dst.bin = src.bin

                for i in range(start_trace - 1, end_trace):
                    dst.trace[i - start_trace + 1] = src.trace[i]
                    dst.header[i - start_trace + 1] = src.header[i]
                    dst.header[i - start_trace + 1].update({segyio.TraceField.TRACE_SEQUENCE_LINE: i - start_trace + 2})

            print(f"Successfully copied traces to {dst_filename}.")
    except Exception as e:
        print(f"Error copying traces: {e}")

def split_sgy_file(sgy_file_path, x_middle, output_folder):
    """
    Split a SEG-Y file into two parts based on a given middle trace index.

    Parameters:
        sgy_file_path (str): Path to the input SEG-Y file.
        x_middle (int): Index of the middle trace to split the file.
        output_folder (str): Path to the folder where the output files will be saved.
    """
    try:
        with segyio.open(sgy_file_path, "r", ignore_geometry=True) as src:
            x_first = 1
            x_last = src.tracecount
            print(f"File {sgy_file_path} contains {x_last} traces. Splitting at trace {x_middle}.")

        # Define output file paths
        base_name = os.path.basename(sgy_file_path)
        left_name = os.path.join(output_folder, f"{os.path.splitext(base_name)[0]}_left.sgy")
        right_name = os.path.join(output_folder, f"{os.path.splitext(base_name)[0]}_right.sgy")

        # Split the file into left and right parts
        copy_trace_range(sgy_file_path, left_name, x_first, x_middle)
        copy_trace_range(sgy_file_path, right_name, x_middle + 1, x_last)
    except Exception as e:
        print(f"Error splitting SEG-Y file: {e}")

# Main script execution
if len(sys.argv) > 3:
    sgy_file_path = sys.argv[1]
    x_middle = int(sys.argv[2])
    output_folder = sys.argv[3]
else:
    print("Error: Missing arguments. Please provide the SGY file path, middle trace index, and output folder.")
    sys.exit(1)

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print(f"Processing file: {sgy_file_path}, middle trace index: {x_middle}, output folder: {output_folder}")
split_sgy_file(sgy_file_path, x_middle, output_folder)
