#!/bin/bash

# Check if a parameter is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <parameter>"
    exit 1
fi

# Get the parameter
param="$1"

# Define DDD
DDD="4-${param}"

# Create the file
touch "${DDD}.disp"
echo "File ${DDD}.disp has been created."

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

echo "Processed data has been written to the file ${DDD}_2.disp."
