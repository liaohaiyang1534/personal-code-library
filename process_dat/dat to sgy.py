import os
import numpy as np
import segyio
from concurrent.futures import ThreadPoolExecutor
import time
from tqdm import tqdm

# Define input directory list
input_paths = [
    r"K:\diff_distance_cavity\1",
]

output_folder_path = r"K:\diff_distance_cavity\1_new"

def process_file(input_path, dat):
    output_path = os.path.join(output_folder_path, os.path.basename(input_path) + '_sgy')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        dat_path = os.path.join(input_path, dat)
        with open(dat_path, 'rb') as f:
            A = np.fromfile(f, dtype=np.float32)
            C = A[:64]
            B = np.ascontiguousarray(A[64:])
            fs = C[10]

            N = int(C[16])
            length = int(fs * C[17])

            DD = B.reshape(int(length), N)
            D = np.ascontiguousarray(DD.T)

            save_path = os.path.join(output_path, dat[:-4] + '.sgy')

            spec = segyio.spec()
            spec.format = 1
            spec.tracecount = N
            spec.samples = np.arange(length) / (1 / fs * 1000 / 4)

            with segyio.create(save_path, spec) as sgy:
                for i in range(N):
                    sgy.trace[i] = D[i]
                    sgy.header[i].update({
                        segyio.TraceField.TraceNumber: i + 1,
                        segyio.TraceField.TRACE_SAMPLE_INTERVAL: int(1e6 / fs)
                    })
        return True
    except Exception as e:
        print(f"Error processing {dat}: {str(e)}")
        return False

def main():
    start_time = time.time()
    cpu_cores = os.cpu_count()
    max_workers = cpu_cores if cpu_cores else 4
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        progress = tqdm(total=sum(len(os.listdir(path)) for path in input_paths), desc="Total Progress", unit="file")

        for input_path in input_paths:
            dat_list = os.listdir(input_path)
            for dat in dat_list:
                future = executor.submit(process_file, input_path, dat)
                future.add_done_callback(lambda p: progress.update())
                futures.append(future)

        for future in futures:
            future.result()

        progress.close()

    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f}s")

if __name__ == '__main__':
    main()
