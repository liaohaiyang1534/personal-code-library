import os
import segyio
from segyio import TraceField
import sys
import shutil
import re

# Get parameters from command line arguments
if len(sys.argv) > 2:
    root_folder = sys.argv[1]
    trace_spacing_m = float(sys.argv[2])  # Accept trace_spacing_m and ensure it is converted to a float
else:
    print("Error: Insufficient command-line arguments provided.")
    sys.exit(1)

print(f"Processing directory: {root_folder}")
print(f"Trace spacing (m): {trace_spacing_m}")


def modify_sgy_file(original_file_path, trace_spacing_m):
    """
    Modify the GroupX coordinates of a SEGY file based on the specified trace spacing.

    Args:
        original_file_path (str): Path to the original SEGY file.
        trace_spacing_m (float): Trace spacing in meters.
    """
    # Generate new file path by appending '_gx' to the original filename
    new_file_path = original_file_path[:-4] + '_gx.sgy'
    
    # Read the original file's metadata and data
    with segyio.open(original_file_path, 'r', ignore_geometry=True) as src:
        # Create a SEGY spec to preserve original file attributes
        spec = segyio.spec()
        spec.sorting = src.sorting
        spec.format = src.format
        spec.samples = src.samples
        spec.tracecount = len(src.trace)

        # Create a new SEGY file
        with segyio.create(new_file_path, spec) as dst:
            # Copy data, binary headers, and text headers
            dst.trace[:] = src.trace[:]
            dst.bin = src.bin
            dst.text[0] = src.text[0]

            # Modify GroupX coordinates and set scaling factor
            # Assume the scaling factor is 1000 (coordinates in millimeters)
            coord_scale_factor = 1000  # Or -1000 depending on your requirements
            for i in range(spec.tracecount):
                # Compute the new GroupX value in millimeters
                new_group_x = int((i + 1) * trace_spacing_m * coord_scale_factor)
                dst.header[i].update({
                    segyio.TraceField.GroupX: new_group_x,
                    segyio.TraceField.SourceGroupScalar: -coord_scale_factor  # Negative value means divide by abs(scalar)
                })

    print(f"File '{new_file_path}' processed. All trace GroupX coordinates updated with scaling factor {coord_scale_factor}.")


def process_folder(root_folder, target_patterns, max_depth, trace_spacing_m):
    """
    Process SEGY files in a folder that match specified patterns.

    Args:
        root_folder (str): Root directory to process.
        target_patterns (list): List of regex patterns for target filenames.
        max_depth (int): Maximum depth to search for files.
        trace_spacing_m (float): Trace spacing in meters.
    """
    # Compile regex patterns for efficiency
    compiled_patterns = [re.compile(pattern) for pattern in target_patterns]
    
    for subdir, _, files in os.walk(root_folder):
        # Calculate current folder depth
        depth = subdir.count(os.sep) - root_folder.count(os.sep)
        if depth > max_depth:
            continue
        for file in files:
            # Match files against the compiled regex patterns
            if any(pattern.match(file) for pattern in compiled_patterns):
                file_path = os.path.join(subdir, file)
                modify_sgy_file(file_path, trace_spacing_m)
                print(f"Processed: {file_path}")


# Target file patterns (regex for matching filenames)
target_file_names = [
    r"\d+(\.\d+)?m_1028\.sgy",  # Matches files like "10.5m_1028.sgy"
    r"\d+(\.\d+)?m_1267\.sgy"   # Matches files like "20m_1267.sgy"
]

max_depth = 4

# Process the root folder
process_folder(root_folder, target_file_names, max_depth, trace_spacing_m)
