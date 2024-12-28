#!/bin/bash

# Check if a parameter is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <parameter>"
    exit 1
fi

# Get the parameter
param="$1"

# Ensure the modl_out directory exists
if [ ! -d "./OUTPUT/modl_out" ]; then
    mkdir -p "./OUTPUT/modl_out"
    echo "./OUTPUT/modl_out directory created."
fi

# Define DDD
DDD="1-${param}"

# Create the file
touch "${DDD}.disp"
echo "File ${DDD}.disp created."

# Check if the file exists
if [ ! -f "./002Curve/${DDD}.disp" ]; then
    echo "File ./002Curve/${DDD}.disp does not exist."
    exit 1
fi

# Read the file and process data
while IFS= read -r line; do
    # Read two values from each line
    read -ra ADDR <<< "$line"
    # Calculate BBB and CCC
    BBB=$(echo "scale=7; 1 / ${ADDR[0]}" | bc)
    CCC=$(echo "scale=7; ${ADDR[1]} / 1000" | bc)
    # Write the processed data to a new file
    echo "SURF96 R C X 0 ${BBB} ${CCC} 0.01" >> "${DDD}_2.disp"
done < "./002Curve/${DDD}.disp"

echo "Processed data written to file ${DDD}_2.disp."

# Rename the file
mv "${DDD}_2.disp" "disp.d"
echo "File ${DDD}_2.disp renamed to disp.d."

# Ensure disp.d and modl.d exist
if [ ! -f "disp.d" ] || [ ! -f "modl.d" ]; then
    echo "disp.d or modl.d file does not exist."
    exit 1
fi

# Read the 7th column of disp.d and find the minimum and maximum values
min=$(awk '{print $7}' disp.d | sort -n | head -n1)
max=$(awk '{print $7}' disp.d | sort -n | tail -n1)

echo "Minimum value: $min"
echo "Maximum value: $max"

# Calculate increment and generate 10, 20, or 30 layers
increment=$(echo "scale=7; ($max - $min) / 30" | bc)

# Generate evenly spaced numbers
seq $min $increment $max > temp.txt
readarray -t M < temp.txt

# Output the generated numbers
echo "Generated evenly spaced numbers:"
printf "%s\n" "${M[@]}"

rm temp.txt

# Convert M array into a space-separated string
M_values="${M[*]}"

# Update modl.d file, processing lines based on the number of layers (e.g., <=19 for 10 layers, <=29 for 20 layers, etc.)
awk -v mvals="$M_values" '
BEGIN {
    split(mvals, m_array, " ");
}
NR >= 9 && NR <= 39 {
    $2 = m_array[NR - 8] * 1.5;
    $3 = m_array[NR - 8];
    print;
    next;
}
{ print }
' modl.d > modl.d.tmp && mv modl.d.tmp modl.d

echo "modl.d updated."

# Run another script
./process_single_disp.sh
echo "process_single_disp.sh executed."

# Ensure OUTPUT/${DDD} directory exists
if [ ! -d "./OUTPUT/${DDD}" ]; then
    mkdir "./OUTPUT/${DDD}"
    echo "./OUTPUT/${DDD} directory created."
fi

# Define the list of files to move
files_to_move=("modl.out" "I.PLT" "T.PLT" "IT.PLT" "SRFPHV96.PLT" "disp.d" "modl.d" "figsrf1.eps" "figsrf2.eps")

# Move files to OUTPUT/${DDD}
for file in "${files_to_move[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" "./OUTPUT/${DDD}/"
        echo "$file copied to ./OUTPUT/${DDD}/"
    else
        echo "$file does not exist, cannot copy."
    fi
done

# Copy modl.out to modl_out directory and rename
if [ -f "modl.out" ]; then
    cp "modl.out" "./OUTPUT/modl_out/${DDD}.out"
    echo "modl.out copied and renamed to ./OUTPUT/modl_out/${DDD}.out"
else
    echo "modl.out does not exist, cannot copy."
fi

# Clear the OUTPUT directory
if [ -d "./OUTPUT" ]; then
    rm -rf ./OUTPUT/*
    echo "The ./OUTPUT directory has been cleared."
else
    mkdir "./OUTPUT"
    echo "The ./OUTPUT directory has been created."
fi

# Loop through a range of values and call the process_all_disp.sh script
# The sequence starts from 8.5, increments by 1, and ends at 52.5
for EEE in $(seq 8.5 1 52.5); do
    echo "Processing value: ${EEE}"
    ./process_all_disp.sh "${EEE}"
done

echo "All processing tasks are complete."
