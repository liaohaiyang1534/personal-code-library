import os
import glob
import subprocess

# 定义目录路径
directory_path = r"F:\SYM\ResultS_line1_60traces_1_tracesinterval_0124-13-20\h5_2_20240811"

# 获取目录下所有的 .h5 文件
h5_files = glob.glob(os.path.join(directory_path, "*.h5"))

# 打印获取到的 .h5 文件列表
print(f"Found {len(h5_files)} .h5 files: {h5_files}")

# 新建一个带后缀 _picked_yml 的文件夹
new_directory_path = directory_path + "_disp_curve"
os.makedirs(new_directory_path, exist_ok=True)

# 遍历所有文件并调用另一个 Python 脚本
for file_path in h5_files:
    try:
        print(f"Processing file: {file_path}")
        result = subprocess.run(
            ["python", r"./pick_dispersion_curves_passive_imaging_FJ", file_path, new_directory_path],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error processing file {file_path}: {e}")
        print(f"Output: {e.output}")
        print(f"Error output: {e.stderr}")

print("All files have been processed.")
