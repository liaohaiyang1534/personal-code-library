import os
import glob

def process_txt_file(file_path, output_dir):
    # Create the output file name
    base_name = os.path.basename(file_path)
    new_file_name = os.path.splitext(base_name)[0] + '_adjusted.txt'
    new_file_path = os.path.join(output_dir, new_file_name)

    # Open the input and output files
    with open(file_path, 'r') as input_file, open(new_file_path, 'w') as output_file:
        for line in input_file:
            # Skip empty lines
            if not line.strip():
                continue

            # Split the line into columns
            columns = line.strip().split()
            if len(columns) < 3:
                continue

            # Convert frequency to period
            try:
                frequency_hz = float(columns[0])
                period_s = 1 / frequency_hz
                velocity_km_s = float(columns[1])
                order = int(columns[2])
            except ValueError:
                continue

            # Write the new content to the output file
            output_file.write(f"{period_s} {velocity_km_s} {order}\n")

def main(input_dir):
    # Create the output directory
    output_dir = input_dir + '_adjusted'
    os.makedirs(output_dir, exist_ok=True)

    # Get all .txt files in the input directory
    txt_files = glob.glob(os.path.join(input_dir, "*.txt"))

    # Process each .txt file
    for file_path in txt_files:
        process_txt_file(file_path, output_dir)

    print("All files have been processed.")

if __name__ == "__main__":
    input_dir = r"F:\SYM\ResultS_line1_60traces_1_tracesinterval_0124-13-20\h5_2_20240811_disp_curve"
    main(input_dir)
