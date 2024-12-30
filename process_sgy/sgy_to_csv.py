import segyio
import csv
import os

def segy_to_csv(sgy_file_path, csv_file_path):
    # Use segyio to read the SGY file
    with segyio.open(sgy_file_path, "r", ignore_geometry=True) as src:
        # Get the sample rate in microseconds
        sample_interval = src.bin[segyio.BinField.Interval]
        # Convert the sample rate to milliseconds
        sample_rate_ms = sample_interval / 1000.0

        # Collect all trace data using segyio tools
        data = segyio.tools.collect(src.trace[:])

        # Build the CSV file name with sample rate information
        base_name = os.path.basename(csv_file_path)
        name, ext = os.path.splitext(base_name)
        modified_csv_file_path = os.path.join(os.path.dirname(csv_file_path), f"{name}_sr{sample_rate_ms}ms{ext}")

        # Open a new CSV file to write the data
        with open(modified_csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

            # Transpose the trace data so each column represents a trace
            for i in range(len(data[0])):
                row = [trace[i] for trace in data]
                csvwriter.writerow(row)

    print(f"Trace data has been exported to {modified_csv_file_path}, sample rate is {sample_rate_ms} ms.")

# Use the function
sgy_file_path = r"H:\github\personal-code-library\SGY_process\2024-05-07-18-19-28.000_24.851_output.sgy"
csv_file_path = r"H:\github\personal-code-library\SGY_process\2024-05-07-18-19-28.000_24.851_output.csv"
segy_to_csv(sgy_file_path, csv_file_path)
