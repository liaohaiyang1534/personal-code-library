import os
import shutil
import obspy
from obspy.core import Trace, Stream
import numpy as np
from scipy.fftpack import fft, ifft
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import re
from obspy import UTCDateTime
import ccfj
from ccfj import CC, GetStationPairs
from concurrent.futures import ThreadPoolExecutor, as_completed
from geopy.distance import great_circle
from tqdm import tqdm
import h5py
import time
from obspy.signal.filter import lowpass
from matplotlib.font_manager import FontProperties, fontManager
import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set font
font_path = '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf'
matplotlib.font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 8

# Start time for the entire process
total_start_time = time.time()
time_records = {}

def record_time(step_name):
    time_records[step_name] = time.time()

# -------------------------------------------------------------------------------

# 20240627-0706 Yinji Data
suffix = "_TEST_20241004"
original_path = '/mnt/i/阴井/data_20240627-0706'
result_path = os.path.join(original_path, 'ResultS' + suffix)
no_arrange_file_path_list = ['/mnt/i/阴井/data_20240627-0706/2024-07-02_sac']

start_time_list = ['07-00-15']
end_time_list = ['14-00-15']

seismic_lines = [[90, 110]]
# Array arrangement length, number of stations
array_length = 20

# trace_interval, interval of trace arrangement
trace_interval = 1
Fs = sampling_rate = 500
nThreads = 20

# --------------------------------------------------------------------------------

fstride = 1
piece_time = 15
nf = piece_time * 50
fft_length = Fs * piece_time
overlap_rate = 0.9

f = np.arange(0, nf) * Fs / fft_length * fstride
cmin = 1
cmax = nc = 1200

Gauge_Length = [0.25]

Start_trace_list_Lm = []
End_trace_list_Lm = []

for line in seismic_lines:
    start_trace, end_trace = line
    start_list = list(range(start_trace, end_trace - array_length + 1, trace_interval))
    end_list = list(range(start_trace + array_length, end_trace + 1, trace_interval))
    Start_trace_list_Lm.append(start_list)
    End_trace_list_Lm.append(end_list)

Start_trace_list = [Start_trace_list_Lm]
End_trace_list = [End_trace_list_Lm]

Total_Start_Traces_list = [min(lst) for lst in Start_trace_list_Lm]
Total_End_Traces_list = [max(lst) for lst in End_trace_list_Lm]

# Add log statements
logging.info(f"Start_trace_list_Lm: {Start_trace_list_Lm}")
logging.info(f"End_trace_list_Lm: {End_trace_list_Lm}")
logging.info(f"Start_trace_list: {Start_trace_list}")
logging.info(f"End_trace_list: {End_trace_list}")
logging.info(f"Total_Start_Traces_list: {Total_Start_Traces_list}")
logging.info(f"Total_End_Traces_list: {Total_End_Traces_list}")

def create_clean_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def initialize_directories(result_path, date, suffix):
    paths = {
        "output": os.path.join(result_path, 'DataDemoSource' + suffix),
        "temp": os.path.join(result_path, 'DataDemoTem' + suffix),
        "merge": os.path.join(result_path, 'DataDemoMerge' + suffix),
        "amplitude_spectrum": os.path.join(result_path, 'outputImage/Amplitude Spectrum', date),
        "dispersion_curve": os.path.join(result_path, 'outputImage/Dispersion Curve', date),
        "egf": os.path.join(result_path, 'outputImage/EGF', date),
        "seismograms": os.path.join(result_path, 'outputImage/Seismograms', date),
        "h5": os.path.join(result_path, 'outputImage/H5', date),
        "ccf_file": os.path.join(result_path, 'outputImage/CCF', date),
        "output_file": os.path.join(result_path, 'outputfile', date)
    }
    for path in paths.values():
        create_clean_directory(path)
    return paths

