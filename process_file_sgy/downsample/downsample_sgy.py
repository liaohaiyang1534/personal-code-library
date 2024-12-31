import segyio
import obspy
import sys

def downsample_stream(stream, target_sample_rate, original_sample_rate):
    """
    Downsample the stream to the target sample rate using decimation.
    """
    factor = int(original_sample_rate / target_sample_rate)  # Calculate the downsample factor
    return stream[::factor]  # Select every nth element as per the downsampling factor

def write_stream_to_segy_2d(stream, output_file_path, input_file_path):
    with segyio.open(input_file_path, 'r', ignore_geometry=True) as src:
        spec = segyio.spec()
        spec.sorting = 1
        spec.format = src.format
        spec.samples = src.samples
        spec.tracecount = len(stream)

        with segyio.create(output_file_path, spec) as dst:
            dst.text[0] = src.text[0]
            dst.bin.update(src.bin)

            for i, tr in enumerate(stream):
                dst.header[i] = src.header[i]
                dst.trace[i] = tr.data

def process_sgy_file_with_obspy(original_file_path, output_file_path, original_sample_rate, target_sample_rate):
    with segyio.open(original_file_path, "r", ignore_geometry=True) as src:
        data = segyio.tools.collect(src.trace[:])
        stream = obspy.Stream()
        
        for d in data:
            tr = obspy.Trace(d)
            tr.stats.delta = 1.0 / original_sample_rate  # Set the original sample rate manually
            stream.append(tr)

    # Downsample the stream to the required sample rate
    downsampled_stream = downsample_stream(stream, target_sample_rate, original_sample_rate)

    write_stream_to_segy_2d(downsampled_stream, output_file_path, original_file_path)
    print(f"Processed file saved as: {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python downsample_sgy.py <original_file_path> <output_file_path> <current_sample_rate> <target_sample_rate>")
        sys.exit(1)

    original_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    original_sample_rate = float(sys.argv[3])  # Current sample rate will be read as argument
    target_sample_rate = float(sys.argv[4])  # The desired sample rate will be read as argument
    
    print(f"Processing {original_file_path} to downsample to {target_sample_rate} Hz")
    process_sgy_file_with_obspy(original_file_path, output_file_path, original_sample_rate, target_sample_rate)