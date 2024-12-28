import os
import subprocess
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-interactive plotting
import matplotlib.pyplot as plt

def create_output_folder(input_folder):
    output_folder = input_folder + "_split"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def process_sgy_files(input_folders, stalta_script_path, minus_min, minus_second, duration):
    for input_folder in input_folders:
        output_folder = create_output_folder(input_folder)
        for root, _, files in os.walk(input_folder):
            for file in files:
                if file.endswith(".sgy"):
                    input_file_path = os.path.join(root, file)
                    print(f"Processing {input_file_path}")
                    result = subprocess.run(
                        ["python", stalta_script_path, input_file_path, output_folder, str(minus_min), str(minus_second), str(duration)],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                    )
                    print(result.stdout)
                    if result.stderr:
                        print(f"Error processing {input_file_path}: {result.stderr}")
                    
                    # 检查并保存生成的图形文件
                    image_filename = os.path.splitext(file)[0] + "_stalta.png"
                    image_path = os.path.join(output_folder, image_filename)
                    if os.path.exists(image_path):
                        print(f"Saving {image_path}")
                        img = plt.imread(image_path)
                        plt.imshow(img)
                        plt.axis('off')
                        plt.savefig(image_path)
                        plt.close()

if __name__ == "__main__":
    input_folders = [
        # r"H:\lhyonedrive\OneDrive\diff_coupling\active_source_2\dianjiao_2024-05-02_sgy_519_631",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\active_source_2\jiaodai_2024-05-02_sgy_638_750",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\active_source_2\shadai_2024-05-02_sgy_755_868",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\active_source_2\shigao_2024-05-02_sgy_392_509",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\active_source_2\tumai_2024-05-02_sgy_273_389"

        # r"H:\lhyonedrive\OneDrive\termite\school\active_source_2\shots_510_610"

        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\tumai_shots_273_389"



        # r"H:\lhyonedrive\OneDrive\termite\temple\shots_263_393_test"

        # r"H:\lhyonedrive\OneDrive\termite\school\active_source_1\shots_253_356"

        r"H:\termite\dike\shots_218_257",
        r"H:\termite\dike\shots_257_297"

    ]

    # minus_min = 0  # 减去的分钟数
    # minus_second = -2  # 减去的秒数
    # txt_file_path = r"H:\lhyonedrive\OneDrive\diff_coupling\active_source_2\shot_time.txt"



    # minus_min = 4  # 减去的分钟数
    # minus_second = -4  # 减去的秒数
    # txt_file_path = r"H:\lhyonedrive\OneDrive\termite\temple\shot_time.txt"





    # minus_min = 4  # 减去的分钟数
    # minus_second = 20  # 减去的秒数
    # txt_file_path = r"H:\lhyonedrive\OneDrive\termite\school\active_source_1\shot_time.txt"



    minus_min = 4  # 减去的分钟数
    minus_second = 6  # 减去的秒数
    txt_file_path = r"H:\termite\dike\shot_time.txt"






    stalta_script_path = r"H:\code_copy\active_source_classification\2_STALTA\stalta.py"
    duration = 1.0  # Duration in seconds
    process_sgy_files(input_folders, stalta_script_path, minus_min, minus_second, duration)
    print("All .sgy files have been processed.")



    for input_folder in input_folders:
        total_energy_script_path = r"H:\code_copy\active_source_classification\2_STALTA\total_energy.py"
        output_folder_path = create_output_folder(input_folder)
        removebad_folder_path = output_folder_path + "_removebad"
        print(f"Running total energy script: {total_energy_script_path} with input folder: {output_folder_path} and output folder: {removebad_folder_path}")
        result = subprocess.run(["python", total_energy_script_path, output_folder_path, removebad_folder_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Error running total energy script: {result.stderr}")

        # Run batch_shot_time_match.py
        shot_time_match_script_path = r"H:\code_copy\active_source_classification\2_STALTA\batch_shot_time_match.py"
        print(f"Running shot time match script: {shot_time_match_script_path} with input folder: {removebad_folder_path} and txt file path: {txt_file_path}")
        result = subprocess.run(["python", shot_time_match_script_path, removebad_folder_path, txt_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Error running shot time match script: {result.stderr}")








