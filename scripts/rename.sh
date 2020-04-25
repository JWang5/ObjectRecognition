#!/bin/bash

for f in ../evaluation_data/*.txt; do
sed -i 's/.\/aridDataset\/arid_40k_scene_dataset/\/home\/jiayi\/aridDataset\/arid_40k_scene_dataset/g' $f
done
