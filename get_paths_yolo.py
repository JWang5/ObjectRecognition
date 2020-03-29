# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 00:26:39 2020

@author: jiayi
"""
import os
import random

ROOT_PATH = "/home/jiayi/aridDataset/arid_40k_scene_dataset"

paths = list()

for root,_,files in os.walk(ROOT_PATH):
    for f in files:
        if f.split('.')[-1] == 'png' and root.split('/')[-1] == 'rgb':
          f = os.path.join(root, f)
          paths.append(f)
          
random.shuffle(paths)

def train_test_split(is_train, filename):
    file = open(filename, "w")
    for i in range(0,len(paths)):
        if is_train and i >= len(paths)*0.8:
            continue
        if not is_train and i < len(paths)*0.8:
            continue
        file.write(paths[i] + "\n")
    file.close()

train_test_split(True, "/home/jiayi/ObjectRecognition/train.txt")
train_test_split(False, "/home/jiayi/ObjectRecognition/test.txt")