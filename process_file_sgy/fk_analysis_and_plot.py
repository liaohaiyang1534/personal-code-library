# -*- encoding: utf-8 -*-
'''
@File        :   fk_analysis_and_plot.py
@Time        :   2025/01/03 22:45:45
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''

import numpy as np
import segyio
from segyio import TraceField
from obspy import Stream, Trace
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def get_trace_coordinates_from_segy(file_path):
    print(f"Getting trace coordinates from SEG-Y: {file_path}")
    with segyio.open(file_path, "r", ignore_geometry=True) as f:
        n_traces = len(f.trace)
        coordinates = np.zeros((n_traces, 2), dtype=float)
        for i in range(n_traces):
            x = f.header[i][TraceField.GroupX]
            y = 0
            coordinates[i] = [x, y]
    return coordinates

def fk_analysis(st, input_file, smax, fmin, fmax, tmin, tmax, stat='power'):
    print(f"Performing FK analysis on: {input_file}")
    start_time = st[0].stats.starttime
    tmin_utc = start_time + tmin
    tmax_utc = start_time + tmax
    st = st.copy().trim(starttime=tmin_utc, endtime=tmax_utc)
    st.detrend()
    st.taper(type='cosine', max_percentage=0.05)
    st = st.copy().filter("bandpass", freqmin=fmin, freqmax=fmax)
    npts = st[0].stats.npts
    delta = st[0].stats.delta
    nbeam = len(st)
    fft_st = np.zeros((nbeam, int((npts // 2) + 1)), dtype=complex)
    for i, tr in enumerate(st):
        fft_st[i, :] = np.fft.rfft(tr.data)
    freqs = np.fft.rfftfreq(npts, delta)
    slow_x = np.linspace(-smax, smax, nbeam)
    slow_y = np.linspace(-smax, smax, nbeam)
    coordinates = get_trace_coordinates_from_segy(input_file)
    x, y = np.split(coordinates[:, :2], 2, axis=1)
    x /= 1000.
    y /= 1000.
    dt_x = np.outer(slow_x, x)
    dt_y = np.outer(slow_y, y)
    dt_total = dt_x[:, :, np.newaxis] + dt_y[:, :, np.newaxis]
    exp_term = np.exp(-1j * 2 * np.pi * dt_total * freqs)
    beam_sum = np.sum(exp_term * fft_st, axis=2) / nbeam
    fk = np.abs(beam_sum)**2
    if stat == 'semblance' or stat == 'F':
        tracepower = np.vdot(fft_st, fft_st).real
        if stat == 'semblance':
            fk_semb = nbeam * fk / tracepower
            return fk_semb
        elif stat == 'F':
            fk_F = (nbeam - 1) * nbeam * fk / (tracepower - nbeam * fk)
            return fk_F
    else:
        return fk

def convert_array_to_stream(data, dt):
    print("Converting data to stream")
    stream = Stream()
    for i in range(data.shape[1]):
        trace = Trace(data[:, i])
        trace.stats.delta = dt
        stream.append(trace)
    return stream

def fk_plot(fk_result, dx, dt, fmin, fmax, kmin, kmax, input_file):
    print("Processing: Calculating frequencies and wavenumbers...")
    freqs = np.fft.rfftfreq(fk_result.shape[0], dt)
    freq_indices = np.where((freqs >= fmin) & (freqs <= fmax))[0]
    kx_max = np.pi / dx
    kx = np.linspace(-kx_max, kx_max, fk_result.shape[1])
    k_indices = np.where((kx >= kmin) & (kx <= kmax))[0]
    fk_selected = fk_result[np.ix_(freq_indices, k_indices)]
    print("Processing: Creating plot object...")
    fig, ax = plt.subplots(figsize=(8, 6))
    print("Processing: Plotting FK analysis results...")
    c = ax.contourf(kx[k_indices], freqs[freq_indices], fk_selected, 20, cmap='jet')
    print("Processing: Setting title and axis labels...")
    ax.set_title("FK Analysis", y=1.1)
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    ax.set_xlabel('Wavenumber (rad/m)')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_ylim(fmax, fmin)
    print("Processing: Adding color bar...")
    fig.colorbar(c, ax=ax)
    output_path = input_file + "_fk_analysis.png"
    print("Processing: Saving image file...")
    plt.savefig(output_path)
    plt.close()
    print(f"FK analysis plot saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 11:
        print("Usage: python fk_analysis_and_plot.py <input_segy> dt dx smax fmin fmax tmin tmax kmin kmax")
        sys.exit(1)
    input_segy = sys.argv[1]
    dt = float(sys.argv[2])
    dx = float(sys.argv[3])
    smax = float(sys.argv[4])
    tmin = float(sys.argv[5])
    tmax = float(sys.argv[6])
    fmin = float(sys.argv[7])
    fmax = float(sys.argv[8])
    kmin = float(sys.argv[9])
    kmax = float(sys.argv[10])

    print(f"Processing file: {input_segy}")
    with segyio.open(input_segy, "r", ignore_geometry=True) as src:
        data = segyio.tools.collect(src.trace[:])
    st = convert_array_to_stream(data.T, dt)
    fk_result = fk_analysis(st, input_segy, smax, fmin, fmax, tmin, tmax)
    fk_plot(fk_result, dx, dt, fmin, fmax, kmin, kmax, input_segy)
    print("FK analysis and plotting completed.")
