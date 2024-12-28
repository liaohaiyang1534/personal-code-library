import os
import subprocess
import sys
from datetime import datetime
import shutil

# python /mnt/h/lhyonedrive/OneDrive/code_copy/active_source_classification/9_inversion/passive_source/batch_inversion.py

def convert_to_long_path(path):
    # Add Windows long path prefix if necessary
    if sys.platform == "win32" and not path.startswith("\\\\?\\"):
        path = "\\\\?\\" + os.path.abspath(path)
    return path

def create_output_directory(input_dir):
    # Create an output directory with a suffix "_inversion"
    output_dir = input_dir.rstrip('/') + '_inversion'
    output_dir = convert_to_long_path(output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def run_inversion(input_dir, output_dir, timestamp):
    input_dir = convert_to_long_path(input_dir)
    output_dir = convert_to_long_path(output_dir)
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_file = os.path.join(input_dir, filename)
            input_file = convert_to_long_path(input_file)
            output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_{timestamp}.txt")
            subprocess.run([
                'python', 
                convert_to_long_path('/mnt/h/lhyonedrive/OneDrive/code_copy/active_source_classification/9_inversion/passive_source/inversion.py'), 
                input_file, 
                output_dir, 
                timestamp
            ])

def process_directories(directories):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for input_dir in directories:
        output_dir = create_output_directory(input_dir)
        run_inversion(input_dir, output_dir, timestamp)
        # Copy the scripts to the output directory
        shutil.copy(__file__, os.path.join(output_dir, f"batch_inversion_{timestamp}.py"))
        shutil.copy(
            '/mnt/h/lhyonedrive/OneDrive/code_copy/active_source_classification/9_inversion/passive_source/inversion.py', 
            os.path.join(output_dir, f"inversion_{timestamp}.py")
        )

if __name__ == "__main__":
    directories = [
        # Add the directories you want to process here
        # "/mnt/h/TEMP_disp_curve"
        # "/mnt/f/SYM/ResultS_line1_60traces_1_tracesinterval_0124-13-20/h5_2_disp_curve_adjusted"

        # "/mnt/h/lhyonedrive/OneDrive/termite/school/active_source_2/shots_510_610_split_removebad_shottimematch_ALL_dispersion_6_18_disp_curve_adjusted"

        # "/mnt/h/lhyonedrive/OneDrive/termite/school/active_source_2/test"

        # "/mnt/h/lhyonedrive/OneDrive/termite/school/active_source_1/shots_253_356_split_removebad_shottimematch_1s_together_disp_curve_adjusted_right"

        # "/mnt/f/BAIYI/ResultS_school_line1_510_610_30_2_20240516_09-00_16-00/outputImage/H5/2024-05-16_disp_curve_adjusted"

        # "/mnt/f/diff_distance_to_cavity/20240531-0603_data/ResultS_line5_628_743_30_07-00_14-00/H5/2024-06-03_sac_disp_curve_adjusted"

        "/mnt/g/ResultS_line1_90_203_30_20240702_07-00_14-00/2024-07-02_sac_disp_curve_adjusted"
    ]

    process_directories(directories)
