# -*- encoding: utf-8 -*-
'''
@File        :   convert_sacs_from_a_sgy.py
@Time        :   2025/01/03 22:33:41
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import segyio
from obspy import Trace, UTCDateTime
import os
import sys

def segy_to_sac(sgy_file_path):
    # Determine the output directory name based on the SGY file name
    output_dir_basename = os.path.splitext(os.path.basename(sgy_file_path))[0] + "_sac"
    output_dir = os.path.join(os.path.dirname(sgy_file_path), output_dir_basename)
    os.makedirs(output_dir, exist_ok=True)

    with segyio.open(sgy_file_path, "r", ignore_geometry=True) as src:
        # Iterate over each trace in the SEG-Y file
        for index, trace in enumerate(src.trace):
            # Create an ObsPy Trace object
            tr = Trace(data=trace)
            tr.stats.starttime = UTCDateTime(0)  # Set a dummy start time
            tr.stats.sampling_rate = 1.0 / (src.bin[segyio.BinField.Interval] / 1e6)

            # Attempt to retrieve the coordinate scale factor from the trace header
            scale_factor = src.header[index][segyio.TraceField.SourceGroupScalar]
            if scale_factor < 0:
                scale = -1.0 / scale_factor
            elif scale_factor > 0:
                scale = scale_factor
            else:
                scale = 1.0

            # Apply the scale factor to GroupX to obtain the true coordinate value
            group_x = src.header[index][segyio.TraceField.GroupX]
            group_x_real = group_x * scale

            # Print relevant information for debugging
            print(f"Trace {index + 1}:")
            print(f"  Sampling rate: {tr.stats.sampling_rate} Hz")
            print(f"  Scale factor: {scale_factor}")
            print(f"  GroupX: {group_x}")
            print(f"  Real GroupX: {group_x_real}")

            # Set SAC header information, including the true GroupX coordinate
            tr.stats.sac = {}

            group_x_real = group_x_real / 1000  # Convert to kilometers
            tr.stats.sac['dist'] = group_x_real

            # Write to a SAC file
            sac_file_name = f"trace_{index + 1}.sac"
            sac_file_path = os.path.join(output_dir, sac_file_name)
            tr.write(sac_file_path, format='SAC')
        
        print(f"Conversion complete: {sgy_file_path} -> {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <sgy_file_path>")
        sys.exit(1)
    
    sgy_file_path = sys.argv[1]
    segy_to_sac(sgy_file_path)
