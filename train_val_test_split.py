# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 23:28:23 2020

@author: jiayi
"""
import random
import numpy as np
import json
import os


#test_data_file = open('/home/jiayi/ObjectRecognition/test_data_paths.txt', "r")
#test_paths = test_data_file.readlines()
#set_1, set_2 = set(train_paths), set(test_paths)
#print(len(list(set_1 & set_2)))
#new_train_file = open('/home/jiayi/ObjectRecognition/train.txt', "w+")

#val_data_file = open('/home/jiayi/ObjectRecognition/val.txt', "w+")
#counter = 0
#for p in train_paths:
#    if counter < 400:
#        val_data_file.write(p)
#    else:
#        new_train_file.write(p)
#    counter +=1

#print(len(new_train_file.readlines()))
#print(len(val_data_file.readlines()))


#val_data_file = open('/home/jiayi/ObjectRecognition/val.txt', "a")





#val_data_file.close()
#train_data_file.close()
#test_data_file.close()
#new_train_file.close()

def get_class_name(class_key):
    if not class_key.split('_')[1].isdigit():
        class_name = class_key.split('_')[0] +"_" + class_key.split('_')[1]
    else:
        class_name = class_key.split('_')[0]
    return class_name

def remove_paths(class_dict, eliminate_paths):
    for c in class_dict:
        new_paths = list()
        for i in class_dict[c]:
            if i not in eliminate_paths:
                new_paths.append(i)
        for i in class_dict[c]:
            if i in eliminate_paths and len(new_paths) < 9:
                new_paths.append(i)
        if len(new_paths) > 20:
            del new_paths[20:]
        class_dict[c] = new_paths
        
    all_paths = list()
    all_values = class_dict.values()
    for p in all_values:
        all_paths += p
    return class_dict
    
def get_paths_statistic(class_dict, remove, eliminate_paths):
    new_dict = {}
    if remove:
        class_dict = remove_paths(class_dict, eliminate_paths)
    for c in class_dict:
        class_name = get_class_name(c)
        if class_name not in new_dict:
            new_dict[class_name] = []
        new_dict[class_name].append(len(class_dict[c]))
    
    all_size = []
    s = 0
    for i in new_dict:
        counts = new_dict[i]
        size = 0
        for c in counts:
            size += c
        new_dict[i] = size
        all_size.append(size)
        s += size
        
    return new_dict, class_dict, s, all_size
    

def get_unique_paths(class_path_dict):
    all_paths = list()
    all_values = class_path_dict.values()
    for p in all_values:
        all_paths += p
    unique_paths = list(dict.fromkeys(all_paths, {}))
    return unique_paths
    
    
def get_class_sizes(paths):
    all_classes = list()
    for f in paths:
        image_name = f.split('/')[-1].split('.')[0]
        json_path = f.split('/rgb')[0] + '/' + image_name + '.json'
        annotations = json.load(open(json_path))                
        for anno in annotations['annotations']:
            class_name = anno['id']
            if class_name is None:
                continue
            #class_name = class_name.split('_')[:-1]
            if not class_name.split('_')[1].isdigit():
                class_name = class_name.split('_')[0] +"_" + class_name.split('_')[1]
            else:
                class_name = class_name.split('_')[0]
            all_classes.append(class_name)
    size_dict = {i:all_classes.count(i) for i in all_classes}
    print(size_dict)
    print(len(size_dict))
    
    
class_dict = json.load(open('/home/jiayi/ObjectRecognition/data_statistic/class_path_dict.json'))
#print class_paths_dict
new_dict, class_dict, s, all_size = get_paths_statistic(class_dict, False, {})
print(new_dict)
print(len(new_dict), s)

#get unique paths from class_paths_dict
uniq_paths = get_unique_paths(class_dict)
print("unique paths: " + str(len(uniq_paths)))

eliminate_paths = list()
test_paths = list()

#pick paths from defined classes for elimination
classes = ['binder', 'kleenex', 'bell_pepper', 'hand_towel', 'cap', 'keyboard', 'food_box', 'notebook', 'cell_phone', 'flashlight', 'food_cup', 'pitcher','water_bottle']

for c in class_dict:
    class_name = get_class_name(c)
    #put all paths from classes, which has fewer paths, as test paths
    if class_name not in classes:
        test_paths += class_dict[c]
#get unique test paths
test_paths = list(dict.fromkeys(test_paths, {}))

#eliminate paths in defined classes from test set, eliminated paths should not be in test paths
for c in class_dict:
    class_name = get_class_name(c)
    if class_name in classes:
        for i in class_dict[c]:
            if i not in test_paths:
                eliminate_paths.append(i)
                
eliminate_paths = list(dict.fromkeys(eliminate_paths, {}))

class_dict = remove_paths(class_dict, eliminate_paths)
paths_dict = {}
for c in class_dict:
    if not c.split('_')[1].isdigit():
        class_name = c.split('_')[0] +"_" + c.split('_')[1]
    else:
        class_name = c.split('_')[0]

    if class_name not in paths_dict:
        paths_dict[class_name] = []
    for f in class_dict[c]:
        paths_dict[class_name].append(f)

for c in paths_dict:
    paths_dict[c] = list(dict.fromkeys(paths_dict[c], {}))

for c in paths_dict:
    c_file = open('/home/jiayi/ObjectRecognition/'+ c + '.txt', "w+")
    for p in paths_dict[c]:
        c_file.write(p + '\n')
    c_file.close()

#print("unique test paths: " + str(len(test_paths)))
#print("unique eliminate paths: " + str(len(eliminate_paths)))
#
#test_dict, final_dict, s, all_size = get_paths_statistic(class_dict, True, eliminate_paths)
#
#print(test_dict)
#print(len(test_dict), s)
#
#uniq_test_set = get_unique_paths(final_dict)
#print("test set size: " + str(len(uniq_test_set)))


#val_set = list()
#for i in uniq_paths:
#    if i not in uniq_test_set:
#        val_set.append(i)
#
#print("val set size: " + str(len(val_set)))


#ROOT_PATH = "/home/jiayi/aridDataset/arid_40k_scene_dataset"
#
#paths = list()
#for root,_,files in os.walk(ROOT_PATH):
#    for f in files:
#        if f.split('.')[-1] == 'png' and root.split('/')[-1] == 'rgb':
#          f = os.path.join(root, f)
#          paths.append(f)
#print(len(paths))
#
#train_paths = list()
#for p in paths:
#    if p not in uniq_paths:
#        train_paths.append(p)
#print("train set size: " + str(len(train_paths)))
#
#
#set_1, set_2 = set(train_paths), set(uniq_test_set)
#print("duplicate: " + str(len(list(set_1 & set_2))))


#with open('class_occlusion_count.json', 'w') as outfile:
#    json.dump(test_dict, outfile)
#
#test_data = open('/home/jiayi/ObjectRecognition/test.txt', "w+")
#for i in uniq_test_set:
#    test_data.write(i + '\n')
#test_data.close()
#
#val_data = open('/home/jiayi/ObjectRecognition/val.txt', "w+")
#for i in val_set:
#    val_data.write(i + '\n')
#val_data.close()
#
#train_data = open('/home/jiayi/ObjectRecognition/train.txt', "w+")
#for i in train_paths:
#    train_data.write(i + '\n')
#train_data.close()


#background_count = list()
#for p in uniq_test_set:
#    b = p.split('/')[-3].split('_')[-2]
#    background_count.append(b)   
#counter = {i:background_count.count(i) for i in background_count}
#print(counter)
#
#get_class_sizes(uniq_test_set)
#
#background_count = list()
#for p in val_set:
#    b = p.split('/')[-3].split('_')[-2]
#    background_count.append(b)   
#counter = {i:background_count.count(i) for i in background_count}
#print(counter)
#
#get_class_sizes(val_set)






