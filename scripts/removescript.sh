#!/bin/bash

rootname="/home/jiayi/aridDataset/arid_40k_scene_dataset/Exp_1"
for f in $rootname/*; do
for j in $f/rgb; do
#rm -r $f/depth
#rm -r $f/pcd
rm -fv $j/*.txt
done
done

