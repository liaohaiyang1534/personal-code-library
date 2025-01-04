# -*- encoding: utf-8 -*-
'''
@File        :   12345—A Script—From Inversion to Final Plot.py
@Time        :   2025/01/03 22:42:53
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import sys
import subprocess

# Update the paths as required:
# Path for inversion model results
inversion_path = r"I:\diff_dis_to_cavity\RESULTS_LHY_20241201_whole_line1_rolling_6_16marray\curve_C3_modified_inversion_model\best_model_res"

# Notes for modification:
# Modification 1: Modify "2-添加x-location.py" to adjust how x-location is calculated.
# Modification 2: Update the horizontal adjustment in "3-合成一个txt.py".
# Modification 3: In "5-画简单插值图.py", decide on the aspect ratio for the plot.
# Modification 4: In "5-画简单插值图.py", confirm if the x-axis should be inverted.

# Get the directory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Paths to the dependent scripts
script1 = os.path.join(current_script_directory, "1_depth_conversion.py")
script2 = os.path.join(current_script_directory, "2_add_x_location.py")
script3 = os.path.join(current_script_directory, "3_merge_to_one_txt.py")
script4 = os.path.join(current_script_directory, "4_plot_scatter.py")
script5 = os.path.join(current_script_directory, "5_plot_interpolation.py")


# Execute the first script
try:
    result1 = subprocess.run(['python', script1, inversion_path], check=True, capture_output=True, text=True, encoding='utf-8')
    output_folder_1 = result1.stdout.strip()
    print(f"First script output:\n{output_folder_1}")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running the first script:\n{e.stderr}")
    sys.exit(1)

# Execute the second script
try:
    result2 = subprocess.run(['python', script2, output_folder_1], check=True, capture_output=True, text=True, encoding='utf-8')
    print(f"Second script raw output:\n{result2.stdout}")
    output_folder_2 = result2.stdout.strip().split("\n")[-1].strip()
    print(f"Second script output:\n{output_folder_2}")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running the second script:\n{e.stderr}")
    sys.exit(1)

# Execute the third script
try:
    result3 = subprocess.run(['python', script3, output_folder_2], check=True, capture_output=True, text=True, encoding='utf-8')
    output_file = result3.stdout.strip()
    print(f"Third script output:\n{output_file}")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running the third script:\n{e.stderr}")
    sys.exit(1)

# Execute the fourth script
try:
    result4 = subprocess.run(['python', script4, output_file], check=True, capture_output=True, text=True, encoding='utf-8')
    print(f"Fourth script output:\n{result4.stdout}")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running the fourth script:\n{e.stderr}")
    sys.exit(1)

# Execute the fifth script
try:
    result5 = subprocess.run(['python', script5, output_file], check=True, capture_output=True, text=True, encoding='utf-8')
    print(f"Fifth script output:\n{result5.stdout}")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running the fifth script:\n{e.stderr}")
    sys.exit(1)

print("All scripts executed successfully.")
