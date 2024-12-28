#!/bin/bash

# Check if parameters are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <total_layers> <inversion_depth>"
    exit 1
fi

# Get the parameters
total_layers="$1"
inversion_depth="$2"

# Calculate the thickness of a single layer, result divided by 1000
single_layer_thickness=$(echo "scale=6; ($inversion_depth / $total_layers) / 1000" | bc)

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
    
    # Generate rows based on total_layers
    for (( i=0; i<total_layers; i++ ))
    do
        echo "$single_layer_thickness 0.154025 0.1026830 2.8 0.0 0.0 0.0 0.0 1.0 1.0"
    done
    
    # Add the final line
    echo "0 0.154025 0.1026830 2.8 0.0 0.0 0.0 0.0 1.0 1.0"

} > modl.d