def process_traces(start_traces, end_traces, path, start_time, end_time, output_path, info, gauge_length):
    func_start_time = time.time()
    time_folder_list = sorted(os.listdir(path))

    # Create directories for SAC files
    for i in range(start_traces, end_traces + 1):
        save_sac_path = os.path.join(output_path, f'NJU-{i:04d}-STA')
        create_clean_directory(save_sac_path)

    # Find the indices for start_time and end_time
    count1 = count2 = count3 = 1
    for folder in time_folder_list:
        if folder[11:19] == start_time:
            break
        count1 += 1
    for folder in time_folder_list:
        if folder[11:19] == end_time:
            break
        count2 += 1

    def copy_file(sac_file, process_file_path):
        shutil.copy(sac_file, process_file_path)

    with tqdm(total=len(time_folder_list), desc='Processing traces') as pbar, ThreadPoolExecutor(max_workers=nThreads) as executor:
        futures = []
        for folder in time_folder_list:
            if count1 <= count3 <= count2:
                sac_path = os.path.join(path, folder)
                sac_list = sorted(os.listdir(sac_path))
                for sac in sac_list:
                    try:
                        trace_num = int(sac[-8:-4])
                        if start_traces <= trace_num <= end_traces:
                            sac_file = os.path.join(sac_path, sac)
                            process_file_path = os.path.join(output_path, f'NJU-{trace_num:04d}-STA')
                            futures.append(executor.submit(copy_file, sac_file, process_file_path))
                    except ValueError:
                        logging.warning(f"Unexpected file name format: {sac}")
            count3 += 1
            pbar.update(1)
        for future in as_completed(futures):
            future.result()

    func_end_time = time.time()
    logging.info(f'{info} {start_traces} to {end_traces} {gauge_length} Transfer Done! Time taken: {func_end_time - func_start_time:.2f} seconds')
    return func_end_time - func_start_time

def downsample_and_filter(trace, target_sampling_rate, corner_frequency):
    trace.filter('lowpass', freq=corner_frequency)
    trace.resample(sampling_rate=target_sampling_rate)
    return trace

def merge_traces(folder, output_path, temp_path, target_sampling_rate, corner_frequency):
    func_start_time = time.time()
    path6 = os.path.join(output_path, folder)
    sac_list = sorted(os.listdir(path6))
    st = obspy.read(os.path.join(path6, sac_list[0]))
    trace = st[0]
    for sac in sac_list[1:]:
        st = obspy.read(os.path.join(path6, sac))
        trace += st[0]
    # Downsample and low-pass filter
    trace = downsample_and_filter(trace, target_sampling_rate, corner_frequency)
    merged_path = os.path.join(temp_path, folder)
    create_clean_directory(merged_path)
    trace.write(os.path.join(merged_path, f'{folder}-merge.sac'), format='SAC')
    func_end_time = time.time()
    return func_end_time - func_start_time

def generate_station_info(start_trace, end_trace, gauge_length, output_path, info):
    func_start_time = time.time()
    tmp_sta = list(range(start_trace, end_trace + 1))
    tmp_long = [118.96188946 + (0.00002478 * gauge_length * i) for i in tmp_sta]
    tmp_lat = [32.11321776 + (0.00000332 * gauge_length * i) for i in tmp_sta]
    station_info_file = os.path.join(output_path, 'stations_info.txt')
    with open(station_info_file, 'w', encoding='UTF-8') as file:
        for sta, lon, lat in zip(tmp_sta, tmp_long, tmp_lat):
            file.write(f'NJU-{sta:04d}-STA {lon:.8f} {lat:.8f}\n')
    logging.info(f'{info} Station info file written: {station_info_file}')
    return time.time() - func_start_time

def read_data(i, Dir, npts, data, startend, Fs, namelist):
    dirname = namelist[i]
    filename = os.path.join(Dir, dirname)
    filelist = sorted(os.listdir(filename))
    reading_file = filelist[0]  # Assuming only one file per directory
    file_path = os.path.join(filename, reading_file)
    st = obspy.read(file_path)
    trace = st[0]
    if trace.stats.npts >= npts:
        data[npts * i:npts * (i + 1)] = trace.data[:npts]
        startend[i * 2] = 0
        startend[i * 2 + 1] = npts
    else:
        t0 = trace.stats.starttime
        t1 = trace.stats.endtime
        idx0 = int((t0.second + t0.minute * 60 + (t0.hour - 11) * 3600) * Fs)
        idx1 = int((t1.second + t1.minute * 60 + (t1.hour - 11) * 3600) * Fs)
        data[(npts * i + idx0):(npts * i + idx1)] = trace.data[:idx1 - idx0]
        startend[i * 2] = idx0
        startend[i * 2 + 1] = idx1

