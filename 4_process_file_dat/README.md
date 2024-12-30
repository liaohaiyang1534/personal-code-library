# Process File DAT: Convert DAT to SAC and SEGY Formats

This repository contains scripts to process `.dat` files, converting them into `SAC` and `SEGY` formats for seismic data analysis. The tools are designed to efficiently handle large datasets using multi-threaded or concurrent processing.

---

## Repository Structure

### Scripts

1. **`dat to sac.py`**  
   Converts `.dat` files into `SAC` format files.  
   - **Input**: `.dat` files containing seismic data with a fixed header structure.  
   - **Output**: Individual `SAC` files, one per channel, organized into subdirectories.  
   - **Key Features**:
     - Reads header and waveform data from `.dat` files.
     - Automatically calculates sampling rates and channel configurations.
     - Supports multi-threaded processing to utilize all available CPU cores.
   - **File Paths**:
     - Input Directory: `F:\diff_distance_to_cavity\noise_data\raw_data`
     - Output Directory: `F:\diff_distance_to_cavity\noise_data\processed_sac`

2. **`dat to sgy.py`**  
   Converts `.dat` files into `SEGY` format files.  
   - **Input**: `.dat` files containing seismic data.  
   - **Output**: `.sgy` files with header and trace data formatted according to SEGY standards.  
   - **Key Features**:
     - Utilizes `segyio` for SEGY file creation and trace handling.
     - Processes files concurrently using a thread pool for maximum efficiency.
     - Includes a progress bar (via `tqdm`) for tracking overall conversion progress.
   - **File Paths**:
     - Input Directory: `K:\diff_distance_cavity\1`
     - Output Directory: `K:\diff_distance_cavity\1_new`

---

## Workflow

### 1. Converting `.dat` to `SAC`
Run the `dat to sac.py` script to process all `.dat` files in the specified input directory. The script will:
1. Parse each `.dat` file to extract header information and waveform data.
2. Create a separate `SAC` file for each channel in the data.
3. Save the resulting `SAC` files in organized subdirectories.

**Usage**:  
Modify the `input_dir` and `output_dir` paths in the script as needed, then run:
```bash
python "dat to sac.py"
