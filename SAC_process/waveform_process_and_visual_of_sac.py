from obspy import read
import matplotlib.pyplot as plt
import os

def plot_saved_sac(file_name, output_directory, suffix):
    """ Read and plot signal from SAC file, then save the image """
    st = read(file_name)
    tr = st[0]  # Get the first trace
    plt.figure(figsize=(20, 4))
    plt.plot(tr.times(), tr.data)
    plt.title(f'{suffix} Waveform')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.savefig(os.path.join(output_directory, file_name.replace('.sac', f'_{suffix}.png')))
    plt.show()

# Path to the SAC file
sac_file_path = r"H:\github\personal-code-library\SAC_process\2024-01-24-11-17-19-out0012.sac"

# Read the SAC file
st = read(sac_file_path)
tr = st[0]  # Get the first trace

# Define the time range
start_time = tr.stats.starttime + 38.8  # Start at 38.8 seconds after the start
end_time = start_time + 9.9  # Duration of 9.9 seconds

# Trim the trace for the specified time range
tr_trimmed = tr.slice(start_time, end_time)

# Specify the output directory
output_directory = r"H:\github\personal-code-library\SAC_process\TEST"

os.makedirs(output_directory, exist_ok=True)

# Get the original file name (without path)
sac_filename = os.path.basename(sac_file_path)

# Save the trimmed SAC file
trimmed_file_name = sac_filename.replace('.sac', '_trimmed.sac')
trimmed_file_path = os.path.join(output_directory, trimmed_file_name)
tr_trimmed.write(trimmed_file_path, format='SAC')

# Plot and save the original waveform
plot_saved_sac(sac_file_path, output_directory, 'original')

# Plot and save the trimmed waveform
plot_saved_sac(trimmed_file_path, output_directory, 'trimmed')

# Further refine the time range, e.g., zoom in on 2-3 seconds
zoom_start_time = start_time + 2.5
zoom_end_time = start_time + 3
tr_zoomed = tr_trimmed.slice(zoom_start_time, zoom_end_time)

# Calculate relative time
relative_times = tr_zoomed.times() - (zoom_start_time - tr_trimmed.stats.starttime)

# Plot and save the zoomed waveform
plt.figure(figsize=(20, 4))
plt.plot(relative_times, tr_zoomed.data)
plt.title('Zoomed Waveform (2.5-3 sec)')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid()
zoomed_waveform_image_path = os.path.join(output_directory, sac_filename.replace('.sac', '_zoomed_waveform.png'))
plt.savefig(zoomed_waveform_image_path)
plt.show()
