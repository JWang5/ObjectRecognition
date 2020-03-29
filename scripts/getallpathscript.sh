#!/bin/bash

rootname="/home/jiayi/aridDataset/arid_40k_scene_dataset"
for f in $rootname/*; do
for j in $f/*; do
for img in $j/rgb/*.png; do
echo $img >> /home/jiayi/ObjectRecognition/training.txt

done
done
done