def process_traces_with_thread_pool(Total_Start_Traces_list, Total_End_Traces_list, path, start_time, end_time, output_path, info, gauge_length):
    times = []
    with ThreadPoolExecutor(max_workers=nThreads) as executor:
        futures = [
            executor.submit(
                process_traces, start, end, path, start_time, end_time, output_path, info, gauge_length
            )
            for start, end in zip(Total_Start_Traces_list, Total_End_Traces_list)
        ]
        for future in as_completed(futures):
            times.append(future.result())
    return sum(times)

def merge_folders_with_thread_pool(folder_list, output_path, temp_path, target_sampling_rate=500, corner_frequency=50):
    total_tasks = len(folder_list)
    times = []

    def merge_and_record_time(folder):
        return merge_traces(folder, output_path, temp_path, target_sampling_rate, corner_frequency)

    with ThreadPoolExecutor(max_workers=nThreads) as executor:
        futures = [executor.submit(merge_and_record_time, folder) for folder in folder_list]
        with tqdm(total=total_tasks, desc="Processing folders") as pbar:
            for future in as_completed(futures):
                times.append(future.result())
                pbar.update(1)
    logging.info('Merge Done!')
    total_merge_time = sum(times)
    logging.info(f'Total merge time: {total_merge_time:.2f} seconds')
    return total_merge_time

