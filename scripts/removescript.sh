#!/bin/bash

rootname="/home/jiayi/ObjectRecognition/arid_40k_scene_dataset/Exp_3"
for f in $rootname/*; do
#for j in $f; do
rm -r $f/depth
rm -r $f/pcd
done
#done

