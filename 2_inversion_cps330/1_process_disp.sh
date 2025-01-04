#!/bin/bash

# -*- encoding: utf-8 -*-
'''
@File        :   1_process_disp.sh
@Time        :   2025/01/03 22:38:11
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


# Check if an argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

# Get the input parameter
input_file="$1"

# Clear the disp.d file
> disp.d

# Read the file and process the data
awk '{ 
    BBB = 1 / $1; 
    CCC = $2; 
    printf("SURF96 R C X %d %.7f %.7f 0.01\n", $3, BBB, CCC); 
}' "$input_file" >> disp.d

# Uncomment the following lines if you want to print the processed data
# echo "Processed data has been written to disp.d."
# echo "Contents of disp.d:"
# cat disp.d
