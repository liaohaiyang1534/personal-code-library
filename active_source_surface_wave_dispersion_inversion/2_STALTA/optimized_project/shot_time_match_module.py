import os
import shutil
from datetime import datetime, timedelta

def match_shot_time(file_path, txt_file_path, output_folder):
    """
    Match shot times and copy files based on reference.

    Args:
        file_path (str): Path to the `.sgy` file.
        txt_file_path (str): Path to the text file containing reference times.
        output_folder (str): Folder to save results.

    Returns:
        None
    """
    base_name = os.path.basename(file_path)
    time_stamp = extract_timestamp(base_name)

    if not time_stamp:
        print(f"Invalid timestamp in {base_name}.")
        return

    with open(txt_file_path, "r") as f:
        matches = [line for line in f if time_stamp in line]

    if len(matches) == 1:
        output_file = os.path.join(output_folder, f"matched_{base_name}")
        shutil.copy(file_path, output_file)
        print(f"Matched file saved: {output_file}.")
    elif len(matches) > 1:
        print(f"Multiple matches found for {base_name}.")
    else:
        print(f"No match found for {base_name}.")
