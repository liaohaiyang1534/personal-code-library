#!/bin/bash

# -*- encoding: utf-8 -*-
'''
@File        :   2_process_modl.sh
@Time        :   2025/01/03 22:38:17
@Author      :   Haiyang Liao
@Affiliation :   Nanjing University (NJU)
@Contact     :   haiyangliao@smail.nju.edu.cn
'''


# The initial model is important and can be manually set here. Currently, there are 5 ways to set the initial model:
# 1. Uniform model where all layers have the same velocity.
# 2. Velocity gradient model with user-defined min and max velocity.
# 3. Velocity gradient model with min and max velocity automatically extracted from the dispersion curve.
# 4. Custom model defined layer by layer in the code.
# 5. Custom model by manually editing the model file and placing it in the ../modl directory; it will be automatically copied during runtime.

# Check if an argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

# Get the input parameter
input_file="$1"

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "The input file does not exist. Please provide a valid txt file."
    exit 1
fi

# Set the model type
model_type="3"

if [ "$model_type" -eq 1 ]; then
    # Uniform model
    layer_thickness=0.005 # Layer thickness (km)
    inversion_depth=0.1   # Inversion depth (km)
    total_layers=$(echo "scale=0; $inversion_depth / $layer_thickness" | bc) # Calculate total layers
    single_layer_thickness=$layer_thickness

    # Create the model file modl.d
    {
        echo "MODEL"
        echo "TEST MODEL"
        echo "ISOTROPIC"
        echo "KGS"
        echo "FLAT EARTH"
        echo "1-D"
        echo "CONSTANT VELOCITY"
        echo "HR VP VS RHO QP QS ETAP ETAS FREFP FREFS"
        
        for (( i=0; i<total_layers; i++ )); do
            echo "$single_layer_thickness 0.1540 0.1027 28.0000 0.0000 0.0000 0.0000 0.0000 1.0000 1.0000"
        done
        
        echo "0 $single_layer_thickness 0.1540 0.1027 28.0000 0.0000 0.0000 0.0000 0.0000 1.0000 1.0000"
    } > modl.d

elif [ "$model_type" -eq 2 ]; then
    # Velocity gradient model with user-defined min and max velocity
    layer_thickness=0.005
    inversion_depth=0.1
    total_layers=$(echo "scale=0; $inversion_depth / $layer_thickness" | bc)

    initial_velocity=1.0
    final_velocity=2.5
    single_layer_thickness=$layer_thickness
    velocity_increment=$(echo "scale=6; ($final_velocity - $initial_velocity) / ($total_layers - 1)" | bc)
    vp_vs_ratio=1.7321

    {
        echo "MODEL"
        echo "TEST MODEL"
        echo "ISOTROPIC"
        echo "KGS"
        echo "FLAT EARTH"
        echo "1-D"
        echo "CONSTANT VELOCITY"
        echo "HR VP VS RHO QP QS ETAP ETAS FREFP FREFS"
        
        for (( i=0; i<total_layers; i++ )); do
            current_vs=$(echo "scale=6; $initial_velocity + $i * $velocity_increment" | bc)
            current_vp=$(awk -v vs=$current_vs -v ratio=$vp_vs_ratio 'BEGIN {print vs * ratio}')
            density=$(awk -v vp=$current_vp 'BEGIN {print 1.741 * (vp ^ 0.25)}')
            echo "$(printf "%.4f" $single_layer_thickness) $(printf "%.4f" $current_vp) $(printf "%.4f" $current_vs) $(printf "%.4f" $density) 0.0000 0.0000 0.0000 0.0000 1.0000 1.0000"
        done
        
        final_vs=$final_velocity
        final_vp=$(awk -v vs=$final_vs -v ratio=$vp_vs_ratio 'BEGIN {print vs * ratio}')
        final_density=$(awk -v vp=$final_vp 'BEGIN {print 1.741 * (vp ^ 0.25)}')
        echo "0.0000 $(printf "%.4f" $final_vp) $(printf "%.4f" $final_vs) $(printf "%.4f" $final_density) 0.0000 0.0000 0.0000 0.0000 1.0000 1.0000"
    } > modl.d

elif [ "$model_type" -eq 3 ]; then
    # Velocity gradient model with auto-extracted min and max velocity
    layer_thickness=0.001
    inversion_depth=0.015
    total_layers=$(echo "scale=0; $inversion_depth / $layer_thickness" | bc)

    initial_velocity=$(awk 'NR == 1 || $2 < min {min = $2} END {print min}' "$input_file")
    final_velocity=$(awk 'NR == 1 || $2 > max {max = $2} END {print max}' "$input_file")
    single_layer_thickness=$layer_thickness
    velocity_increment=$(echo "scale=6; ($final_velocity - $initial_velocity) / ($total_layers - 1)" | bc)
    vp_vs_ratio=1.7321

    {
        echo "MODEL"
        echo "TEST MODEL"
        echo "ISOTROPIC"
        echo "KGS"
        echo "FLAT EARTH"
        echo "1-D"
        echo "CONSTANT VELOCITY"
        echo "HR VP VS RHO QP QS ETAP ETAS FREFP FREFS"
        
        for (( i=0; i<total_layers; i++ )); do
            current_vs=$(echo "scale=6; $initial_velocity + $i * $velocity_increment" | bc)
            current_vp=$(awk -v vs=$current_vs -v ratio=$vp_vs_ratio 'BEGIN {print vs * ratio}')
            density=$(awk -v vp=$current_vp 'BEGIN {print 1.741 * (vp ^ 0.25)}')
            echo "$(printf "%.4f" $single_layer_thickness) $(printf "%.4f" $current_vp) $(printf "%.4f" $current_vs) $(printf "%.4f" $density) 0.0000 0.0000 0.0000 0.0000 1.0000 1.0000"
        done
        
        final_vs=$final_velocity
        final_vp=$(awk -v vs=$final_vs -v ratio=$vp_vs_ratio 'BEGIN {print vs * ratio}')
        final_density=$(awk -v vp=$final_vp 'BEGIN {print 1.741 * (vp ^ 0.25)}')
        echo "0.0000 $(printf "%.4f" $final_vp) $(printf "%.4f" $final_vs) $(printf "%.4f" $final_density) 0.0000 0.0000 0.0000 0.0000 1.0000 1.0000"
    } > modl.d

elif [ "$model_type" -eq 4 ]; then
    # Custom model defined layer by layer in the code
    echo "Custom model requires manual configuration in the code."
    exit 1

elif [ "$model_type" -eq 5 ]; then
    # Copy custom model file
    cp ../modl/mymodl.d modl.d
else
    echo "Invalid model type. Please choose 1, 2, 3, 4, or 5."
    exit 1
fi

echo "Contents of modl.d:"
cat modl.d
