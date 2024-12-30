import os
import shutil

def find_sac_files(directory):
    sac_files = []
    print(f"Searching for .sac files in directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            # Find specific SAC files containing '0700'
            if file.endswith('.sac') and '0700' in file:
                file_path = os.path.join(root, file)
                sac_files.append(file_path)
                print(f"Found file: {file_path}")
    sac_files.sort()
    print(f"Total .sac files found: {len(sac_files)}")
    return sac_files

def copy_sac_files(sac_files, destination_directory):
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
        print(f"Created destination directory: {destination_directory}")
    for sac_file in sac_files:
        destination_path = shutil.copy(sac_file, destination_directory)
        print(f"Copied {sac_file} to {destination_path}")

def main():
    source_directory = r"I:\阴井\data_20240627-0706\2024-07-05_sac"
    destination_directory = r"I:\阴井\data_20240627-0706\700thsac"

    # Uncomment for Linux environment
    # source_directory = "/mnt/f/diff_distance_to_cavity/noise_data/2024-05-21_sac/2024-05-21_sac"
    # destination_directory = "/mnt/h/lhyonedrive/OneDrive/sym/paper/docs/pics_画图的代码_copy/背景噪声能量白天黑夜对比/700th_sac"

    print("Starting SAC file processing...")
    
    sac_files = find_sac_files(source_directory)
    
    print("Listing found .sac files:")
    for sac_file in sac_files:
        print(sac_file)
    
    print("Copying .sac files to destination directory...")
    copy_sac_files(sac_files, destination_directory)
    
    print("SAC file processing completed.")

if __name__ == "__main__":
    main()
