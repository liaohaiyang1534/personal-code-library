import os
import glob
import re
import sys
import matplotlib.pyplot as plt


def find_txt_files_and_extract_ds_info(folder_path):
    # Find all .txt files in the folder and its subfolders
    txt_files = glob.glob(os.path.join(folder_path, '**', '*.txt'), recursive=True)
    
    # Store file information and extracted DS info
    files_info = []
    
    for txt_file in sorted(txt_files):
        # Get the file name and full path
        file_name = os.path.basename(txt_file)
        file_path = os.path.abspath(txt_file)
        
        # Use regex to extract numbers before 'ds' in the file name
        match = re.search(r'(\d+)ds', file_name)
        if match:
            ds_number = match.group(1)
        else:
            # If 'ds' is not found, search for the number between the last two dashes
            match = re.search(r'-(\d+)-[^-]*$', file_name)
            if match:
                ds_number = match.group(1)
            else:
                ds_number = None

        # Store file info
        files_info.append({
            'file_name': file_name,
            'file_path': file_path,
            'ds_number': ds_number
        })
    
    return files_info


def process_and_output_files(files_info, output_folder):
    # Create the output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for info in files_info:
        with open(info['file_path'], 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
        
        # Determine the output file path
        relative_path = os.path.relpath(info['file_path'], os.path.dirname(info['file_path']))
        output_file = os.path.join(output_folder, relative_path)
        output_dir = os.path.dirname(output_file)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        data = []
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for line in lines:
                if line.strip():  # Skip empty lines
                    thickness, value = map(float, line.split())

                    # Modify the DS number as needed
                    ds_number = float(info['ds_number']) + 20

                    # Uncomment and modify as needed:
                    # For a specific scenario:
                    # ds_number = (float(info['ds_number']) - 1) * 1.2 + 15
                    
                    # For another specific scenario:
                    # ds_number = (float(info['ds_number']) - 1) * 1.2 - 15

                    # Calculate the new thickness and value
                    new_thickness = thickness * 1000
                    new_value = value * 1000

                    # Write the processed data to the output file
                    outfile.write(f"{ds_number:.6f} {new_thickness:.6f} {new_value:.6f}\n")
                    data.append((ds_number, new_thickness, new_value))
        
        # Uncomment for visualization and save as PNG (optional)
        # if data:
        #     ds_numbers, new_thicknesses, new_values = zip(*data)
        #     plt.figure()
        #     plt.plot(new_thicknesses, new_values, 'o-')
        #     plt.xlabel('Thickness * -1000')
        #     plt.ylabel('Value * 1000')
        #     plt.title(f'DS Number: {ds_number}')
        #     png_file = output_file.replace('.txt', '.png')
        #     plt.savefig(png_file)
        #     plt.close()
    
    print(f"All .txt files have been processed and saved to: {output_folder}")


def main():
    # Get the input folder path from command-line arguments
    input_folder = sys.argv[1]

    # Uncomment and modify this for a specific use case:
    # input_folder = r"path_to_input_folder"

    output_folder = input_folder + "_txts"
    
    files_info = find_txt_files_and_extract_ds_info(input_folder)
    process_and_output_files(files_info, output_folder)
    
    print(output_folder)  # Only print the output folder path


if __name__ == "__main__":
    main()
