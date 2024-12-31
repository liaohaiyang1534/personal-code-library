import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# Set font
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 9

# Load data
input_file = r"\\?\H:\lhyonedrive\OneDrive\termite\school\active_source_2\shots_510_610_split_removebad_shottimematch_ALL_dispersion_6_18_disp_curve_adjusted_inversion_left_depthtxt_txts_onetxt\shots_510_610_split_removebad_shottimematch_ALL_dispersion_6_18_disp_curve_adjusted_inversion_left_depthtxt_txts.txt"
data = np.loadtxt(input_file)

# Extract column data
x = data[:, 0]  # First column: x (distance in meters)
z = data[:, 1]  # Second column: z (depth in meters)
vs = data[:, 2]  # Third column: Vs (shear-wave velocity in m/s)

cmap = 'jet'  # Set colormap
levels = 50  # Define the number of contour levels
h = 8.0  # Smoothing parameter for SPI
method = 'spi'  # Smoothing method

# Filter out data where z < -5
mask = z >= -5
x = x[mask]
z = z[mask]
vs = vs[mask]

# Smooth Particle Interpolation (SPI) method
def gaussian_kernel(r, h):
    """Gaussian kernel function for SPI."""
    q = r / h
    if q <= 1.0:
        return (1.0 - q) ** 3
    else:
        return 0.0

def spi(x, z, vs, xi, zi, h):
    """Perform SPI interpolation."""
    vs_interpolated = np.zeros_like(xi)
    for i in range(xi.shape[0]):
        for j in range(xi.shape[1]):
            num = 0.0
            denom = 0.0
            for k in range(len(x)):
                r = np.sqrt((xi[i, j] - x[k]) ** 2 + (zi[i, j] - z[k]) ** 2)
                weight = gaussian_kernel(r, h)
                num += weight * vs[k]
                denom += weight
            vs_interpolated[i, j] = num / denom if denom != 0 else 0
    return vs_interpolated

# Define grid points for interpolation
x_range = np.linspace(min(x), max(x), 100)
z_range = np.linspace(min(z), max(z), 100)
xi, zi = np.meshgrid(x_range, z_range)

# Perform SPI interpolation
vs_interpolated = spi(x, z, vs, xi, zi, h)

# Plot the results
fig, ax = plt.subplots(figsize=(6, 4))
cmap = plt.get_cmap('jet')
levels = np.linspace(0, 300, 50)  # Define contour levels for Vs range (0-300 m/s)
norm = Normalize(vmin=0, vmax=300)
cf = ax.contourf(xi, zi, vs_interpolated, levels=levels, cmap=cmap, norm=norm)
cbar = plt.colorbar(cf, ax=ax, orientation='vertical')
cbar.set_label('Vs (m/s)')

# Display and save the figure
plt.title('SPI Interpolated Vs')
plt.xlabel('Distance (m)')
plt.ylabel('Depth (m)')
plt.gca().invert_yaxis()  # Invert y-axis to match depth convention
plt.show()
