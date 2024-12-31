import numpy as np
import matplotlib.pyplot as plt
import os

# Specify the path to the npz file
file_path = r"F:\SYM\ResultS_line1_10_traces_CCF\outputImage\CCF\2024-01-24\2024-01-24 13-00-19 13-01-19 211 to 221.npz"
output_dir = r"F:\SYM\ResultS_line1_10_traces_CCF\outputImage\CCF\2024-01-24"

# Load the npz file
data = np.load(file_path)

# Get cross-correlation function data and frequency data
ncfs = data['ncfs']
frequencies = data['f']
station_pairs_names = data['station_pairs_names']

# Print debug information
print("ncfs shape:", ncfs.shape)
print("frequencies shape:", frequencies.shape)
print("station_pairs_names shape:", station_pairs_names.shape)
print("First few elements of ncfs:", ncfs[:5])
print("First few elements of frequencies:", frequencies[:5])
print("First few elements of station_pairs_names:", station_pairs_names[:5])

# Filter station pairs containing "0211"
filtered_indices = [i for i, station_pair in enumerate(station_pairs_names) if '0211' in station_pair]
filtered_station_pairs = [station_pairs_names[i] for i in filtered_indices]
filtered_ncfs = ncfs[filtered_indices]

# Print filtered debug information
print("filtered_station_pairs shape:", len(filtered_station_pairs))
print("filtered_ncfs shape:", filtered_ncfs.shape)
print("First few elements of filtered_ncfs:", filtered_ncfs[:5])

# Calculate the time series
dt = 1 / np.max(frequencies)
t = (np.linspace(-len(frequencies) / 2, len(frequencies) / 2 - 1, len(frequencies)) + 0.5) * dt

# Compute the time-domain representation of cross-correlation functions
ncfst = np.array([np.real(np.fft.fftshift(np.fft.ifft(filtered_ncfs[i, :]))) for i in range(len(filtered_ncfs))])

# Print debug information again
print("ncfst shape:", ncfst.shape)
print("First few elements of ncfst:", ncfst[:5])
print("t shape:", t.shape)
print("First few elements of t:", t[:5])

# Plot and save the image
fig, ax = plt.subplots(ncols=1, figsize=(7, 7))
for i in range(len(filtered_station_pairs)):
    y_values = np.real(ncfst[i, :]) / np.max(np.real(ncfst[i, :])) * 1 + i
    ax.plot(t, y_values, 'k', linewidth=0.2)
    print(f"Plotting station pair {filtered_station_pairs[i]} with y-values: {y_values[:10]}")

ax.set_xlim([-1.0, 1.0])
ax.set_ylim(bottom=0)
plt.xlabel('Time (s)', fontsize=9, family='Times New Roman')
plt.ylabel('Station Pair Index', fontsize=9, family='Times New Roman')
plt.title('Cross-correlation in Time Domain (Pairs including 0211)', fontsize=9, family='Times New Roman')
plt.xticks(fontsize=9, family='Times New Roman')
plt.yticks(fontsize=9, family='Times New Roman')

# Save the image
output_path = os.path.join(output_dir, 'Cross-correlation_TimeDomain_0211_Pairs.png')
plt.savefig(output_path)
plt.close()
print(f'Cross-correlation plot saved: {output_path}')
