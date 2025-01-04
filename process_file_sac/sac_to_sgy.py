# -*- encoding: utf-8 -*-
'''
@File        :   sac_to_sgy.py
@Time        :   2025/01/03 22:44:17
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import segyio
import obspy
import os
import numpy as np

def sac_to_segy(sac_dir, output_sgy_file):
    sac_files = sorted([f for f in os.listdir(sac_dir) if f.endswith('.sac')])
    if not sac_files:
        print("No SAC files found")
        return

    first_sac = obspy.read(os.path.join(sac_dir, sac_files[0]))[0]
    n_traces = len(sac_files)
    n_samples = len(first_sac.data)
    sample_interval = int(first_sac.stats.delta * 1_000_000)  # microseconds

    spec = segyio.spec()
    spec.sorting = segyio.TraceSortingFormat.INLINE_SORTING  # inline sorting
    spec.format = 1  # floating-point format
    spec.samples = np.arange(n_samples)
    spec.ilines = np.arange(1, n_traces + 1)
    spec.xlines = np.arange(1, 2)  # only one xline
    spec.tracecount = n_traces

    with segyio.create(output_sgy_file, spec) as dst:
        for i, sac_file in enumerate(sac_files):
            trace_data = obspy.read(os.path.join(sac_dir, sac_file))[0].data
            dst.trace[i] = trace_data
            dst.header[i].update({
                segyio.TraceField.TRACE_SEQUENCE_LINE: i + 1,
                segyio.TraceField.FieldRecord: i + 1,
                segyio.TraceField.TraceNumber: i + 1,
                segyio.TraceField.TRACE_SAMPLE_INTERVAL: sample_interval,  # use the correct field name
            })

    print(f"Conversion completed: SAC files merged and converted to SEGY file {output_sgy_file}")

def process_sac_directory(sac_dir):
    output_sgy_file = os.path.join(sac_dir, "output_merged.sgy")
    sac_to_segy(sac_dir, output_sgy_file)

# Replace `sac_directory` with your SAC files directory
sac_directory = r"H:\github\personal-code-library\SAC_process\sac_sample"
process_sac_directory(sac_directory)
