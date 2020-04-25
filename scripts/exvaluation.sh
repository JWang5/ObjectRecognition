#!/bin/bash

for f in ObjectRecognition/evaluation_data/*.txt; do
echo $f >> output_eval.txt
sed -i "s|^val.*$|valid=${f}|g" arid.data
./darknet detector map arid.data cfg/yolov3.cfg backup/yolov3_start3.weights >> output_eval.txt
done

