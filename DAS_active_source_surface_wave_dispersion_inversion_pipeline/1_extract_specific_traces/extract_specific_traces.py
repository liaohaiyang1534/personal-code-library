import segyio
import os
import re
import sys
import argparse

def extract_numbers_from_parent_folder_name(folder_path):
    parent_folder_name = os.path.basename(os.path.dirname(folder_path))
    return re.findall(r'\d+', parent_folder_name)

def process_sgy_file(sgy_file_path, x1, x2, output_folder):
    path = os.path.dirname(sgy_file_path)
    base_name = os.path.basename(sgy_file_path)
    base_name_no_ext = os.path.splitext(base_name)[0]
    new_name = f"{base_name_no_ext}_{x1}_{x2}.sgy"
    new_file_path = os.path.join(output_folder, new_name)

    copy_trace_range(sgy_file_path, new_file_path, x1, x2)

def copy_trace_range(src_filename, dst_filename, start_trace, end_trace):
    with segyio.open(src_filename, "r", ignore_geometry=True) as src:
        if start_trace < 1 or end_trace > src.tracecount:
            print(f"Invalid trace range. File contains {src.tracecount} traces.")
            return

        spec = segyio.tools.metadata(src)
        spec.tracecount = end_trace - start_trace + 1

        with segyio.create(dst_filename, spec) as dst:
            dst.text[0] = src.text[0]
            dst.bin = src.bin

            for i in range(start_trace - 1, end_trace):
                dst.trace[i - start_trace + 1] = src.trace[i]
                dst.header[i - start_trace + 1] = src.header[i]
                dst.header[i - start_trace + 1].update({segyio.TraceField.TRACE_SEQUENCE_LINE: i - start_trace + 2})

        print(f"Copied traces {start_trace} to {end_trace} from {src_filename} to {dst_filename}.")

def main():
    parser = argparse.ArgumentParser(description='Extract specific traces from a SEG-Y file.')
    parser.add_argument('sgy_file_path', type=str, help='Path to the input SEG-Y file')
    parser.add_argument('output_folder', type=str, help='Path to the output folder')
    parser.add_argument('x1', type=int, help='Starting trace index')
    parser.add_argument('x2', type=int, help='Ending trace index')
    args = parser.parse_args()

    print(f"Processing files: {args.sgy_file_path}")
    process_sgy_file(args.sgy_file_path, args.x1, args.x2, args.output_folder)

if __name__ == "__main__":
    main()
