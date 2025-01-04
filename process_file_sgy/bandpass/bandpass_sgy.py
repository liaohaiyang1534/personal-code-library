# -*- encoding: utf-8 -*-
'''
@File        :   bandpass_sgy.py
@Time        :   2025/01/03 22:44:44
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import segyio
import obspy
import sys

def bandpass_filter(stream, lowcut, highcut, fs, corners=3, zerophase=True):
    """
    Apply a bandpass filter to the stream.
    """
    return stream.filter('bandpass', freqmin=lowcut, freqmax=highcut, corners=corners, zerophase=zerophase)

def write_stream_to_segy_2d(stream, output_file_path, input_file_path):
    """
    Write filtered ObsPy stream data back to a new SEG-Y file,
    specifically tailored for 2D SEG-Y files.
    """
    with segyio.open(input_file_path, 'r', ignore_geometry=True) as src:
        spec = segyio.spec()
        spec.sorting = 1  # This is arbitrary for 2D but necessary for initialization
        spec.format = src.format
        spec.samples = src.samples
        spec.tracecount = len(stream)

        with segyio.create(output_file_path, spec) as dst:
            dst.text[0] = src.text[0]
            dst.bin.update(src.bin)

            for i, tr in enumerate(stream):
                dst.header[i] = src.header[i]
                dst.trace[i] = tr.data

def process_sgy_file_with_obspy(original_file_path, output_file_path, lowcut, highcut, fs):
    """
    Process SEG-Y file with ObsPy by applying a bandpass filter
    and writing the filtered data to a new SEG-Y file.
    """
    nyquist_freq = fs / 2.0
    if highcut > nyquist_freq:
        print(f"Warning: highcut frequency ({highcut} Hz) is above the Nyquist frequency ({nyquist_freq} Hz). Adjusting highcut to Nyquist frequency.")
        highcut = nyquist_freq
    
    with segyio.open(original_file_path, "r", ignore_geometry=True) as src:
        data = segyio.tools.collect(src.trace[:])
        stream = obspy.Stream()
        for d in data:
            tr = obspy.Trace(d)
            tr.stats.delta = 1.0 / fs
            stream.append(tr)
    
    stream_filtered = bandpass_filter(stream, lowcut, highcut, fs)

    write_stream_to_segy_2d(stream_filtered, output_file_path, original_file_path)

    print(f"Processed file saved as: {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python bandpass_sgy.py <original_file_path> <output_file_path> <lowcut> <highcut> <fs>")
        sys.exit(1)
    
    original_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    lowcut = float(sys.argv[3])
    highcut = float(sys.argv[4])
    fs = float(sys.argv[5])
    
    print(f"Processing {original_file_path} with lowcut={lowcut} Hz, highcut={highcut} Hz, and fs={fs} Hz")
    process_sgy_file_with_obspy(original_file_path, output_file_path, lowcut, highcut, fs)