for idx, path in enumerate(no_arrange_file_path_list):
    start_time_str = start_time_list[idx]
    end_time_str = end_time_list[idx]
    Date = os.path.basename(path)
    info = f'{Date} {start_time_str} to {end_time_str}'

    paths = initialize_directories(result_path, Date, suffix)
    gauge_length = Gauge_Length[idx]

    record_time('initialize_directories')
    process_time = process_traces_with_thread_pool(
        Total_Start_Traces_list, Total_End_Traces_list, path, start_time_str, end_time_str, paths["output"], info, gauge_length
    )
    time_records['process_traces'] = process_time

    record_time('process_traces')
    merge_time = merge_folders_with_thread_pool(os.listdir(paths["output"]), paths["output"], paths["temp"])
    time_records['merge_folders'] = merge_time

    for B in range(len(Start_trace_list[idx])):
        for i in range(len(Start_trace_list[idx][B])):
            start_trace = Start_trace_list[idx][B][i]
            end_trace = End_trace_list[idx][B][i]

            create_clean_directory(paths["merge"])
            Trace_list = sorted(os.listdir(paths["temp"]))
            for trace_folder in Trace_list:
                trace_num = int(trace_folder[4:8])
                if start_trace <= trace_num <= end_trace:
                    shutil.copytree(os.path.join(paths["temp"], trace_folder), os.path.join(paths["merge"], trace_folder))

            sample_sac_file = os.path.join(paths["merge"], f'NJU-{start_trace:04d}-STA', f'NJU-{start_trace:04d}-STA-merge.sac')
            sac = obspy.read(sample_sac_file)
            npts = sac[0].stats.npts
            sac.plot(outfile=os.path.join(paths["seismograms"], f'{info}NJU-{start_trace:04d}-STA.png'))

            namelist = sorted(os.listdir(paths["merge"]))
            nsta = len(namelist)
            data = np.zeros(npts * nsta, dtype=np.float32)
            startend = np.zeros(nsta * 2, dtype=np.int32)

            with ThreadPoolExecutor(max_workers=24) as pool:
                futures = [
                    pool.submit(read_data, i, paths["merge"], npts, data, startend, Fs, namelist)
                    for i in range(nsta)
                ]
                for future in as_completed(futures):
                    future.result()

            StationPairs = GetStationPairs(nsta)
            nPairs = int(len(StationPairs) / 2)
            ncfs = CC(npts, nsta, nf, fft_length, StationPairs, startend, data, 
                      fstride=fstride, overlaprate=overlap_rate, nThreads=nThreads, 
                      ifonebit=0, ifspecwhittenning=1)

            def ensure_directory_exists(file_path):
                directory = os.path.dirname(file_path)
                if not os.path.exists(directory):
                    os.makedirs(directory)

            # Save the cross-correlation function data to the specified path
            ccf_file_path = os.path.join(paths["ccf_file"], f'{info}NJU-{start_trace:04d}-to-NJU-{end_trace:04d}.npz')
            ensure_directory_exists(ccf_file_path)

            def save_ccf_data(ncfs, StationPairs, stalist, f, ccf_file_path):
                # Convert station pairs to names
                station_pairs_names = [
                    (stalist[StationPairs[i * 2]], stalist[StationPairs[i * 2 + 1]])
                    for i in range(len(StationPairs) // 2)
                ]
                np.savez(ccf_file_path, ncfs=ncfs, StationPairs=StationPairs, 
                         station_pairs_names=station_pairs_names, stalist=stalist, f=f)
                logging.info(f'Cross-correlation data saved: {ccf_file_path}')

            save_ccf_data(ncfs, StationPairs, namelist, f, ccf_file_path)

            outname = os.path.join(paths["output"], '0EGF.npz')
            ensure_directory_exists(outname)
            np.savez(outname, ncfs=ncfs, StationPairs=StationPairs, stalist=namelist, f=f)
            logging.info(f'{info} Cross-correlation for 0 completed. Output saved: {outname}')

            station_info_time = generate_station_info(start_trace, end_trace, gauge_length, paths["output_file"], info)
            time_records['generate_station_info'] = station_info_time

            # Load station information
            stalist = []
            lon = []
            lat = []
            station_info_path = os.path.join(paths["output_file"], 'stations_info.txt')
            with open(station_info_path, 'r') as f_file:
                for line in f_file:
                    parts = line.split()
                    stalist.append(parts[0])
                    lon.append(float(parts[1]))
                    lat.append(float(parts[2]))
            nsta = len(stalist)
            StationPairs = GetStationPairs(nsta)
            nPairs = int(nsta * (nsta - 1) / 2)
            ncfs = np.zeros((nPairs, nf), dtype=np.complex64)
            count = np.zeros(nPairs, dtype=np.int32)

            # Aggregate cross-correlation data
            for d in range(1):
                outname = os.path.join('output', f'{d}EGF.npz')
                if os.path.exists(outname):
                    data = np.load(outname)
                    nsta0 = len(data["stalist"])
                    id1 = []
                    id2 = []
                    for i in range(nPairs):
                        st1 = stalist[StationPairs[2 * i]]
                        st2 = stalist[StationPairs[2 * i + 1]]
                        i1 = np.where(data["stalist"] == st1)[0]
                        i2 = np.where(data["stalist"] == st2)[0]
                        if len(i1) > 0 and len(i2) > 0:
                            idx1 = min(i1[0], i2[0])
                            idx2 = max(i1[0], i2[0])
                            tmp = int(idx1 * (2 * nsta0 - idx1 - 1) / 2 + idx2 - idx1 - 1)
                            id1.append(i)
                            id2.append(tmp)
                    if id1 and id2:
                        ncfs[id1, :] += data["ncfs"][id2, :]
                        count[id1] += 1

            # Normalize cross-correlation functions
            ncfs1 = np.zeros_like(ncfs)
            valid = count > 0
            ncfs1[valid] = ncfs[valid] / count[valid, np.newaxis]

            # Calculate distances
            r = np.array([
                great_circle(
                    (lat[StationPairs[i * 2]], lon[StationPairs[i * 2]]),
                    (lat[StationPairs[i * 2 + 1]], lon[StationPairs[i * 2 + 1]])
                ).meters
                for i in range(len(ncfs))
            ])
            indx = np.argsort(r)
            r0 = r[indx]
            ncfs0 = ncfs1[indx, :]
            f = np.arange(0, nf) * Fs / fft_length * fstride
            summed_path = os.path.join(paths["output_file"], "summed.npz")
            np.savez(summed_path, ncfs=ncfs0, r=r0, f=f)
            logging.info(f'{info} Cross-correlation data summed and saved: {summed_path}')

            # Plot seismograms
            dt = 1 / np.max(f)
            t = (np.linspace(-len(f) / 2, len(f) / 2 - 1, len(f)) + 0.5) * dt
            ncfst = np.array([np.real(np.fft.fftshift(np.fft.ifft(ncfs0[i, :]))) for i in range(len(ncfs0))])
            fig, ax = plt.subplots(ncols=1, figsize=(7, 7))
            for i in range(len(r0)):
                ax.plot(t, np.real(ncfst[i, :]) / np.max(np.real(ncfst[i, :])) + r0[i], 'k', linewidth=0.2)
            ax.set_xlim([-1.0, 1.0])
            ax.set_ylim(bottom=0)
            seismo_plot_path = os.path.join(paths["seismograms"], f'{info}NJU-{start_trace:04d}-STA.png')
            plt.savefig(seismo_plot_path)
            plt.close()
            logging.info(f'{info} Cross-correlation plot saved: {seismo_plot_path}')

            # --------------------------------------------------------------------------------

            # Prepare to plot dispersion spectra
            logging.info(f'Starting to extract dispersion curves for {info} from {start_trace} to {end_trace}')
            data = np.load(summed_path)
            ncfs = data['ncfs']
            c = np.linspace(cmin, cmax, nc)
            r = data['r']
            f = data['f']

            disp_start_time = time.time()
            ds10 = ccfj.fj_noise(np.real(ncfs), r, c, f, fstride, itype=0, func=1)
            disp_end_time = time.time()
            time_records['extract_dispersion'] = disp_end_time - disp_start_time
            logging.info(f'Dispersion extraction completed in {disp_end_time - disp_start_time:.2f} seconds')

            # Plot dispersion curve
            fig, ax = plt.subplots(figsize=(3.5, 3.5))
            ax.pcolormesh(f, c, ds10, cmap='jet', vmin=0, vmax=1, shading='auto')
            ax.set_xlim([0, 50])
            ax.set_ylim([0, 1200])
            ax.tick_params(axis='x', labelsize=12)
            ax.tick_params(axis='y', labelsize=12)
            plt.tight_layout()
            dispersion_plot_path = os.path.join(paths["dispersion_curve"], f'{info}NJU-{start_trace:04d}-to-NJU-{end_trace:04d}.png')
            plt.savefig(dispersion_plot_path, dpi=500)
            plt.close()
            logging.info(f'{info} Dispersion curve plot saved: {dispersion_plot_path}')

            # -------------------------------------------------------------------------------------------------------

            # Save ds data to h5 file
            logging.info(f'ds10 shape: {ds10.shape}')
            logging.info(f'f shape: {f.shape}')
            logging.info(f'c shape: {c.shape}')

            h5file_path = os.path.join(paths["h5"], f'{info}NJU-{start_trace:04d}-ds10.h5')
            with h5py.File(h5file_path, 'w') as h5file:
                h5file.create_dataset('ds10', data=ds10)
                h5file.create_dataset('f', data=f)
                h5file.create_dataset('c', data=c)
            time_records['save_h5'] = time.time() - disp_end_time
            logging.info(f'{info} H5 file saved: {h5file_path}')

# Clean up temporary directories
for idx, path in enumerate(no_arrange_file_path_list):
    paths = initialize_directories(result_path, os.path.basename(path), suffix)
    shutil.rmtree(paths["output"])
    shutil.rmtree(paths["temp"])
    shutil.rmtree(paths["merge"])

# Copy the script to the result directory
script_path = os.path.realpath(__file__)
shutil.copy(script_path, os.path.join(result_path, os.path.basename(script_path)))

total_end_time = time.time()
logging.info(f'Total processing time: {total_end_time - total_start_time:.2f} seconds')

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours} hours, {minutes} minutes, {seconds:.2f} seconds"

formatted_time = format_time(total_end_time - total_start_time)
logging.info(f'Total processing time: {formatted_time}')
