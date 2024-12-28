#!/bin/bash

# You should first adjust the model file modl.d and check if it meets the expectations.

# Line number
line_number=2
# Starting point of the line
start_dot=6
# Ending point of the line
end_dot=40
# Coordinates file
coordinates=./Line2_dot_xyz.txt

# Custom settings
total_layers=50     # Total number of layers
# Inversion depth (m)
inversion_depth=100
# Location of modl_out folder
modlout_location=./OUTPUT/modl_out

# Clear the OUTPUT directory
if [ -d "./OUTPUT" ]; then
    rm -rf ./OUTPUT/*
    echo "./OUTPUT directory has been cleared."
else
    mkdir "./OUTPUT"
    echo "./OUTPUT directory has been created."
fi

./process_modl.sh "${total_layers}" "${inversion_depth}"

cat modl.d

for EEE in $(seq $start_dot 1 $end_dot); do
    echo "Processing: ${EEE}"
    ./process_single.sh "${EEE}" "${line_number}" "${total_layers}"
done

echo "All processing tasks are completed."

./process_txts_2_onetxt.py $line_number $start_dot $end_dot $modlout_location $coordinates

echo "All processing tasks are completed."
