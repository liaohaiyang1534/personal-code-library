# -*- encoding: utf-8 -*-
'''
@File        :   main.py
@Time        :   2025/01/03 22:30:54
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import json
from shot_time_match_module import match_shot_time
from stalta_module import process_sgy
from total_energy_module import filter_high_energy_files
from utils import setup_logging, create_output_folder, list_sgy_files

def load_config(config_path):
    """
    Load configuration from a JSON file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Configuration parameters.
    """
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def main():
    # Setup logging
    setup_logging()

    # Load configuration
    config = load_config("config.json")

    # Create output folder
    output_folder = create_output_folder("output", suffix="processed")

    # Process files based on configuration
    input_folders = config['input_folders']
    txt_file_path = config['txt_file_path']
    
    # Step 1: Match shot times and copy files
    for folder in input_folders:
        sgy_files = list_sgy_files(folder)
        for file_path in sgy_files:
            match_shot_time(file_path, txt_file_path, output_folder)

    # Step 2: Process SEG-Y files with STA/LTA
    stalta_params = config["stalta_params"]
    for folder in input_folders:
        sgy_files = list_sgy_files(folder)
        for file_path in sgy_files:
            process_sgy(file_path, output_folder, stalta_params)

    # Step 3: Filter high-energy files
    energy_threshold = config.get("energy_threshold", 1000)
    for folder in input_folders:
        filter_high_energy_files(folder, output_folder, energy_threshold)

if __name__ == "__main__":
    main()
