import os
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import shutil
import sys

print("当前工作目录:", os.getcwd())

# Input file path
# filename = r"E:\lhyonedrive\OneDrive\shangyuanmen\2401_seismic_vibrator_truck\data_processing\surface_wave_processing\line3_p\shots_240409_MASW_processed_sgy_1\arraylength_85.0m_offset_minoff_19.5m_spacing_1.5m_103_1st_0.5m_913_gx_fk_fre_ener_1_sac_FJ_dispersion.yml"


filename = sys.argv[1]



# Extract base file name without extension for output file naming
base_filename = os.path.splitext(os.path.basename(filename))[0]

# Loading data from the YAML file
with open(filename, 'r') as file:
    data = yaml.safe_load(file)

# Preparing the DataFrame
columns = []
df = pd.DataFrame()
for key1 in data:
    for key2 in data[key1]:
        f_key = f'{key1}{key2}f'
        c_key = f'{key1}{key2}c'
        columns.append(f_key)
        columns.append(c_key)
        if data[key1][key2]['f'] is not None:
            df[f_key] = pd.Series(data[key1][key2]['f'])
        if data[key1][key2]['c'] is not None:
            df[c_key] = pd.Series(data[key1][key2]['c'])

# Generating output file names based on the input file name
csv_filename = f'{base_filename}.csv'
copied_csv_filename = f'{base_filename}_edit.csv'
image_filename = f'{base_filename}.png'

# Save DataFrame to CSV
df.to_csv(csv_filename, index=False, columns=columns, sep=',')

# Copy the CSV file
shutil.copy(csv_filename, copied_csv_filename)

# Plotting
fig, ax = plt.subplots()
for i in range(0, len(columns), 2):
    f_col = columns[i]
    c_col = columns[i+1]
    f_data = df[f_col].dropna()
    c_data = df[c_col].dropna()
    slice_number = int(f_col[:-1])
    ax.plot(f_data, c_data, 'o-', label=f'Slice {slice_number}')

ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Phase Velocity (m/s)')
ax.legend()

# Save the plot
plt.savefig(image_filename)
plt.show()









# Import necessary libraries
import pandas as pd
import numpy as np
import os

# Use the base_filename from the earlier part of the script
data_name = copied_csv_filename

# Read the CSV file
data = pd.read_csv(data_name, sep=',')

def process_row(row):
    return row[0].split(',') if len(row) == 1 and ' ' in row[0] else row

with open(data_name, 'r') as file:
    rows = [process_row(line.strip().split(',')) for line in file.readlines()[1:]]

init_columns = len(rows[0])
assert(init_columns % 2 == 0)

# Loop through each pair of columns for processing
for i in range(0, init_columns, 2):
    main_columns = [data.columns[i], data.columns[i+1]]
    current_rows = [[row[i], row[i+1]] for row in rows if len(row) >= i+2]
    df = pd.DataFrame(current_rows, columns=main_columns)
    df.replace('', np.nan, inplace=True)
    df.dropna(inplace=True)
    df = df.astype(float)

    char = main_columns[0][1]
    prefix = f"SURF96 R C X {char} "
    suffix = " 0.01"

    df['BBB'] = np.round(1/df[main_columns[0]], 8)
    df['CCC'] = np.round(df[main_columns[1]]/1000, 8)

    df['NewData'] = df.apply(lambda row: prefix + "{:.8f} {:.8f}".format(row['BBB'], row['CCC']) + suffix, axis=1)

    # Save the processed data to .disp file with a name based on the input file
    df['NewData'].to_csv(f'{base_filename}_final_{i // 2 + 1}.disp', index=False, header=False)

# Generate the filenames for merging based on the input file name
filenames = [f'{base_filename}_final_{i + 1}.disp' for i in range(init_columns // 2)]


final_disp_filename = os.path.join(os.getcwd(), f'{base_filename}_final_all.disp')



# Merge the .disp files into one, naming it based on the input file
with open(final_disp_filename, 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())

# Optionally, delete the individual .disp files
for fname in filenames:
    os.remove(fname)














# # List of all generated files
# generated_files = [
#     csv_filename,
#     copied_csv_filename,
#     image_filename,
#     final_disp_filename
# ]

# # Move all generated files into the parent directory
# for file in generated_files:
#     # Construct the destination path by joining the parent directory with the basename of the file
#     dest_path = os.path.join(parent_dir, os.path.basename(file))
    
#     # Move the file
#     shutil.move(file, dest_path)








