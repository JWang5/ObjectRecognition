#!/bin/bash
rootname="/home/jiayi/ObjectRecognition/arid_40k_scene_dataset/Exp_1"
for f in $rootname/*; do
for j in $f/*labels.json; do
mv $j "/home/jiayi/ObjectRecognition/jsons" 
done
done
