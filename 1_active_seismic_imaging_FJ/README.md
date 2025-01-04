# Active Seismic Imaging using Frequency-Bessel Method

This repository contains scripts for active seismic imaging using Distributed Acoustic Sensing (DAS) and the CC-FJpy package (https://github.com/ColinLii/CC-FJpy).

## Experimental Setup

1. **Fiber-optic cables preparation**: Ensure fiber-optic cables are ready and perform tap tests.
2. **Active sources**: Use active sources (e.g., hammer or other sources) to create surface wave signals along the fiber-optic cable, with your own shot offsets.
3. **Record shot information**: Note the shot number and the time of each shot.
4. **Data conversion**: Convert `.dat` files to `.sgy` file format.
5. **Data processing**: Follow the data processing workflow to quickly process data from active source experiments.

## Data Processing Workflow

1. **Extract traces**: `1_extract_specific_traces`
2. **STA/LTA analysis**: Detect shot signals and their timings (`2_STALTA`).
3. **Match shot times**: Ensure shot numbers and signals match (`3_shot_time_match`).
4. **Split SEG-Y files**: Split the files based on the center shot trace (`4_shot_center`).
5. **Apply bandpass filters**: Filter the data (`5_bandpass`).
6. **Dispersion analysis**: Process single SEG-Y files for dispersion analysis (`6_single_sgy_FJs`).
7. **Pick dispersion curves**: Manually or automatically pick dispersion curves (`7_pick_curve`).

## Folder Structure

### `1_extract_specific_traces`
- **`batch_extract_specific_traces.py`**: Takes a folder as input, retrieves SEG-Y file information, and passes it to `extract_specific_traces.py`.
- **`extract_specific_traces.py`**: Extracts a range of traces from a single `.sgy` file.

### `2_STALTA`
- **`config.json`**: Configuration file for STA/LTA processing.
- **`main.py`**: Main script for STA/LTA processing.
- **`shot_time_match_module.py`**: Matches shot times to a reference timestamp.
- **`stalta_module.py`**: Detects trigger events using STA/LTA analysis.
- **`total_energy_module.py`**: Calculates total energy of seismic traces.
- **`utils.py`**: Utility functions (e.g., logging, SEG-Y file listing).

### `3_shot_time_match`
- **`batch_shot_time_match.py`**: Takes a folder as input, retrieves files information, and passes it to `shot_time_match.py`.
- **`shot_time_match.py`**: Matches shot times in a single SEG-Y file.

### `4_shot_center`
- **`batch_split_sgy.py`**: Takes a folder as input, retrieves SEG-Y file information, and passes it to `split_sgy.py`.
- **`split_sgy.py`**: Splits a single SEG-Y file based on a specified index (center shot trace).

### `5_bandpass`
- **`bandpass_sgy.py`**: Applies a bandpass filter to a single SEG-Y file.
- **`batch_bandpass_sgy.py`**: Takes a folder as input, retrieves SEG-Y file information, and passes it to `bandpass_sgy.py`.
- **`plot_sgy_frequency.py`**: Plots the frequency spectrum of SEG-Y files.

### `6_single_sgy_FJs`
- **`FJ_single_processing_sacs_to_pic.py`**: Processes SAC files for dispersion analysis using the CC-FJpy package ([ColinLii's work](https://github.com/ColinLii/CC-FJpy)).
- **`batch_grouping_file.py`**: Groups files into subfolders.
- **`batch_rename_file.py`**: Renames files in bulk.
- **`convert_sacs_from_a_sgy.py`**: Converts SEG-Y traces to SAC format.
- **`pick_diff_arraylength.py`**: Extracts traces with different lengths.
- **`pick_diff_offset_2.py`**: Removes traces based on offset.
- **`pick_diff_trace_spacing.py`**: Resamples traces for different trace spacing.
- **Shell Scripts**: Automates batch processing tasks (`single_batch_processing.sh`, etc.).

### `7_pick_curve`
- **`pick_dispersion_curves_active_imaging_FJ.py`**: GUI tool for manually picking dispersion curves from `.h5` files.
- **`batch_pick_dispersion_curves_active_imaging_FJ.py`**: Takes a folder as input, retrieves files information, and passes it to `pick_dispersion_curves_active_imaging_FJ.py`.
