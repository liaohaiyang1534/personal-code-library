import os
import shutil
import re

def move_files_based_on_pattern(source_folder):
    # Define a regex pattern to match the desired file name format
    regex = re.compile(r'offset_minoff_\d+\.\d+_arraylength_\d+\.\d+_spacing_\d+\.\d+_(.*?)_\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}\.\d{3}_output_right_sac_FJ_dispersion\.(png|h5)')
    
    # Iterate through the files in the source folder
    for filename in os.listdir(source_folder):
        print(f'Checking file: {filename}')  # Debug information
        match = regex.match(filename)
        if match:
            pattern = match.group(1)
            print(f'Pattern found: {pattern}')  # Debug information
            target_folder = os.path.join(source_folder, pattern)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
                print(f'Created folder: {target_folder}')  # Debug information
            
            source_path = os.path.join(source_folder, filename)
            target_path = os.path.join(target_folder, filename)
            # Move the file to the target folder
            shutil.move(source_path, target_path)
            print(f'Moved file: {filename} to {target_folder}')
        else:
            print(f'No match for file: {filename}')  # Debug information

# Example usage
source_folder = r"H:\termite\temple\test"
move_files_based_on_pattern(source_folder)
