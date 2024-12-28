import os
import sys

def merge_txt_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, f"{os.path.basename(input_folder)}.txt")
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in sorted(os.listdir(input_folder)):
            if filename.endswith('.txt'):
                file_path = os.path.join(input_folder, filename)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    for line in infile:
                        line = line.strip()
                        if line:
                            columns = line.split()
                            if len(columns) > 1:
                                try:
                                    # Attempt to convert the second column to a float and check the condition
                                    second_column_value = float(columns[1])
                                    if second_column_value <= 600:
                                        # Do not modify the line
                                        columns[0] = str(float(columns[0]))  # Ensure the first column is a float
                                        
                                        # Join updated columns into a line and write to the output file
                                        outfile.write(" ".join(columns))
                                        outfile.write("\n")
                                except ValueError:
                                    continue  # Skip lines where conversion to float fails
    return output_file

def main():
    input_folder = sys.argv[1]
    output_folder = input_folder + '_onetxt'
    output_file = merge_txt_files(input_folder, output_folder)
    print(output_file)  # Print the output file path

if __name__ == "__main__":
    main()
