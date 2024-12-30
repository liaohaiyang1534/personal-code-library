import os
from obspy import read
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# Set font to Times New Roman
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.size'] = 9  # Set font size to 9pt

# Path to the SAC folder
folder_path = r"H:\github\personal-code-library\SAC_process\sac_sample"

# Read all SAC files in the folder
sac_files = [f for f in os.listdir(folder_path) if f.endswith('.sac')]

# Correctly extract and sort trace numbers from file names
sac_files.sort(key=lambda x: int(x.split('out')[1].split('.')[0]))

# Create a canvas and adjust to a smaller size
fig, ax = plt.subplots(figsize=(2.5, 3))

# Reduce border whitespace while keeping enough space for axes and labels
fig.subplots_adjust(left=0.15, right=0.95, bottom=0.15, top=0.95)

# Initialize minimum and maximum distances for plotting range
min_distance = float('inf')
max_distance = float('-inf')

# Iterate through each file, read and plot waveforms
for i, sac_file in enumerate(sac_files):
    # Construct full path
    full_path = os.path.join(folder_path, sac_file)
    # Read SAC file
    st = read(full_path)
    trace = st[0]
    
    # Extract trace number from file name
    trace_number = int(sac_file.split('out')[1].split('.')[0])
    # Calculate actual distance: (trace_number - 180) * 0.5
    distance = (trace_number - 180) * 0.5
    min_distance = min(min_distance, distance)
    max_distance = max(max_distance, distance)
    
    # Normalize waveform amplitude and shift by distance
    normalized_waveform = trace.data / np.max(np.abs(trace.data))
    ax.plot(trace.times(), normalized_waveform + distance, color='black', linewidth=0.01)

# Set axis view limits to reduce whitespace between waveforms and the frame
ax.set_xlim([np.min(trace.times()), np.max(trace.times())])
ax.set_ylim([min_distance - 1, max_distance + 1])  # Add a small margin to prevent cutting off waveforms

# Set axis labels
ax.set_xlabel('Time (s)')
ax.set_ylabel('Distance (m)')

# Save as a PNG file with high resolution
output_path = os.path.join(folder_path, "waveform_plot.png")
plt.savefig(output_path, dpi=1000, bbox_inches='tight', pad_inches=0.05)
plt.close()

print(f"Waveform plot saved at {output_path}")
