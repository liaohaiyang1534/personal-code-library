#!/usr/bin/env python3

import os
import numpy as np
import sys

if len(sys.argv) != 6:
    print("Usage: ./process.py <line> <start> <end> <base_directory> <xyz_file_path>")
    sys.exit(1)

line = sys.argv[1]  # Line number
start = int(sys.argv[2])  # Start point
end = int(sys.argv[3])  # End point
base_directory = sys.argv[4]  # Base directory
xyz_file_path = sys.argv[5]  # Input file path


# Define required functions
def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    start_index = 0
    for i, line in enumerate(lines):
        if "H(KM)" in line and "VS(KM/S)" in line:
            start_index = i + 1
            break
    
    data = []
    for line in lines[start_index:]:
        parts = line.split()
        if len(parts) < 3:
            continue
        try:
            depth_km = float(parts[0])
            vs_km_s = float(parts[2])
            data.append((depth_km, vs_km_s))
        except ValueError:
            continue
    
    return data


def convert_data(x, y, z, data):
    results = []
    accumulated_depth = 0
    for line in data:
        depth_km, vs_km_s = line
        accumulated_depth += depth_km
        new_z = z - (accumulated_depth * 1000)
        results.append(f"{x:.7e} {y:.7e} {new_z:.7e} {vs_km_s:.7e}")
    return results


def read_specific_line_data(file_path, line_number):
    with open(file_path, 'r') as file:
        for current_line_number, line in enumerate(file, start=1):
            if current_line_number == line_number:
                parts = line.split()
                if len(parts) >= 5 and parts[1] == str(line_number):
                    x = float(parts[2])
                    y = float(parts[3])
                    z = float(parts[4])
                    return x, y, z
    raise ValueError(f"Line number {line_number} not found in the file.")


# Read, convert, and write data
for line_number in np.arange(start, end + 1, 1):
    x, y, z = read_specific_line_data(xyz_file_path, line_number)
    file_path = os.path.join(base_directory, f"{line}-{line_number}.out")
    data = read_data(file_path)
    results = convert_data(x, y, z, data)
    output_file_path = os.path.join(base_directory, f"converted_data_{line_number}.txt")
    
    with open(output_file_path, 'w') as file:
        for result in results:
            file.write(result + '\n')
    
    print(f"Data has been written to: {output_file_path}")


# Merge files, excluding the last line from each file
merged_file_path = os.path.join(base_directory, "line.txt")
with open(merged_file_path, 'w') as merged_file:
    for line_number in np.arange(start, end + 1, 1):
        current_file_path = os.path.join(base_directory, f"converted_data_{line_number}.txt")
        with open(current_file_path, 'r') as current_file:
            lines = current_file.readlines()[:-1]  # Exclude the last line
            merged_file.writelines(lines)

print(f"All files have been merged into {merged_file_path}")


# Update data and format it to non-scientific notation
with open(merged_file_path, 'r') as file:
    lines = file.readlines()

updated_lines = []
for line in lines:
    parts = line.split()
    if len(parts) >= 4:
        parts[3] = "{:.7f}".format(float(parts[3]) * 1000)
        parts[0] = "{:.3f}".format(float(parts[0]))
        parts[1] = "{:.3f}".format(float(parts[1]))
        parts[2] = "{:.3f}".format(float(parts[2]))
        updated_line = ' '.join(parts) + '\n'
        updated_lines.append(updated_line)
    else:
        updated_lines.append(line)

updated_file_path = os.path.join(base_directory, "line_non_scientific.txt")
with open(updated_file_path, 'w') as file:
    file.writelines(updated_lines)

print(f"Updated data has been written to {updated_file_path}")


def remove_empty_lines(file_path):
    # Read file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Filter out empty lines
    non_empty_lines = [line for line in lines if line.strip() != '']

    # Write back non-empty lines to the file
    with open(file_path, 'w') as file:
        file.writelines(non_empty_lines)


# Remove empty lines from line.txt
remove_empty_lines(os.path.join(base_directory, "line.txt"))

# Remove empty lines from line_non_scientific.txt
remove_empty_lines(os.path.join(base_directory, "line_non_scientific.txt"))

print("Empty lines have been removed from the files.")
