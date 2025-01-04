# -*- encoding: utf-8 -*-
'''
@File        :   plot_trace_in_sgy.py
@Time        :   2025/01/03 22:50:25
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


import os
import segyio
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams['font.family'] = 'SimHei'

def ensure_output_directory_exists(output_folder):
    """Ensure the output directory exists, if not, create it."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def generate_output_folder_and_title_prefix(filepath, trace_indices):
    """Automatically generate output folder and title prefix based on filepath and trace indices."""
    base_folder = os.path.dirname(filepath)
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_folder = os.path.join(base_folder, f"{base_name}_plots")
    trace_str = ",".join([str(index + 1) for index in trace_indices]) if isinstance(trace_indices, list) else str(trace_indices + 1)
    title_prefix = f"{base_name} - Traces {trace_str}"
    return output_folder, title_prefix

def plot_traces(filepath, trace_indices, save_fig=False, combine_traces=True, uniform_scale=False, mark_time=False, time_to_mark=150):
    """Plot one or more traces, with an option to combine or plot separately. Can also unify the scale of all plots and mark a specific time."""
    output_folder, title_prefix = generate_output_folder_and_title_prefix(filepath, trace_indices)
    with segyio.open(filepath, "r", ignore_geometry=True) as f:
        times = f.samples
        trace_indices = [trace_indices] if isinstance(trace_indices, int) else trace_indices

        min_value, max_value = 0, 0
        if uniform_scale:
            amplitude_ranges = [(np.min(f.trace[trace_index]), np.max(f.trace[trace_index])) for trace_index in trace_indices]
            min_amplitudes, max_amplitudes = zip(*amplitude_ranges)
            min_value, max_value = min(min_amplitudes), max(max_amplitudes)

        for trace_index in trace_indices:
            plt.figure(figsize=(12, 6))
            trace_data = f.trace[trace_index]
            plt.plot(times, trace_data, label=f"Trace {trace_index + 1}")
            plt.xlabel('Time (ms)')
            plt.ylabel('Amplitude')
            plt.legend()
            if uniform_scale:
                plt.ylim([min_value, max_value])
            if mark_time:
                plt.axvline(x=time_to_mark, color='red', linestyle='-', linewidth=2)
                plt.text(time_to_mark, max_value, f'{time_to_mark}ms', color='red', ha='right', va='bottom')
            trace_label = f"Trace {trace_index + 1}"
            plt.title(f"{title_prefix} - {trace_label}")
            plt.tight_layout()
            if save_fig:
                ensure_output_directory_exists(output_folder)
                filename = f"{title_prefix}_{trace_label}".replace(' ', '_').replace(':', '_').replace(',', '_') + ".png"
                plt.savefig(os.path.join(output_folder, filename))
            else:
                plt.show()
            plt.close()

# Example usage
filepath = r"H:\github\personal-code-library\SGY_process\2024-05-07-18-19-28.000_24.851_output.sgy"
trace_indices = [20]

plot_traces(filepath, trace_indices, save_fig=False, combine_traces=False, uniform_scale=True, mark_time=True, time_to_mark=630)
