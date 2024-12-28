#!/bin/sh

# Clean up
surf96 39

# Define damping
surf96 32 1.

# Select differential smoothing
surf96 36 1

# Set up repeated run for 5 iterations
surf96 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2

# Plot the model and show the data fit after 5 iterations
srfphv96
plotnps -EPS -K -F7 -W10 < SRFPHV96.PLT > figsrf1.eps

# Save the current model
surf96 28 modl.out

# Compare the individual models from the inversion to the true model
shwmod96 -K 1 -W 0.05 model.true
mv SHWMOD96.PLT T.PLT

shwmod96 -K -1 tmpmod96.???
mv SHWMOD96.PLT I.PLT

cat T.PLT I.PLT > IT.PLT
plotnps -EPS -K -F7 -W10 < IT.PLT > figsrf2.eps

convert figsrf1.eps -define png:color-type=2 figsrf1.png
convert figsrf2.eps -define png:color-type=2 figsrf2.png
