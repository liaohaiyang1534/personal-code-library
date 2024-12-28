import os
import subprocess

def process_folder(root_folder, x1, x2, python_script_path):
    """
    Process all .sgy files in a given folder, invoking an external Python script for each file.

    Args:
        root_folder (str): The root directory containing .sgy files to process.
        x1 (int): The starting parameter for processing.
        x2 (int): The ending parameter for processing.
        python_script_path (str): The path to the Python script to be executed.

    Returns:
        None
    """
    # Create an output folder with a suffix based on parameters
    output_suffix = f"_{x1}_{x2}"
    output_folder = os.path.join(os.path.dirname(root_folder), os.path.basename(root_folder) + output_suffix)
    os.makedirs(output_folder, exist_ok=True)
    print("Output folder:", output_folder)

    # Traverse the directory and process each .sgy file
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.sgy'):
                sgy_file_path = os.path.join(foldername, filename)
                print("Processing file:", sgy_file_path)

                # Call the external Python script using subprocess
                cmd = ["python", python_script_path, sgy_file_path, output_folder, str(x1), str(x2)]
                result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

                # Debugging information for subprocess
                print(f"Debug: Subprocess command: {' '.join(cmd)}")
                print("Debug: Subprocess output:", result.stdout)
                if result.stderr:
                    print("Debug: Subprocess error:", result.stderr)
                print("Debug: Subprocess return code:", result.returncode)

if __name__ == "__main__":
    """
    Main entry point of the script.

    This script processes all .sgy files in the specified root folder by calling an external Python script with 
    various parameter groups. The results for each parameter group are saved in separate output folders.
    """

    # Define the root folder containing the .sgy files
    root_folder = r"H:\experiment\2306_主动源面波\DAS data\zdy\0621（无阴井）\36\2023-06-21_sgy"

    # Path to the external Python script to process each file
    python_script_path = r"H:\code_copy\active_source_classification\1_extract_specific_traces\extract_specific_traces.py"

    # Parameter groups to be used for processing
    param_groups = [
        (46, 170),
        (202, 308),
        (836, 944),
        (971, 1094),
        (1784, 1927),
        (1963, 2054),
    ]
    
    # Loop through each parameter group and process the folder
    for x1, x2 in param_groups:
        process_folder(root_folder, x1, x2, python_script_path)
