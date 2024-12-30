import segyio
import os
import sys

# Get the directory path from the command line
if len(sys.argv) > 1:
    root_folder = sys.argv[1]
else:
    print("Error: No directory path provided.")
    sys.exit(1)

print(f"Processing directory: {root_folder}")


def reverse_traces(src_filename, dst_filename):
    print(f"Reversing traces in {src_filename}")
    with segyio.open(src_filename, "r", ignore_geometry=True) as src:
        data = segyio.tools.collect(src.trace[:])

        spec = segyio.spec()
        spec.sorting = src.sorting
        spec.format = src.format
        spec.samples = src.samples
        spec.tracecount = len(data)

        reversed_data = data[::-1]

        with segyio.create(dst_filename, spec) as dst:
            dst.trace[:] = reversed_data
            dst.text[0] = src.text[0]
            dst.bin = src.bin

    print(f"Created reversed file: {dst_filename}")


def process_sgy_file(sgy_file_path):
    path = os.path.dirname(sgy_file_path)
    new_name = "to_1028_reversed.sgy"
    to_1028_reversed_name = os.path.join(path, new_name)
    reverse_traces(sgy_file_path, to_1028_reversed_name)


def process_folder(root_folder, max_depth):
    for subdir, dirs, files in os.walk(root_folder):
        if subdir.count(os.sep) - root_folder.count(os.sep) >= max_depth:
            continue
        for file in files:
            if file.endswith("to_1028.sgy"):
                original_file_path = os.path.join(subdir, file)
                print(f"Processing file: {original_file_path}")
                process_sgy_file(original_file_path)
    print("Finished processing all files.")


# Main logic
max_depth = 4

process_folder(root_folder, max_depth)
print("Script execution completed.")
