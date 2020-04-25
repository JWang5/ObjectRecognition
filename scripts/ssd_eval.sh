#!/bin/bash
#model_dir = '/content/drive/My\ Drive/ssd/models/research/training'

for f in /content/drive/My\ Drive/ssd/data/*.record; do
echo $f >> ssd_eval_occluded.txt
sed -i "s|^tf_record_input_reader .*$|tf_record_input_reader { input_path: \"${f}}\"|g" /content/drive/My\ Drive/ssd/models/research/object_detection/samples/configs/ssd_mobilenet_v2_coco.config
python3 /content/drive/My\ Drive/ssd/models/research/object_detection/legacy/eval.py --logtostderr --pipeline_config_path=/content/drive/My\ Drive/ssd/models/research/object_detection/samples/configs/ssd_mobilenet_v2_coco.config --checkpoint_dir=/content/drive/My\ Drive/backup --eval_dir=/content/drive/My\ Drive/ssd/models/research/training/eval_2 >> ssd_eval_occluded.txt
done



