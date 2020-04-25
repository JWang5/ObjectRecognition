# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 20:02:51 2020

@author: jiayi
"""
import matplotlib.pyplot as plt
import numpy as np

FILE_PATH = '/home/jiayi/ObjectRecognition/mrcnn/mrcnn_train_stat.txt'

file = open(FILE_PATH)

lines = file.readlines()

loss = list()
mrcnn_class_loss = list()
mrcnn_bbox_loss = list()
mrcnn_mask_loss = list()
val_loss = list()
val_mrcnn_class_loss = list()
val_mrcnn_bbox_loss = list()
val_mrcnn_mask_loss = list()

for l in lines:
    if '=======' in l:
        loss.append(float(l.split('- loss: ')[1].split(' - ')[0]))
        mrcnn_class_loss.append(float(l.split('mrcnn_class_loss: ')[1].split(' - mrcnn_bbox_loss:')[0]))
        mrcnn_bbox_loss.append(float(l.split('- mrcnn_bbox_loss: ')[1].split(' - mrcnn_mask_loss:')[0]))
        mrcnn_mask_loss.append(float(l.split(' - mrcnn_mask_loss: ')[1].split(' - val_loss: ')[0]))
        val_loss.append(float(l.split(' - val_loss: ')[1].split(' - val_rpn_class_loss: ')[0]))
        val_mrcnn_class_loss.append(float(l.split(' - val_mrcnn_class_loss: ')[1].split(' - val_mrcnn_bbox_loss: ')[0]))
        val_mrcnn_bbox_loss.append(float(l.split(' - val_mrcnn_bbox_loss: ')[1].split(' - val_mrcnn_mask_loss:')[0]))
        val_mrcnn_mask_loss.append(float(l.split(' - val_mrcnn_mask_loss: ')[1]))

#print(loss, mrcnn_class_loss)

x = range(1,21)
# plotting the line 1 points  
plt.plot(x, mrcnn_class_loss[:20], 'b', label = "loss") 
plt.plot(x, val_mrcnn_class_loss[:20], 'r', label = "val_loss") # plotting t, a separately 
# naming the x axis 
plt.xlabel('epoch') 
# naming the y axis 
plt.ylabel('loss value') 
# giving a title to my graph 
plt.title('loss tendency') 
  
# show a legend on the plot 
plt.legend() 
  
# function to show the plot 
plt.show() 
