# -*- encoding: utf-8 -*-
'''
@File        :   batch_inversion_multi-mode.py
@Time        :   2025/01/03 22:41:41
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import subprocess
import sys
from datetime import datetime
import shutil

def convert_to_long_path(path):
    # Add Windows long path prefix if necessary
    if sys.platform == "win32" and not path.startswith("\\\\?\\"):
        path = "\\\\?\\" + os.path.abspath(path)
    return path

def create_output_directory(input_dir):
    # Create an output directory based on the input directory
    output_dir = input_dir.rstrip('/') + '_inversion_model'
    output_dir = convert_to_long_path(output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def run_inversion(input_dir, output_dir, timestamp, script_path):
    # Convert input and output directories to long path format
    input_dir = convert_to_long_path(input_dir)
    output_dir = convert_to_long_path(output_dir)
    
    # Define subdirectories for the output
    output_best_model_res_dir = os.path.join(output_dir, "best_model_res")
    output_best_model_dir = os.path.join(output_dir, "best_model")
    output_models_jpg_dir = os.path.join(output_dir, "models_jpg")
    
    # Create subdirectories if they don't exist
    if not os.path.exists(output_best_model_res_dir):
        os.makedirs(output_best_model_res_dir)
    if not os.path.exists(output_models_jpg_dir):
        os.makedirs(output_models_jpg_dir)
    if not os.path.exists(output_best_model_dir):
        os.makedirs(output_best_model_dir)
    
    # Loop through files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_file = os.path.join(input_dir, filename)
            input_file = convert_to_long_path(input_file)
            output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_{timestamp}.txt")
            
            # Run the inversion script for each file
            subprocess.run(['python', convert_to_long_path(script_path), input_file, output_dir, 
                            output_best_model_res_dir, output_best_model_dir, output_models_jpg_dir])

def process_directories(directories):
    # Get the current script directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the inversion script
    script_path = os.path.join(current_directory, "inversion_multi-mode.py")
    
    # Create a timestamp for the output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Process each directory
    for input_dir in directories:
        output_dir = create_output_directory(input_dir)
        run_inversion(input_dir, output_dir, timestamp, script_path)
        
        # Copy the scripts to the output directory for tracking
        shutil.copy(__file__, os.path.join(output_dir, f"batch_inversion_multi-mode_{timestamp}.py"))
        shutil.copy(script_path, os.path.join(output_dir, f"inversion_multi-mode_{timestamp}.py"))

if __name__ == "__main__":
    # List of directories to process
    directories = [
        # Example directories (uncomment as needed)
        # "/mnt/h/TEMP_disp_curve",
        # "/mnt/f/SYM/ResultS_line1_60traces_1_tracesinterval_0124-13-20/h5_2_disp_curve_adjusted",
        # "/mnt/h/lhyonedrive/OneDrive/termite/school/active_source_2/shots_510_610_split_removebad_shottimematch_ALL_dispersion_6_18_disp_curve_adjusted",
        # "/mnt/h/lhyonedrive/OneDrive/termite/school/active_source_2/test",
        # "/mnt/h/lhyonedrive/OneDrive/termite/school/active_source_1/shots_253_356_split_removebad_shottimematch_1s_together_disp_curve_adjusted_right",
        # "/mnt/f/BAIYI/ResultS_school_line1_510_610_30_2_20240516_09-00_16-00/outputImage/H5/2024-05-16_disp_curve_adjusted",
        # "/mnt/f/diff_distance_to_cavity/20240531-0603_data/ResultS_line5_628_743_30_07-00_14-00/H5/2024-06-03_sac_disp_curve_adjusted",
        # "/mnt/g/ResultS_line1_90_203_30_20240702_07-00_14-00/2024-07-02_sac_disp_curve_adjusted",
        # "/mnt/i/diff_dis_to_cavity/RESULTS_2024-07-02_sgy_20240912_7h_10-17/dispersion_curve_filter",
        # "/mnt/i/diff_dis_to_cavity/RESULTS_2024-06-29_sgy_60x4-60x6/dispersion_curve_revise_revise",
        # "/mnt/i/diff_dis_to_cavity/RESULTS_TEST_20240925/curve_C2_modified",
        "/mnt/i/diff_dis_to_cavity/RESULTS_LHY_20141125_5m深度10m排列20道的排列看看频散有无空洞的对比/curve_C3_line1_modified",
    ]

    # Process the listed directories
    process_directories(directories)
