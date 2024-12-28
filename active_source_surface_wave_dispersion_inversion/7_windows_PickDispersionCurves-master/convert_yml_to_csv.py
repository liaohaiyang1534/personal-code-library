import os
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import shutil

# Input file path
filename = r"E:\lhyonedrive\OneDrive\shangyuanmen\2401_seismic_vibrator_truck\data_processing\surface_wave_processing\line3_p\shots_240409_MASW_processed_sgy_1\arraylength_85.0m_offset_minoff_19.5m_spacing_1.5m_103_1st_0.5m_913_gx_fk_fre_ener_1_sac_FJ_dispersion.yml"

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
