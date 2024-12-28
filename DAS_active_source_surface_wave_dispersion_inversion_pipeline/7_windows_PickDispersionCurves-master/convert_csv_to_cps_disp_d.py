import pandas as pd
import numpy as np 

data_name = 'dispersion_curve_edit.csv'
# 读取全部数据
# data = pd.read_csv(data_name)
data = pd.read_csv(data_name, sep=',')

# def process_row(row):
    # return row[0].split(',') if len(row) == 1 and ',' in row[0] else row
def process_row(row):
    return row[0].split(',') if len(row) == 1 and ' ' in row[0] else row

with open(data_name, 'r') as file:
    rows = [process_row(line.strip().split(',')) for line in file.readlines()[1:]]

init_columns = len(rows[0])
assert(init_columns % 2 == 0)

# 循环每二列进行处理
for i in range(0, init_columns, 2):
    main_columns = [data.columns[i], data.columns[i+1]]
    # 取出对应的两列数据
    # current_rows = [[row[i], row[i+1]] for row in rows]
    current_rows = [[row[i], row[i+1]] for row in rows if len(row) >= i+2]
    df = pd.DataFrame(current_rows, columns=main_columns)

    # 替换空字符串为 np.nan
    df.replace('', np.nan, inplace=True)

    # 删除包含 np.nan 的行
    df.dropna(inplace=True)

    df = df.astype(float)
    
    # 提取第一列第二个字符，更新prefix 
    char = main_columns[0][1]
    prefix = f"SURF96 R C X {char} "
    suffix = " 0.01"
    
    df['BBB'] = np.round(1/df[main_columns[0]], 8)
    df['CCC'] = np.round(df[main_columns[1]]/1000, 8)
    
    df['NewData'] = df.apply(lambda row: prefix + "{:.8f} {:.8f}".format(row['BBB'], row['CCC']) + suffix, axis=1)
    
    df['NewData'].to_csv(f'dispersion_curve_final_{i // 2 + 1}.disp', index=False, header=False)





# 获取所有需要合并的文件名
filenames = [f'dispersion_curve_final_{i + 1}.disp' for i in range(init_columns // 2)]

# 打开你想写入的文件
with open('dispersion_curve_final_all.disp', 'w') as outfile:
    for fname in filenames:
        # 打开每一个文件
        with open(fname) as infile:
            # 将每一个文件的内容写入到你想写入的文件中
            for line in infile:
                outfile.write(line)

# 删除单独的文件（如果需要）
for fname in filenames:
    os.remove(fname)