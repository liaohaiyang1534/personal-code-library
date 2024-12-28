import re
import os
import sys

def rename_or_copy_file(filename):
    # Define the regex pattern to match arraylength and offset_minoff parts
    pattern = r"(arraylength_[\d\.]+m)_(offset_minoff_[\d\.]+m)"
    
    # Check if the filename needs to be transformed
    match = re.search(pattern, filename)
    if match:
        arraylength_part = match.group(1)
        offset_minoff_part = match.group(2)
        # Construct the new filename
        new_filename = filename.replace(f"{arraylength_part}_{offset_minoff_part}", f"{offset_minoff_part}_{arraylength_part}")
        # Get the directory of the file and the base name
        directory = os.path.dirname(filename)
        new_filename = os.path.join(directory, os.path.basename(new_filename))
        # Rename the file
        os.rename(filename, new_filename)
        print(f"File renamed to: {new_filename}")
    else:
        # If offset_minoff is already at the front, no renaming is needed
        print(f"No rename needed for: {filename}")

# Get the filename parameter
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rename_file.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    print(f"Renaming file: {filename}")
    rename_or_copy_file(filename)
