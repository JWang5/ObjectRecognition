# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 20:54:26 2020

@author: jiayi
"""
import json
import numpy as np
import matplotlib.pyplot as plt

file = open('/home/jiayi/ObjectRecognition/yolo/yolo_occluded_output_eval.txt', "r")
file2 = open('/home/jiayi/ObjectRecognition/yolo/yolo_evaluation.txt', "r")
file3 = open('/home/jiayi/ObjectRecognition/ssd/ssd_evaluation.txt', "r")
file4 =  open('/home/jiayi/ObjectRecognition/yolo/background_eval.txt', "r")
file5 = open('/home/jiayi/ObjectRecognition/ssd/ssd_occluded_eval.txt', "r")
file6 = open('/home/jiayi/ObjectRecognition/ssd/ssd_background_eval.txt', "r")

lines = file.readlines()
lines2 = file2.readlines()
lines3 = file3.readlines()
lines4 = file4.readlines()
lines5 = file5.readlines()
lines6 = file6.readlines()

bars = []
yolo_occluded = []
occluded_counter = []
yolo_general = []
ssd_general = []
ssd_occluded = []
yolo_background=[]
ssd_background = []
counter = [['instant_noodles', 39], ['food_bag', 28], ['toothpaste', 23], ['mushroom', 2], ['lightbulb', 22], ['orange', 17], ['food_cup', 16], ['water_bottle', 25], ['cap', 57], ['garlic', 17], ['binder', 36], ['glue_stick', 17], ['bowl', 39], ['cell_phone', 26], ['food_jar', 21], ['bell_pepper', 21], ['food_box', 24], ['toothbrush', 5], ['coffee_mug', 30], ['ball', 25], ['food_can', 25], ['banana', 25], ['pear', 15], ['comb', 20], ['scissors', 25], ['kleenex', 46], ['pliers', 22], ['keyboard', 22], ['lime', 5], ['marker', 24], ['cereal_box', 23], ['plate', 29], ['stapler', 22], ['rubber_eraser', 3], ['apple', 30], ['hand_towel', 48], ['soda_can', 24], ['lemon', 17], ['sponge', 21], ['potato', 4], ['tomato', 26], ['notebook', 32], ['peach', 24], ['dry_battery', 1], ['calculator', 35], ['camera', 24], ['pitcher', 36], ['shampoo', 22], ['flashlight', 19]]

#create list of class names
for l in lines:
    if '.txt' in l:
        class_name = l.split('/')[-1].split('.')[0]
        if class_name not in bars:
            bars.append(class_name)
print(len(bars))
print(bars)

#create occluded image counts for test data
for c in bars:
    for i in counter:
        if c in i:
            occluded_counter.append(int(i[1]))
print(len(occluded_counter))
print(occluded_counter)
            
#create list of class-ap for yolo in general            
for c in bars:
    for n in lines2:
        if c in n:
            yolo_general.append(float(n.split('%')[0].split('= ')[-1]))
print(len(yolo_general))
print(yolo_general)

#create class-ap from occluded image for yolo
for c in bars:
    percentage = list()
    label_ind = 0
    for l in lines:
        if c in l and '.txt' in l:
            label_ind = lines.index(l)
            for i in range(label_ind +1, label_ind + 80):
                if c in lines[i]:
                    yolo_occluded.append(float(lines[i].split('%')[0].split('= ')[-1]))
print('yolo_occluded: ' + str(len(yolo_occluded)))
print(yolo_occluded)

#createt list of class-ap for ssd in general
for l in lines3:
    if 'eval_util.py:87]' in l:
        for c in bars:
            if c in l:
                percentage = float(l.split(': ')[-1])*100
                ssd_general.append(percentage)
                
#create class-ap from occluded image for yolo
class_ind = []
for c in bars:
    ind = list()
    for l in lines5:
        if 'class: ' in l and c in l:
            ind.append(lines5.index(l))
    class_ind.append([ind[0], c])

print(class_ind)
            
for c in bars:
    #print(class_ind[bars.index(c)])
    label_ind = int(class_ind[bars.index(c)][0])
    if bars.index(c) + 1 >= 49:
        next_ind = len(lines5)
    else:
        next_ind = class_ind[bars.index(c) + 1][0]
    for i in range(label_ind +1, next_ind):
        if c in lines5[i] and 'estimator.py:2049]' in lines5[i]:
            print(c, lines5[i])
            value = float(lines5[i].split('PascalBoxes_PerformanceByCategory/AP@0.5IOU/' + c + ' = ')[1].split(',')[0]) * 100
            print(value)
            ssd_occluded.append(value)
print('ssd_occluded: ' + str(len(ssd_occluded)))
print(ssd_occluded)                


print(len(ssd_general))
print(ssd_general)
#bars.append('mAP')
#ssd_general.append(0.762480 * 100)
#yolo_general.append(87.16)

#plot for occlusion
ind = np.arange(len(bars))
width = 0.5

fig = plt.figure()
ax = fig.add_subplot(111)
rects1 = ax.bar(ind*1.75+width, yolo_occluded, width, color='#da680f')
ax2 = ax.twinx()
rects2 = ax2.bar(ind*1.75+width+width, ssd_occluded, width, color='#0492c2')

ax.set_xticks(ind*1.75 + (width/2))

ax.set_xticklabels(bars, rotation='80', fontsize=13)

ax.set_ylabel('AP in %', fontsize=15)
ax.set_yticks(np.arange(0, 110, step=10))
ax.set_yticklabels(np.arange(0, 110, step=10), fontsize=15)
ax2.set_ylabel('AP in %', fontsize=15)
ax2.set_yticks(np.arange(0, 110, step=10))
ax2.set_yticklabels(np.arange(0, 110, step=10), fontsize=15)

#ax.set_ylabel('Anzahl der vedeckten Bilder pro klasse', fontsize=13)
#ax.legend(rects1[0],'AP mit YOLO')
plt.title('Evaluation der Modelle mit verdeckten Objekten')
ax.legend( (rects1[0], rects2[0]), ('AP mit YOLO', 'AP mit SSD') , fontsize=13)
#ax.legend('Anzahl der Bilder pro Klasse')
plt.tight_layout()
#plt.show() 


#create background evaluation for yolo
for l in lines4:
    if '(mAP@0.50) = ' in l:
        value = float(l.split('(mAP@0.50) = ')[-1].split(',')[0]) *100
        yolo_background.append(value)
print(len(yolo_background))
print(yolo_background)

#create background evaluation for ssd
for l in lines6:
    if ' PascalBoxes_Precision/mAP@0.5IOU = ' in l:
        value = float(l.split(' PascalBoxes_Precision/mAP@0.5IOU = ')[1].split(',')[0]) *100
        if value not in ssd_background:
            ssd_background.append(value)
print(len(ssd_background))
print(ssd_background)



#Basic plot
#ind = np.arange(4)
#width = 0.45
#
#fig = plt.figure()
#ax = fig.add_subplot(111)
#rects1 = ax.bar(ind*1.5+width, yolo_background, width, color='#deb0b0')
#ax2 = ax.twinx()
#rects2 = ax2.bar(ind*1.5+width+width, ssd_background, width, color='#b0c4de')
#
#ax.set_xticks(ind*1.5+width+width)
#
#ax.set_xticklabels(['background_1', 'background_2', 'background_3', 'background_4'])
#
#ax.set_ylabel('AP in %')
#ax.set_yticks(np.arange(0, 110, step=10))
#ax2.set_ylabel('AP in %')
#
##ax2.set_ylabel('Anzahl der Bilder')
#
#ax.legend( (rects1[0], rects2[0]), ('AP mit YOLO', 'AP mit SSD') )
##ax.legend('Anzahl der Bilder pro Klasse')
#plt.tight_layout()
#plt.show()






#class_paths_dict = {}
#for c in file:
#    if not c.split('_')[1].isdigit():
#        class_name = c.split('_')[0] +"_" + c.split('_')[1]
#    else:
#        class_name = c.split('_')[0]
#
#    if class_name not in class_paths_dict:
#        class_paths_dict[class_name] = []
#    for f in file[c]:
#        class_paths_dict[class_name].append(f)
#
#for c in class_paths_dict:
#    class_paths_dict[c] = list(dict.fromkeys(class_paths_dict[c], {}))
#
#for c in class_paths_dict:
#    print(c, len(class_paths_dict[c]))