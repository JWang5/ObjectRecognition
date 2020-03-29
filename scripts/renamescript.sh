#!/bin/bash

rootname="/home/jiayi/aridDataset/arid_40k_scene_dataset/Exp_10"
for f in $rootname/*; do
result="${f%"${f##*[!/]}"}"
result="${result##*/}_"
printf '%s\n' "$result"
for i in $f/rgb/*.png; do
name="${i%"${i##*[!/]}"}"
name="${name##*/}"
printf '%s %s\n' "$name" "$i"
mv "$i" "$f/rgb/$result$name"
done 
done
