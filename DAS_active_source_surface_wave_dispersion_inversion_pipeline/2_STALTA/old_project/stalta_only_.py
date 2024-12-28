import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import segyio
from obspy.signal.trigger import classic_sta_lta
from datetime import datetime

def process_sgy(file_path, output_folder, duration):
    print(f"Opening SEG-Y file: {file_path}")
    with segyio.open(file_path, "r", ignore_geometry=True) as f:
        sample_interval = f.bin[segyio.BinField.Interval] / 1_000_000  # 转换为秒
        num_samples = f.bin[segyio.BinField.Samples]
        trace_count = f.tracecount
        print(f"Sample interval: {sample_interval} seconds, Number of samples: {num_samples}, Trace count: {trace_count}")

        sta_lta_all = np.zeros((trace_count, num_samples), dtype=np.float32)  # 使用float32避免警告
        nsta = 1  # 短期平均窗口长度
        nlta = 1000  # 长期平均窗口长度

        for i in range(trace_count):
            trace = f.trace[i]
            sta_lta = classic_sta_lta(trace, nsta, nlta).astype(np.float32)  # 显式转换为float32
            sta_lta_all[i] = sta_lta

        sta_lta_mean = np.mean(sta_lta_all, axis=0)

    threshold = 10.0
    trigger_indices = np.where(sta_lta_mean > threshold)[0]
    print(f"Trigger indices: {trigger_indices}")

    trigger_times = trigger_indices / (1 / sample_interval)
    print(f"Trigger times: {trigger_times}")

    cleaned_trigger_times = []
    min_interval = 2.0

    prev_time = None
    for time in trigger_times:
        if prev_time is not None and time - prev_time < min_interval:
            continue
        cleaned_trigger_times.append(time)
        prev_time = time
    print(f"Cleaned trigger times: {cleaned_trigger_times}")

    time_axis = np.arange(len(sta_lta_mean)) * sample_interval * 1000

    plt.figure(figsize=(10, 6))
    plt.plot(time_axis, sta_lta_mean, color='red', label='STA/LTA Feature Mean')
    plt.axhline(y=threshold, color='green', linestyle='--', label='Threshold')
    plt.xlabel('Time (ms)')
    plt.ylabel('Feature')
    plt.title('STA/LTA Feature Mean')
    plt.legend()
    plt.grid(True)
    
    image_filename = os.path.splitext(os.path.basename(file_path))[0] + "_stalta.png"
    image_path = os.path.join(output_folder, image_filename)
    plt.savefig(image_path)
    plt.close()

    print(f"STA/LTA plot saved to {image_path}")

    if cleaned_trigger_times:
        print("Cleaned triggers found at corresponding times (in seconds):")
        for time in cleaned_trigger_times:
            print(f"Time: {time:.3f} seconds")
            try:
                copy_time_range(file_path, time, duration, prefix='_output', output_folder=output_folder)
            except Exception as e:
                print(f"Error processing trigger at time {time:.3f} seconds: {e}")
    else:
        print("No trigger found above the threshold.")

def copy_time_range(src_filename, start_time, duration=1.0, prefix='_output', output_folder=''):
    start_time -= 0.01
    if start_time < 0:
        start_time = 0

    print(f"Copying time range starting at {start_time} seconds for duration {duration} seconds from {src_filename}")

    try:
        with segyio.open(src_filename, "r", ignore_geometry=True) as src:
            sample_interval = src.bin[segyio.BinField.Interval] / 1_000_000
            num_samples = src.bin[segyio.BinField.Samples]
            recording_length = num_samples * sample_interval

            end_time = start_time + duration
            if end_time > recording_length:
                end_time = recording_length

            start_sample = int(start_time / sample_interval)
            end_sample = start_sample + int(duration / sample_interval)
            if end_sample > num_samples:
                end_sample = num_samples
            num_output_samples = end_sample - start_sample

            expected_samples = int(duration / sample_interval)
            output_data = np.zeros((src.tracecount, expected_samples), dtype=np.float32)  # 使用float32避免警告

            for i in range(src.tracecount):
                trace_data = src.trace[i][start_sample:end_sample]
                output_data[i, :len(trace_data)] = trace_data

            spec = segyio.tools.metadata(src)
            spec.samples = np.arange(0, expected_samples * sample_interval, sample_interval, dtype=np.float32)
            spec.tracecount = src.tracecount

            src_basename, src_extension = os.path.splitext(os.path.basename(src_filename))
            timestamp_str = src_basename.split('-out_')[0]
            print(f"Extracted timestamp from filename: {timestamp_str}")

            # 兼容没有微秒部分的时间戳
            try:
                file_time = datetime.strptime(timestamp_str, '%Y-%m-%d-%H-%M-%S.%f')
            except ValueError:
                file_time = datetime.strptime(timestamp_str, '%Y-%m-%d-%H-%M-%S')
            
            trigger_time_str = file_time.strftime('%Y-%m-%d-%H-%M-%S.%f')[:-3]

            dst_filename = f"{trigger_time_str}_{start_time:.3f}{prefix}{src_extension}"
            dst_filename = os.path.join(output_folder, dst_filename)

            print(f"Creating new SEG-Y file: {dst_filename}")

            with segyio.create(dst_filename, spec) as dst:
                dst.text[0] = src.text[0]
                dst.bin = src.bin
                dst.bin[segyio.BinField.Samples] = len(spec.samples)

                for i in range(src.tracecount):
                    dst.trace[i] = output_data[i]
                    dst.header[i] = src.header[i]
                    dst.header[i][segyio.TraceField.TRACE_SEQUENCE_LINE] = i + 1

            print(f"Copied all traces from {src_filename} to {dst_filename} within time range {start_time} to {end_time} seconds.")
            
            # 检查文件是否存在并且大小是否大于0
            if os.path.exists(dst_filename):
                print(f"File {dst_filename} created successfully with size {os.path.getsize(dst_filename)} bytes.")
            else:
                print(f"File {dst_filename} was not created.")
    except Exception as e:
        print(f"Error copying time range: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python stalta_only_.py <input_sgy_file_path> <output_folder_path> <duration>")
        sys.exit(1)
    
    input_sgy_file_path = sys.argv[1]
    output_folder_path = sys.argv[2]
    duration = float(sys.argv[3])

    process_sgy(input_sgy_file_path, output_folder_path, duration)
