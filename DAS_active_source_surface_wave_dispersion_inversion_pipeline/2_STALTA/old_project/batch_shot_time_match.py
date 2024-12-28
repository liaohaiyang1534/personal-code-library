import os
import sys
import subprocess

def create_output_folder(input_folder):
    output_folder = f"{input_folder}_shottimematch"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def find_sgy_files(input_folder):
    sgy_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".sgy"):
                sgy_files.append(os.path.join(root, file))
    return sgy_files

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python batch_shot_time_match.py <input_folder> <txt_file_path>")
        sys.exit(1)

    input_folder = sys.argv[1]
    txt_file_path = sys.argv[2]

    output_folder = create_output_folder(input_folder)
    sgy_files = find_sgy_files(input_folder)
    python_file_path = r"H:\code_copy\active_source_classification\2_STALTA\shot_time_match.py"

    success_files = []
    no_match_files = []
    multiple_match_files = []
    file_not_found_files = []

    for sgy_file in sgy_files:
        result = subprocess.run(["python", python_file_path, txt_file_path, sgy_file, output_folder], capture_output=True, text=True)
        if result.returncode == 0:
            success_files.append(sgy_file)
        elif result.returncode == 1:
            no_match_files.append(sgy_file)
        elif result.returncode == 2:
            multiple_match_files.append(sgy_file)
        elif result.returncode == 3:
            file_not_found_files.append(sgy_file)

    print("\nSummary:")
    print(f"Total SGY files processed: {len(sgy_files)}")
    print(f"Successful matches: {len(success_files)}")
    print(f"No matching times found: {len(no_match_files)}")
    print(f"Multiple matching times found: {len(multiple_match_files)}")
    print(f"File not found: {len(file_not_found_files)}")

    if no_match_files:
        print("\nFiles with no matching times:")
        for file in no_match_files:
            print(file)

    if multiple_match_files:
        print("\nFiles with multiple matching times:")
        for file in multiple_match_files:
            print(file)

    if file_not_found_files:
        print("\nFiles not found:")
        for file in file_not_found_files:
            print(file)
