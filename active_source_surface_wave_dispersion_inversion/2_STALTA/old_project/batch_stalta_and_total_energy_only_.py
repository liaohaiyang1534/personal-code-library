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

def process_sgy_files(input_folders, stalta_script_path, duration):
    for input_folder in input_folders:
        output_folder = create_output_folder(input_folder)
        for root, _, files in os.walk(input_folder):
            for file in files:
                if file.endswith(".sgy"):
                    input_file_path = os.path.join(root, file)
                    print(f"Processing {input_file_path}")
                    result = subprocess.run(
                        ["python", stalta_script_path, input_file_path, output_folder, str(duration)],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8'
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


        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\重锤-垫板-土_土埋_273_389"

        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\重锤-垫板-土_石膏_392_509"





        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\重锤-垫板-土_沙袋_755_868",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\重锤-垫板-土_胶带_638_750",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\重锤-垫板-土_点胶_519_631",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\重锤-垫板-水泥_土埋_273_389",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\重锤-垫板-水泥_石膏_392_509",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\重锤-垫板-水泥_沙袋_755_868",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\重锤-垫板-水泥_胶带_638_750",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\重锤-垫板-水泥_点胶_519_631",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\重锤-垫板-沥青_土埋_273_389",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\重锤-垫板-沥青_石膏_392_509",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\重锤-垫板-沥青_沙袋_755_868",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\重锤-垫板-沥青_胶带_638_750",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\重锤-垫板-沥青_点胶_519_631",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-垫板-土_土埋_273_389",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-垫板-土_石膏_392_509",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-垫板-土_沙袋_755_868",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-垫板-土_胶带_638_750",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-垫板-土_点胶_519_631",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-垫板-水泥_土埋_273_389",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-垫板-水泥_石膏_392_509",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-垫板-水泥_沙袋_755_868",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-垫板-水泥_胶带_638_750",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-垫板-水泥_点胶_519_631",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-垫板-沥青_土埋_273_389",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-垫板-沥青_石膏_392_509",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-垫板-沥青_沙袋_755_868",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-垫板-沥青_胶带_638_750",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-垫板-沥青_点胶_519_631",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-不垫板-土_土埋_273_389",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-不垫板-土_石膏_392_509",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-不垫板-土_沙袋_755_868",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-不垫板-土_胶带_638_750",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-不垫板-土_点胶_519_631",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-不垫板-水泥_土埋_273_389",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-不垫板-水泥_石膏_392_509",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-不垫板-水泥_沙袋_755_868",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-不垫板-水泥_胶带_638_750",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-不垫板-水泥_点胶_519_631",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-不垫板-沥青_土埋_273_389",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-不垫板-沥青_石膏_392_509",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-不垫板-沥青_沙袋_755_868",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-不垫板-沥青_点胶_519_631",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\diff_hammer_compare\穿心锤-不垫板-沥青_胶带_638_750"



        # r"H:\lhyonedrive\OneDrive\diff_coupling\car\car_30kmh_2_273_389",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\car\car_30kmh_2_392_509",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\car\car_30kmh_2_519_631",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\car\car_30kmh_2_638_750",
        # r"H:\lhyonedrive\OneDrive\diff_coupling\car\car_30kmh_2_755_868"





        r"H:\experiment\2306_主动源面波\DAS data\zdy\0621_无阴井\0\2023-06-21_sgy_836_944"





    ]

    stalta_script_path = r"H:\code_copy\active_source_classification\2_STALTA\stalta_only_.py"
    duration = 1.0  # Duration in seconds

    process_sgy_files(input_folders, stalta_script_path, duration)


    print("------------------------------------")
    print("------------------------------------")
    print("------------------------------------")
    print("All .sgy files have been processed.")
    print("------------------------------------")
    print("------------------------------------")
    print("------------------------------------")


    for input_folder in input_folders:
        total_energy_script_path = r"H:\code_copy\active_source_classification\2_STALTA\total_energy.py"
        output_folder_path = create_output_folder(input_folder)
        removebad_folder_path = output_folder_path + "_removebad"

        print("------------------------------------")

        print(f"Running total energy script: {total_energy_script_path} with input folder: {output_folder_path} and output folder: {removebad_folder_path}")

        print("------------------------------------")

        result = subprocess.run(["python", total_energy_script_path, output_folder_path, removebad_folder_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        
        print(result.stdout)
        if result.stderr:
            print(f"Error running total energy script: {result.stderr}")






