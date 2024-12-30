import os
import subprocess

def find_sgy_files(folder_path):
    sgy_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.sgy'):
                sgy_files.append(os.path.join(root, file))
    return sgy_files

def create_output_folder(folder_path):
    output_folder = folder_path + '_downsampled'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def call_downsample_script(sgy_file, output_folder, current_sample_rate, target_sample_rate):
    script_path = r".\downsample_sgy.py"
    output_file = os.path.join(output_folder, os.path.basename(sgy_file))
    
    if current_sample_rate > target_sample_rate:
        subprocess.call(['python', script_path, sgy_file, output_file, str(current_sample_rate), str(target_sample_rate)])

def main(folder_path, current_sample_rate, target_sample_rate):
    sgy_files = find_sgy_files(folder_path)
    output_folder = create_output_folder(folder_path)
    for sgy_file in sgy_files:
        call_downsample_script(sgy_file, output_folder, current_sample_rate, target_sample_rate)

if __name__ == "__main__":
    folder_path = r"I:\diff_dis_to_cavity\2024-06-28_sgy"  # Change this to your input folder
    current_sample_rate = 500  # Specify the current sample rate in Hz
    target_sample_rate = 100  # Desired downsampled frequency in Hz
    main(folder_path, current_sample_rate, target_sample_rate)