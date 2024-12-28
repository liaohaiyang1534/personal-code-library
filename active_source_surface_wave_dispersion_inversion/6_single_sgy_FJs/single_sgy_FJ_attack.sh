#!/bin/bash

# SGY file path
sgy_file_path=$1

# Variables
min_offset=10
max_offset=10
current_min_offset=0
add_gap=5
min_length=30
max_length=30
step_length=5

spacing_now=0.5
desired_spacings="0.5"

PYTHON_EXEC="/home/lhy/miniconda3/bin/python"

# Base path and directory without extension
base_path="${sgy_file_path%.sgy}"
dir_path=$(dirname "$sgy_file_path")
file_base_name=$(basename "$sgy_file_path" .sgy)
file_path_without_ext="$dir_path/$file_base_name"

echo "SGY file path: $sgy_file_path"
echo "Base path without extension: $base_path"
echo "Directory path: $dir_path"
echo "File base name: $file_base_name"
echo "File path without extension: $file_path_without_ext"

# Check if SGY file exists
if [[ ! -f "$sgy_file_path" ]]; then
    echo "Error: SGY file does not exist: $sgy_file_path"
    exit 1
fi

# Confirm Python script location
PYTHON_SCRIPT_DIR="/mnt/h/code_copy/active_source_classification/6_single_sgy_FJs"

# Function to show progress bar
show_progress() {
    local current=$1
    local total=$2
    local bar_length=40
    local progress=$((current * bar_length / total))
    local remaining=$((bar_length - progress))
    printf "\r["
    for ((i=0; i<progress; i++)); do printf "#"; done
    for ((i=0; i<remaining; i++)); do printf "-"; done
    printf "] %d/%d" $current $total
}

echo "Processing Python script: pick_diff_trace_spacing"
$PYTHON_EXEC "$PYTHON_SCRIPT_DIR/pick_diff_trace_spacing.py" "$sgy_file_path" "$spacing_now" "$desired_spacings"

if [[ $? -ne 0 ]]; then
    echo "Error: Python script pick_diff_trace_spacing.py failed"
    exit 1
fi

echo "Processing in directory: $file_path_without_ext"

target_depth=1
file_count=$(find "$file_path_without_ext" -mindepth $target_depth -maxdepth $target_depth -type f -name "*.sgy" | wc -l)
current_file=0

echo 'Processing Python script: pick_diff_offset'
find "$file_path_without_ext" -mindepth $target_depth -maxdepth $target_depth -type f -name "*.sgy" | while read file_path; do
    file_name=$(basename "$file_path")
    if [[ $file_name =~ spacing_([0-9.]+)m_ ]]; then
        trace_spacing="${BASH_REMATCH[1]}"
        $PYTHON_EXEC "$PYTHON_SCRIPT_DIR/pick_diff_offset_2.py" "$file_path" "$trace_spacing" "$min_offset" "$max_offset" "$current_min_offset" "$add_gap" > /dev/null 2>&1
        current_file=$((current_file + 1))
        show_progress $current_file $file_count
    else
        echo "Could not extract trace spacing from file name: $file_name"
    fi
done
echo

target_depth=2
file_count=$(find "$file_path_without_ext" -mindepth $target_depth -maxdepth $target_depth -type f -name "*.sgy" | wc -l)
current_file=0

echo 'Processing Python script: pick_diff_array_length'
find "$file_path_without_ext" -mindepth $target_depth -maxdepth $target_depth -type f -name "*.sgy" | while read file_path; do
    file_name=$(basename "$file_path")
    if [[ $file_name =~ spacing_([0-9.]+)m_ ]]; then
        trace_spacing="${BASH_REMATCH[1]}"
        $PYTHON_EXEC "$PYTHON_SCRIPT_DIR/pick_diff_arraylength.py" "$file_path" "$trace_spacing" "$min_length" "$max_length" "$step_length" > /dev/null 2>&1
        current_file=$((current_file + 1))
        show_progress $current_file $file_count
    else
        echo "Could not extract trace spacing from file name: $file_name"
    fi
done
echo

target_depth=3
file_count=$(find "$file_path_without_ext" -mindepth $target_depth -maxdepth $target_depth -type f -name "*.sgy" | wc -l)
current_file=0

echo 'Processing Python script: convert_sacs_from_a_sgy'
find "$file_path_without_ext" -mindepth $target_depth -maxdepth $target_depth -type f -name "*.sgy" | while read file_path; do
    $PYTHON_EXEC "$PYTHON_SCRIPT_DIR/convert_sacs_from_a_sgy.py" "$file_path" > /dev/null 2>&1
    current_file=$((current_file + 1))
    show_progress $current_file $file_count
done
echo

file_count=$(find "$file_path_without_ext" -mindepth $target_depth -maxdepth $target_depth -type d -name "*_sac" | wc -l)
current_file=0

echo 'Processing Python script: FJ_single_sacs_to_pic'
find "$file_path_without_ext" -mindepth $target_depth -maxdepth $target_depth -type d -name "*_sac" | while read sac_dir_path; do
    $PYTHON_EXEC "$PYTHON_SCRIPT_DIR/FJ_single_processing_sacs_to_pic.py" "$sac_dir_path" > /dev/null 2>&1
    current_file=$((current_file + 1))
    show_progress $current_file $file_count
done
echo

echo 'Copying PNG files'
find "$file_path_without_ext" -mindepth $target_depth -maxdepth $target_depth -type f -name "*.png" | while read png_file_path; do
    cp "$png_file_path" "$dir_path"
done

echo 'Copying H5 files'
find "$file_path_without_ext" -mindepth $target_depth -maxdepth $target_depth -type f -name "*.h5" | while read h5_file_path; do
    cp "$h5_file_path" "$dir_path"
done

echo 'Removing intermediate files'
rm -rf "$file_path_without_ext"

echo "Processing complete"
