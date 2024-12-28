#!/bin/sh

# clean up
surf96 39

# define damping
surf96 32 1.

# select differential smoothing
surf96 36 1

# set up repeated run for 5 iterations
surf96 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2 6 1 2

# plot the model and show the data fit after 5 iterations
srfphv96
plotnps -EPS -K -F7 -W10 < SRFPHV96.PLT > figsrf1.eps

# save current model
surf96 28 modl.out

# compare the individual models from the inversion to the true model
shwmod96 -VMIN 0 -VMAX 1 -ZMIN 0 -ZMAX 0.015 -K 1 -W 0.05 model.true
mv SHWMOD96.PLT T.PLT

shwmod96 -VMIN 0 -VMAX 1 -ZMIN 0 -ZMAX 0.015 -K -1 tmpmod96.???
mv SHWMOD96.PLT I.PLT

cat T.PLT I.PLT > IT.PLT
plotnps -EPS -K -F7 -W10 < IT.PLT > figsrf2.eps

convert figsrf1.eps -background white -flatten -define png:color-type=2 figsrf1.png
convert figsrf2.eps -background white -flatten -define png:color-type=2 figsrf2.png






