import os
import re
import subprocess
import sys

def rename_file(file_path):
    # Extract the filename and extension
    directory, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)

    # Use a regex to find parts like 101-3_ in the filename
    match = re.search(r'(\d+-\d+_)', name)
    if match:
        part_to_move = match.group(1)
        # Move the matched part to the front of the filename
        new_name = part_to_move + name.replace(part_to_move, '')
        new_file_path = os.path.join(directory, new_name + ext)
        os.rename(file_path, new_file_path)
        return new_file_path
    return file_path

def process_files_in_directory(directory):
    # Iterate through all files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".png") or file.endswith(".h5"):
                full_path = os.path.join(root, file)
                print(f"Original file: {full_path}")

                # Rename the file
                new_full_path = rename_file(full_path)
                print(f"Renamed file: {new_full_path}")

                # Call a subprocess to process the renamed file
                try:
                    result = subprocess.run(
                        ["python3", "/mnt/h/code_copy/active_source_classification/6_single_sgy_FJs/rename_file.py", new_full_path],
                        capture_output=True, text=True, encoding='utf-8'
                    )
                    print(result.stdout)
                    print(result.stderr)
                except subprocess.CalledProcessError as e:
                    print(f"Error processing {new_full_path}: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <directory_path>")
        sys.exit(1)
    
    directory = sys.argv[1]
    process_files_in_directory(directory)
