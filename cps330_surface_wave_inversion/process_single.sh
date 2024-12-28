#!/bin/bash

script_to_run="./process_single_disp.sh"  # Script to run

files_to_move=("modl.out" "I.PLT" "T.PLT" "IT.PLT" "SRFPHV96.PLT" "disp.d" "modl.d" "figsrf1.eps" "figsrf2.eps" "figsrf1.png" "figsrf2.png")  # List of files to move

# Check if parameters are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <EEE> <line_number> <total_layers>"
    exit 1
fi

# Get the parameters
EEE="$1"
line_number="$2"
total_layers="$3"

start_layer=9       # Starting layer
end_layer=$((start_layer + total_layers))     # Ending layer

echo "Processing point $EEE on line $line_number"

# Ensure OUTPUT/modl_out directory exists
if [ ! -d "./OUTPUT/modl_out" ]; then
    mkdir -p "./OUTPUT/modl_out"
    echo "./OUTPUT/modl_out directory created."
fi

# Define DDD
DDD="${line_number}-${EEE}"

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
    read -ra ADDR <<< "$line"
    BBB=$(echo "scale=7; 1 / ${ADDR[0]}" | bc)
    CCC=$(echo "scale=7; ${ADDR[1]} / 1000" | bc)
    echo "SURF96 R C X 0 ${BBB} ${CCC} 0.01" >> "${DDD}_2.disp"
done < "./002Curve/${DDD}.disp"

echo "Processed data has been written to file ${DDD}_2.disp."

# Rename the file
mv "${DDD}_2.disp" "disp.d"
echo "File ${DDD}_2.disp renamed to disp.d."

# Ensure disp.d and modl.d exist
if [ ! -f "disp.d" ] || [ ! -f "modl.d" ]; then
    echo "disp.d or modl.d file does not exist."
    exit 1
fi

# Read the 7th column of disp.d to find the minimum and maximum values
min=$(awk '{print $7}' disp.d | sort -n | head -n1)
max=$(awk '{print $7}' disp.d | sort -n | tail -n1)

echo "Minimum value: $min"
echo "Maximum value: $max"

# Calculate increment
increment=$(echo "scale=7; ($max - $min) / $total_layers" | bc)

# Generate evenly spaced numbers
seq $min $increment $max > temp.txt
readarray -t M < temp.txt

echo "Generated evenly spaced numbers:"
printf "%s\n" "${M[@]}"

rm temp.txt

# Convert the M array into a space-separated string
M_values="${M[*]}"

# Update the modl.d file
awk -v mvals="$M_values" -v start=$start_layer -v end=$end_layer '
BEGIN {
    split(mvals, m_array, " ");
}
NR >= start && NR <= end {
    $2 = m_array[NR - start + 1] * 1.5;
    $3 = m_array[NR - start + 1];
    print;
    next;
}
{ print }
' modl.d > modl.d.tmp && mv modl.d.tmp modl.d

echo "modl.d updated."

# Run another script
$script_to_run
echo "$script_to_run script executed."

# Ensure OUTPUT/${DDD} directory exists
if [ ! -d "./OUTPUT/${DDD}" ]; then
    mkdir "./OUTPUT/${DDD}"
    echo "./OUTPUT/${DDD} directory created."
fi

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
