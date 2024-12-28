import os
import sys

def process_files(input_folder):
    output_folder = input_folder + "_depthtxt"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)

            with open(input_file_path, 'r') as infile:
                lines = infile.readlines()

            processed_lines = lines[8:-7]

            filtered_lines = []
            depth = 0.0
            first_vs = 0.0  # Used to store the Vs value of the first layer
            for index, line in enumerate(processed_lines):
                columns = line.split()
                if len(columns) >= 3:
                    thickness = float(columns[0])
                    depth += thickness
                    if index == 0:
                        first_vs = float(columns[2])  # Store the Vs value of the first layer
                    filtered_lines.append(f"{depth:.4f}\t{float(columns[2]):.4f}\n")

            # Insert a row at the beginning for depth 0 with the Vs value of the first layer
            filtered_lines.insert(0, f"0.0000\t{first_vs:.4f}\n")

            with open(output_file_path, 'w') as outfile:
                outfile.writelines(filtered_lines)

    return output_folder

def main():
    input_folder = sys.argv[1]
    output_folder = process_files(input_folder)
    print(output_folder)  # Print the output folder path

if __name__ == "__main__":
    main()
