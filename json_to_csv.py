# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 00:43:22 2020

@author: jiayi
"""


import os
import glob
import pandas as pd
import json

def json_to_csv(paths):
    xml_list = []
    for p in paths:
        p = p.split('\n')[0]
        image_name = p.split('/')[-1].split('.')[0]
        json_path = p.split('/rgb')[0] + '/' + image_name + '.json'
        annotations = json.load(open(json_path))
        for anno in annotations['annotations']:
            if anno['id'] is None:
                continue
            if not anno['id'].split('_')[1].isdigit():
                classname = anno['id'].split('_')[0] +"_" + anno['id'].split('_')[1]
            else:
                classname = anno['id'].split('_')[0]
            value = (annotations['filename'],
                     640,
                     480,
                     classname,
                     int(anno['x']),
                     int(anno['y']),
                     int(anno['x'] + anno['width']),
                     int(anno['y'] + anno['height'])
                     )
            xml_list.append(value)
    
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df
    
    


def main(f):
    train_file = open(f, "r")
    train_paths = train_file.readlines()
    xml_df = json_to_csv(train_paths)
    file_name = f.split('/')[-1].split('.')[0]
    xml_df.to_csv('/home/jiayi/ssdDataset/' + file_name + '_labels.csv', index=None)
    print('Successfully converted xml to csv.')

for f in glob.glob("/home/jiayi/ObjectRecognition/background_*.txt"):
    main(f)