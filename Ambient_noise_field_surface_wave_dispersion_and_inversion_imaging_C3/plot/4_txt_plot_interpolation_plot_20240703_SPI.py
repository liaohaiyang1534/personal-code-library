import numpy as np
import matplotlib.pyplot as plt
import os

# Set font for plots
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 9

# Load data from input file
input_file = r"\\?\H:\lhyonedrive\OneDrive\termite\school\active_source_2\shots_510_610_split_removebad_shottimematch_ALL_dispersion_6_18_disp_curve_adjusted_inversion_left_depthtxt_txts_onetxt\shots_510_610_split_removebad_shottimematch_ALL_dispersion_6_18_disp_curve_adjusted_inversion_left_depthtxt_txts.txt"
data = np.loadtxt(input_file)

# Extract columns from the data
x = data[:, 0]  # First column: x (distance in meters)
z = data[:, 1]  # Second column: z (depth in meters)
vs = data[:, 2]  # Third column: Vs (shear-wave velocity in m/s)

# Filter out data where z is less than -6
mask = z >= -6
x = x[mask]
z = z[mask]
vs = vs[mask]

# Smooth Particle Interpolation (SPI) method
def gaussian_kernel(r, h):
    """
    Gaussian kernel function for SPI interpolation.
    Args:
        r (float): Distance between two points.
        h (float): Smoothing parameter.
    Returns:
        float: Kernel weight.
    """
    q = r / h
    if q <= 1.0:
        return (1.0 - q)**3
    else:
        return 0.0

def spi(x, z, vs, xi, zi, h):
    """
    Perform Smooth Particle Interpolation (SPI).
    Args:
        x (array): Array of x-coordinates.
        z (array): Array of z-coordinates.
        vs (array): Array of Vs values.
        xi (array): Grid x-coordinates for interpolation.
        zi (array): Grid z-coordinates for interpolation.
        h (float): Smoothing parameter for the kernel.
    Returns:
        array: Interpolated Vs values on the grid.
    """
    vs_interpolated = np.zeros_like(xi)
    for i in range(xi.shape[0]):
        for j in range(xi.shape[1]):
            num = 0.0
            denom = 0.0
            for k in range(len(x)):
                r = np.sqrt((xi[i, j] - x[k])**2 + (zi[i, j] - z[k])**2)
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
h = 8.0  # Smoothing parameter
vs_interpolated = spi(x, z, vs, xi, zi, h)
