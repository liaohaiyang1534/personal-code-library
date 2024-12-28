#!/bin/bash

# Clear the OUTPUT directory
if [ -d "./OUTPUT" ]; then
    rm -rf ./OUTPUT/*
    echo "./OUTPUT directory has been cleared."
else
    mkdir "./OUTPUT"
    echo "./OUTPUT directory has been created."
fi

# Loop through a range of values and call the process_all_disp.sh script
# The sequence starts from 8.5, increments by 1, and ends at 52.5
for EEE in $(seq 8.5 1 52.5); do
    echo "Processing: ${EEE}"
    ./process_all_disp.sh "${EEE}"
done

echo "All processing is complete."
