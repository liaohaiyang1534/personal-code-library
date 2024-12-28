import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('dispersion_curve_edit.csv', sep='\t') # read the csv file

columns = df.columns.to_list()

fig, ax = plt.subplots()

# iterate over the columns
for i in range(0, len(columns), 2):
    f_col = columns[i]
    c_col = columns[i+1]
    f_data = df[f_col].dropna()  
    c_data = df[c_col].dropna()
    slice_number = int(f_col[:-1])  
    ax.plot(f_data, c_data, 'o-', label=f'{slice_number}') 

ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Phase Velocity (m/s)')
ax.legend()
plt.savefig("dispersion curve.png")
plt.show()
plt.close()