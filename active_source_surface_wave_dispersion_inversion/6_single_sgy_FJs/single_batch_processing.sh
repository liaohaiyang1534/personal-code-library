#!/bin/bash

# Define an array of target directories
TARGET_DIRS=(
  # "/mnt/h/termite/temple/shots_263_393_split_removebad_shottimematch_right"
  # "/mnt/h/termite/temple/shots_263_393_split_removebad_shottimematch_left_reverse"
  # Add more directories here
  # "/mnt/h/termite/temple/test"
  # "/mnt/h/termite/school/active_source_1/test"
  # "/mnt/h/termite/school/active_source_1/shots_253_356_split_removebad_shottimematch_1s_right"
  # "/mnt/h/termite/school/active_source_1/shots_253_356_split_removebad_shottimematch_1s_left_reverse"
  # "/mnt/h/termite/school/active_source_1/shots_253_356_split_removebad_shottimematch_1s_ALL_picked"
  # "/mnt/h/termite/school/active_source_2/shots_510_610_split_removebad_shottimematch_ALL"
  # "/mnt/h/termite/school/active_source_2/test"
  # "/mnt/h/termite/dike/shots_218_257_split_removebad_shottimematch_ALL"
  "/mnt/h/termite/temple/shots_263_393_split_removebad_shottimematch_ALL"
)

# Define an array of minoff values
MINOFF_VALUES=(8 6 4)

# Check the path to the single_sgy_FJ.sh script
ATTACK_SGY_SCRIPT="/mnt/h/code_copy/active_source_classification/6_single_sgy_FJs/single_sgy_FJ.sh"
BATCH_RENAME_SCRIPT="/mnt/h/code_copy/active_source_classification/6_single_sgy_FJs/batch_rename_file.py"

# Iterate over the minoff array
for minoff in "${MINOFF_VALUES[@]}"; do
  array=$((2 * minoff))
  total_files=0
  processed_files=0

  # Calculate the total number of .sgy files in all target directories
  for TARGET_DIR in "${TARGET_DIRS[@]}"; do
    total_files_in_dir=$(find "$TARGET_DIR" -type f -name "*.sgy" | wc -l)
    total_files=$((total_files + total_files_in_dir))
  done

  echo "Total .sgy files to process with minoff=$minoff and array=$array: $total_files"

  # Process each target directory
  for TARGET_DIR in "${TARGET_DIRS[@]}"; do
    echo "Processing directory: $TARGET_DIR with minoff=$minoff and array=$array"
    
    # Find and process all .sgy files in the target directory and its subdirectories
    find "$TARGET_DIR" -type f -name "*.sgy" | while read filename; do
      # Call the single_sgy_FJ.sh script with the .sgy file as a parameter
      echo "Processing SGY file: $filename with minoff=$minoff and array=$array"
      $ATTACK_SGY_SCRIPT "$filename" "$minoff" "$array"
      
      # Update the count of processed files
      ((processed_files++))
      
      # Calculate and display the progress
      remaining_files=$((total_files - processed_files))
      echo "Processed: $processed_files / $total_files files, Remaining: $remaining_files files"
    done
    
    # Run the batch rename script and pass the target directory as a parameter
    echo "Running batch rename script for directory: $TARGET_DIR"
    python3 "$BATCH_RENAME_SCRIPT" "$TARGET_DIR"
    
    # Create a new folder with the _dispersion_${minoff}_${array} suffix
    new_folder="${TARGET_DIR}_dispersion_${minoff}_${array}"
    
    # Create the new folder
    mkdir -p "$new_folder"
    
    # Move .h5 and .png files into the new folder
    find "$TARGET_DIR" -type f \( -name "*.h5" -o -name "*.png" \) -exec mv {} "$new_folder" \;
    
    echo "Moved .h5 and .png files to: $new_folder"
  done
done
