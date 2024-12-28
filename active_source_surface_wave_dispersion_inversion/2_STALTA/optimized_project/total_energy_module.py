import segyio
import numpy as np
import os
from utils import create_output_folder

def calculate_total_energy(file_path):
    with segyio.open(file_path, "r", ignore_geometry=True) as f:
        total_energy = sum(np.sum(trace**2) for trace in f.trace)
    return total_energy

def filter_high_energy_files(input_folder, output_folder, energy_threshold):
    for file in os.listdir(input_folder):
        if file.endswith(".sgy"):
            file_path = os.path.join(input_folder, file)
            total_energy = calculate_total_energy(file_path)
            if total_energy > energy_threshold:
                shutil.copy(file_path, output_folder)
                print(f"File {file} copied (Energy: {total_energy}).")
