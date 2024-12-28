#!/bin/bash

# Define an array of target directories
TARGET_DIRS=(
  # Add more directories here
  # "/mnt/h/termite/temple/test"
  # "/mnt/h/termite/school/active_source_1/test"
  # "/mnt/h/termite/school/active_source_1/shots_253_356_split_removebad_shottimematch_1s_right"
  # "/mnt/h/termite/school/active_source_1/shots_253_356_split_removebad_shottimematch_1s_left_reverse"

  # "/mnt/h/termite/school/active_source_1/shots_253_356_split_removebad_shottimematch_1s_ALL_picked"

  # "/mnt/h/termite/school/active_source_2/shots_510_610_split_removebad_shottimematch_ALL"

  # "/mnt/h/termite/school/active_source_2/test"

  # "/mnt/h/termite/dike/shots_218_257_split_removebad_shottimematch_ALL"

  # '/mnt/h/sym/truck/process/surface/line1_s/test_2/correlated_data_ref_trace_195_reversed_rs_rs_rs_rs_et_1.sgy'

  # "/mnt/h/diff_coupling/active_source/tumai/TEST_20241129/1-2_2024-05-02-15-20-04.693_output_right.sgy"

  # "/mnt/h/diff_coupling/active_source/tumai/TEST_20241129_1507"

  # "/mnt/h/diff_coupling/diff_hammer_compare/Heavy_hammer_plate_soil_buried_273_389_split_removebad"

  # "/mnt/h/diff_coupling/diff_hammer_compare/穿心锤-垫板-水泥_土埋_273_389_split_removebad"

  "/mnt/h/diff_coupling/diff_hammer_compare/穿心锤-不垫板-土_点胶_519_631_split_removebad"
  "/mnt/h/diff_coupling/diff_hammer_compare/穿心锤-不垫板-土_胶带_638_750_split_removebad"
  "/mnt/h/diff_coupling/diff_hammer_compare/穿心锤-不垫板-土_沙袋_755_868_split_removebad"
  "/mnt/h/diff_coupling/diff_hammer_compare/穿心锤-不垫板-土_石膏_392_509_split_removebad"
  "/mnt/h/diff_coupling/diff_hammer_compare/穿心锤-不垫板-土_土埋_273_389_split_removebad"
)

# Check the path to the single_sgy_FJ.sh script
ATTACK_SGY_SCRIPT="/mnt/h/code_copy/active_source_classification/6_single_sgy_FJs/single_sgy_FJ_attack.sh"
BATCH_RENAME_SCRIPT="/mnt/h/code_copy/active_source_classification/6_single_sgy_FJs/batch_rename_file.py"

total_files=0
processed_files=0

# Calculate the total number of .sgy files in all target directories
for TARGET_DIR in "${TARGET_DIRS[@]}"; do
  total_files_in_dir=$(find "$TARGET_DIR" -type f -name "*.sgy" | wc -l)
  total_files=$((total_files + total_files_in_dir))
done

echo "Total .sgy files to process: $total_files"

# Iterate over each target directory
for TARGET_DIR in "${TARGET_DIRS[@]}"; do
  echo "Processing directory: $TARGET_DIR"
  
  # Find and process all .sgy files in the target director
