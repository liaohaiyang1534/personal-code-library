import os
import subprocess
import segyio

def find_sgy_files(folder_path):
    sgy_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.sgy'):
                sgy_files.append(os.path.join(root, file))
    return sgy_files

def create_output_folder(folder_path):
    output_folder = folder_path + '_band'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def get_sample_rate(sgy_file):
    with segyio.open(sgy_file, "r", ignore_geometry=True) as f:
        sample_rate = segyio.tools.dt(f) / 1e6  # Sample rate in seconds
        sample_rate_hz = 1 / sample_rate  # Sample rate in Hz
    print(f"Sample rate for {sgy_file}: {sample_rate_hz} Hz")
    return sample_rate_hz

def call_bandpass_script(sgy_file, output_folder, lowcut, highcut):
    script_path = r"H:\lhyonedrive\OneDrive\termite\scripts\bandpass\bandpass_sgy.py"
    output_file = os.path.join(output_folder, os.path.basename(sgy_file))
    sample_rate_hz = get_sample_rate(sgy_file)
    subprocess.call(['python', script_path, sgy_file, output_file, str(lowcut), str(highcut), str(sample_rate_hz)])

def main(folder_path, lowcut, highcut):
    sgy_files = find_sgy_files(folder_path)
    output_folder = create_output_folder(folder_path)
    for sgy_file in sgy_files:
        call_bandpass_script(sgy_file, output_folder, lowcut, highcut)

if __name__ == "__main__":
    folder_path = r"H:\lhyonedrive\OneDrive\termite\school\active_source_2\shots_510_610_split_center_right"
    lowcut = 2
    highcut = 100
    main(folder_path, lowcut, highcut)
