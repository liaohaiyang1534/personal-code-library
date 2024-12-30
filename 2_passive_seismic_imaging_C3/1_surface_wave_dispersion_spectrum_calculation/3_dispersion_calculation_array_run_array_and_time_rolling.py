# ----------------------------------------------------------------------------------
# PYTHON SCRIPT: 3_dispersion_calculation_array_run_array_and_time_rolling.py
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# Importing libraries
# ----------------------------------------------------------------------------------
import subprocess
import os

# ----------------------------------------------------------------------------------
# Setting parameters
# ----------------------------------------------------------------------------------

# Define the directories containing the data files
directories = [
    "/mnt/i/diff_dis_to_cavity/2024-06-28_sgy/",
    # "/mnt/i/diff_dis_to_cavity/2024-06-29_sgy/",
    # "/mnt/i/diff_dis_to_cavity/2024-06-30_sgy/",
    # "/mnt/i/diff_dis_to_cavity/2024-07-01_sgy/",
    # "/mnt/i/diff_dis_to_cavity/2024-07-02_sgy/",
    # "/mnt/i/diff_dis_to_cavity/2024-07-03_sgy/",
    # "/mnt/i/diff_dis_to_cavity/2024-07-04_sgy/",
    # "/mnt/i/diff_dis_to_cavity/2024-07-05_sgy/",
]

# Define file number pairs (start and end)
file_number_pairs = [
    ('60x20', '60x22'),
]

# ----------------------------------------------------------------------------------
# Running the script
# ----------------------------------------------------------------------------------

# Get the current directory of the script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the script path relative to the current directory
script_path = os.path.join(current_directory, "2_dispersion_calculation_array_run_array_rolling.py")

# Iterate through directories and file number pairs
for directory in directories:
    for start_file_number, end_file_number in file_number_pairs:
        command = ["python3", script_path, start_file_number, end_file_number, directory]
        try:
            print(f"Processing {start_file_number} to {end_file_number} in directory {directory}")
            subprocess.run(command, check=True, cwd=directory)
            print(f"Completed processing {start_file_number} to {end_file_number} in directory {directory}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while processing files from {start_file_number} to {end_file_number} in directory {directory}: {e}")

# ----------------------------------------------------------------------------------
# THE END
# ----------------------------------------------------------------------------------
