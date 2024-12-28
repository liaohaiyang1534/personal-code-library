import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import segyio
import sys

def calculate_total_energy(file_path):
    with segyio.open(file_path, "r", ignore_geometry=True) as f:
        num_traces = f.tracecount
        total_energy = 0
        for trace in f.trace:
            total_energy += np.sum(trace**2)
    return total_energy

def process_folder(folder_path, output_folder, threshold):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    energy_values = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".sgy"):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}")
                total_energy = calculate_total_energy(file_path)
                energy_values[file] = total_energy
                print(f"Total energy for {file}: {total_energy}")

                # 复制能量超过阈值的文件到新文件夹
                if total_energy > threshold:
                    output_file_path = os.path.join(output_folder, file)
                    shutil.copy(file_path, output_file_path)
                    print(f"Copied {file_path} to {output_file_path}")

    return energy_values

def plot_energy(energy_values, threshold):
    files = list(energy_values.keys())
    energies = list(energy_values.values())

    plt.figure(figsize=(10, 6))
    plt.barh(files, energies, color='blue')
    plt.axvline(x=threshold, color='red', linestyle='--', label=f'Threshold ({threshold})')
    plt.xlabel('Total Energy')
    plt.ylabel('File')
    plt.title('Total Energy of SEG-Y Files')
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.close()

    # 打印能量小于阈值的文件
    print(f"Files with total energy less than {threshold}:")
    for file, energy in energy_values.items():
        if energy < threshold:
            print(file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python total_energy.py <input_folder_path> <output_folder_path>")
        sys.exit(1)

    print("folder_path = sys.argv[1]")
    folder_path = sys.argv[1]
    print("output_folder = sys.argv[2]")
    output_folder = sys.argv[2]
    
    threshold = 2000  # 设置阈值

    print("energy_values=process_folder()")
    energy_values = process_folder(folder_path, output_folder, threshold)
    plot_energy(energy_values, threshold)



