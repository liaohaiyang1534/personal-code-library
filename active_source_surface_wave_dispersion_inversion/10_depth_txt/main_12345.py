import subprocess
import sys

# Paths to input and scripts
# Modification 1: Set the inversion path
inversion_path = r"I:\diff_dis_to_cavity\RESULTS_2024-06-29_sgy_60x4-60x6\dispersion_curve_revise_inversion_model5\best_model"

# Paths to scripts
script2 = r"H:\CODE\ambient_noise_dispersion_C3\result_plot\1-depth_transform.py"
script3 = r"H:\CODE\ambient_noise_dispersion_C3\result_plot\3-txts_to_txt.py"
script4 = r"H:\CODE\ambient_noise_dispersion_C3\result_plot\4-plot_scatters.py"
script5 = r"H:\CODE\ambient_noise_dispersion_C3\result_plot\5-plot_final_pic.py"

# Execute the second script
try:
    result2 = subprocess.run(['python', script2, inversion_path], check=True, capture_output=True, text=True, encoding='utf-8')
    print(f"Second script raw output:\n{result2.stdout}")
    output_folder_2 = result2.stdout.strip().split("\n")[-1].strip()  # Extract the last line of the output
    print(f"Second script output:\n{output_folder_2}")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running the second script:\n{e.stderr}")
    sys.exit(1)

# Execute the third script
try:
    result3 = subprocess.run(['python', script3, output_folder_2], check=True, capture_output=True, text=True, encoding='utf-8')
    output_file = result3.stdout.strip()  # Capture the output file path
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
