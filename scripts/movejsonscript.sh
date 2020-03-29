#!/bin/bash
rootname="/home/jiayi/aridDataset/arid_40k_scene_dataset/Exp_10"
for f in $rootname/*; do
for j in $f/*labels.json; do
mv $j "/home/jiayi/BachelorThesis/jsons" 
done
done
