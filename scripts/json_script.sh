
#!/bin/bash

rootname="/home/jiayi/aridDataset/arid_40k_scene_dataset/Exp_10"
for f in $rootname/*; do
result="${f%"${f##*[!/]}"}"
result="${result##*/}_"
for j in $f/*.json; do
ex $f/*.json << EOEX 
:%s/img\//$result
:x
EOEX
sh split_json.sh $f ${result}labels.json; done; done
