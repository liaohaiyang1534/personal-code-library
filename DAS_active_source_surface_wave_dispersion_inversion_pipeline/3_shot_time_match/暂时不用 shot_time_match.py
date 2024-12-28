import re
import shutil
import os
import sys
from datetime import datetime, timedelta

def extract_datetime_from_filename(filename):
    # 使用正则表达式从文件名中提取日期和时间
    pattern = r'(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})\.\d{3}_output\.sgy'
    match = re.search(pattern, filename)
    
    if match:
        # 提取匹配的日期和时间部分
        datetime_str = match.group(1)
        return datetime_str
    else:
        return None

def adjust_time_range(datetime_str):
    # 将时间字符串转换为datetime对象
    date_time_obj = datetime.strptime(datetime_str, '%Y-%m-%d-%H-%M-%S')
    # 生成前后1秒的时间区间
    time_before = (date_time_obj - timedelta(seconds=1)).strftime('%Y-%m-%d-%H-%M-%S')
    time_after = (date_time_obj + timedelta(seconds=1)).strftime('%Y-%m-%d-%H-%M-%S')
    return [time_before, datetime_str, time_after]

def find_and_copy_sgy(file_path, time_range, original_sgy_path, output_folder):
    try:
        with open(file_path, 'r') as file:
            matching_lines = []
            for line in file:
                # 假设文件的列用空格或制表符分隔
                columns = line.strip().split()
                if columns and columns[0] in time_range:
                    matching_lines.append(columns)

            # 检查匹配结果
            if len(matching_lines) == 0:
                print("No matching times found. This is an exception.")
                return 1
            elif len(matching_lines) > 1:
                print("Multiple matching times found. This may be an exception.")
                for match in matching_lines:
                    print("Matching line:", match)
                return 2
            else:
                print("Single matching time found. This is normal.")
                prefix = matching_lines[0][1]

                # 创建新的SGY文件名并复制文件
                new_sgy_filename = f"{prefix}_{os.path.basename(original_sgy_path)}"
                new_sgy_path = os.path.join(output_folder, new_sgy_filename)
                shutil.copy2(original_sgy_path, new_sgy_path)
                print(f"New SGY file created: {new_sgy_path}")
                return 0
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return 3

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: shot_time_link.py <txt_file_path> <input_sgy_path> <output_folder>")
        sys.exit(1)
    
    txt_file_path = sys.argv[1]
    input_sgy_path = sys.argv[2]
    output_folder = sys.argv[3]

    datetime_str = extract_datetime_from_filename(input_sgy_path)

    if datetime_str:
        print("Extracted datetime:", datetime_str)
        time_range = adjust_time_range(datetime_str)
        print("Time range:", time_range)
    else:
        print("Filename format is incorrect.")
        sys.exit(1)

    result = find_and_copy_sgy(txt_file_path, time_range, input_sgy_path, output_folder)
    sys.exit(result)
