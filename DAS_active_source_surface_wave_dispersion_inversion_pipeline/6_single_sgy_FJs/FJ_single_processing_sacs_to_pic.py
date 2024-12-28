print("Starting execution...")
import matplotlib
matplotlib.use('Agg')  # Use Agg backend
import os
from matplotlib import pyplot as plt
import obspy
import numpy as np
import ccfj
import sys
import h5py

folder_path = sys.argv[1]

print("Reading SAC files...")
st = obspy.core.stream.Stream()
sac_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.sac')]
for sac_file in sac_files:
    st += obspy.read(sac_file)

nst = len(st)
nwin = 1

nf = 120

minc = 10
maxc = 600
nc = 120

tmp = []
for a in st:
    tmp.append(a.stats.sac['npts'])
npts = min(tmp)

T = np.linspace(0, npts-1, npts) * st[0].stats.sac['delta']

u0 = np.zeros([nst, npts])
winl = np.zeros([nwin, nst])
winr = np.zeros([nwin, nst])
r = np.zeros(nst)
Fs = 1.0 / st[0].stats.sac['delta']
f = Fs * np.linspace(0, nf-1, nf) / npts
c = np.linspace(minc, maxc, nc)

print("Processing SAC file data...")
for i in range(nst):
    u0[i, :] = st[i].data[0:npts]
    r[i] = st[i].stats.sac['dist']
    winl[0, i] = 0
    winr[0, i] = npts - 1

indx = np.argsort(r)
u0 = u0[indx, :]
r = r[indx] * 1000
winl = winl[:, indx]
winr = winr[:, indx]

print("Performing FJ transformation...")
out1 = ccfj.MWFJ(u0, r, c, f, Fs, nwin, winl, winr, func=1)

vmax = 1.05

fmax_display = 50  # Maximum frequency to display
fmax_data = 100  # Maximum frequency in the data

# Select 0-50Hz data for display
f_display_indices = np.where(f <= fmax_display)[0]
out1_display = out1[:, :, f_display_indices]
f_display = f[f_display_indices]

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Only plot with smooth interpolation
im = ax.imshow(np.flip(out1_display[0, :, :], 0), extent=[1, fmax_display, min(c/1e3), max(c/1e3)],
          aspect='auto', vmax=vmax, cmap='jet', interpolation='bilinear')

# Adjust x-axis range
ax.set_xlim([3, fmax_display])
ax.set_ylim([min(c/1e3), max(c/1e3)])
ax.set_xlabel('Frequency (Hz)', fontsize=12, fontname='Times New Roman')
ax.set_ylabel('Phase velocity (km/s)', fontsize=12, fontname='Times New Roman')
ax.set_title('Dispersion Analysis', fontsize=14, fontname='Times New Roman')

# Add colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Amplitude', fontsize=12, fontname='Times New Roman')

# Set the overall title for the figure
plt.suptitle(os.path.basename(folder_path) + " FJ Dispersion Analysis", fontsize=16, fontname='Times New Roman', y=0.95)

# Adjust subplot margins
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

# Use tight layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Generate image file name based on the folder name
image_file_name = os.path.basename(folder_path) + "_FJ_dispersion.png"
image_file_path = os.path.join(os.path.dirname(folder_path), image_file_name)

# Save the figure
plt.savefig(image_file_path, dpi=100, bbox_inches='tight')
plt.close()

# Generate .h5 file name based on the image file name
h5_file_name = image_file_name.replace(".png", ".h5")
h5_file_path = os.path.join(os.path.dirname(folder_path), h5_file_name)

ds = [out1_display]
ds = np.array(ds)
np.shape(ds)

h5file = h5py.File(h5_file_path, 'w')
h5file.create_dataset('ds', data=ds)
h5file.create_dataset('f', data=f_display)
h5file.create_dataset('c', data=c)
h5file.close()

print("Task completed...")
