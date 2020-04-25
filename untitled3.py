# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 02:13:53 2020

@author: jiayi
"""

import shutil
destination = "/home/jiayi/ssdDataset/images"

train_file = open('test.txt', "r")
train_paths = train_file.readlines()

for p in train_paths:
    p = p.split('\n')[0]
    shutil.copy(p,destination)