import os
import logging

def setup_logging(log_folder="logs"):
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(log_folder, "pipeline.log")),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging setup complete.")

def create_output_folder(base_folder, suffix=""):
    output_folder = os.path.join(base_folder, suffix)
    os.makedirs(output_folder, exist_ok=True)
    return output_folder

def list_sgy_files(input_folder):
    sgy_files = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".sgy"):
                sgy_files.append(os.path.join(root, file))
    return sgy_files
