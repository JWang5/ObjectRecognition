# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 02:13:18 2020

@author: jiayi
"""
import os
import glob
import json

ROOT_PATH = "/home/jiayi/aridDataset/arid_40k_scene_dataset"
OCCLUSION_PATH = "/home/jiayi/Downloads/occluded_images"
SMALL_PATH = "/home/jiayi/Downloads/arid_40k_small_crops"

def map_crop_to_image(source_path, p):
    folder_name = p.split('/')[6]
    img_index = int(p.split('/')[-1].split('_')[1]) + 1
    img_index = "{0:0=3d}".format(img_index)
    return source_path + '/' + folder_name +'/rgb/'+ folder_name +'_' + img_index + '.png'

def get_occluded_objects(source_path, all_occluded_img, condition_paths, class_paths_dict):
    #get all wp_*_*_* folder paths from source path
    root_paths = list()
    for root,_,files in os.walk(source_path):
        if root.split('/')[-1].split('_')[0] == 'wp':
            root_paths.append(root)
    root_paths.sort()
        
    #get class names
    classes = list()
    for root in root_paths:
        path = root + '/rgb/crops/'
        for o in os.listdir(path):
            class_name = o
            if class_name not in classes:
                classes.append(class_name)
    
    
    my_dict = {}  
    #get croped image paths for class c and append to class_paths_dict
    for c in classes:  
        class_paths = list()        
        for root in root_paths:
            root = root + '/rgb/crops/'
            for o in os.listdir(root):
                path = os.path.join(root, o)
                for file in glob.glob(path + "/*.png"):
                    if file.split('/')[-2] == c:
                        class_paths.append(file)
        #sort the class paths for class c to map the paths to occloded paths
        s = sorted(class_paths, key=lambda x:int(x.split('/')[-1].split('_')[-2]))
        s = sorted(s,key=lambda x:int(x.split('/')[-5].split('_')[-1]))
        s = sorted(s,key=lambda x:int(x.split('/')[-5].split('_')[-2]))
        my_dict[c] = s
                
    all_occluded_paths = list()
    for file in condition_paths:
        file_name = file.split('/')[-1]
        #check if the occluded image is in the source path
        if not file_name.split('_')[1].isdigit():
            if not int(file_name.split('_')[4]) == int(source_path.split('_')[-1]):
                continue
        else:
            if not int(file_name.split('_')[3]) == int(source_path.split('_')[-1]):
                continue
        #get the index of the occluded image in class_path_dict
        object_index = file_name.split('.')[0].split('_')[-1]
        #get class name from occluded image path
        if not file_name.split('_')[1].isdigit():
            class_name = file_name.split('_')[0] +"_" + file_name.split('_')[1]+ '_'+ file_name.split('_')[3]
        else:
            class_name = file_name.split('_')[0] + '_'+ file_name.split('_')[2]
        #get all image_path in dict for class
        object_paths = my_dict.get(class_name)
        if object_paths is None:
            continue
        #get image path in dict with index
        occluded_path = object_paths[int(object_index)]
        #append to a list with all wanted paths
        all_occluded_paths.append(occluded_path)
        #create a dict with class and its occluded paths
        if class_name not in class_paths_dict:
            class_paths_dict[class_name] = []
        class_paths_dict[class_name].append(map_crop_to_image(source_path, occluded_path))

    #get image path
    for p in all_occluded_paths:
        path = map_crop_to_image(source_path, p)
        all_occluded_img.append(path)    


#get classes with paths counts (not depending on occluded or not)
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
    class_dict = {i:all_classes.count(i) for i in all_classes}
    print(class_dict)
    print(len(class_dict))
    




class_paths_dict = {}
all_occluded_img = list()       
get_occluded_objects(ROOT_PATH + '/Exp_3', all_occluded_img, glob.glob(OCCLUSION_PATH + "/*.png"), class_paths_dict)
print("after Exp_3: " + str(len(all_occluded_img)))
get_occluded_objects(ROOT_PATH + '/Exp_5', all_occluded_img, glob.glob(OCCLUSION_PATH + "/*.png"),class_paths_dict)
print("after Exp_5: " + str(len(all_occluded_img)))

get_occluded_objects(ROOT_PATH + '/Exp_6', all_occluded_img, glob.glob(OCCLUSION_PATH + "/*.png"), class_paths_dict)
print("after Exp_6: " + str(len(all_occluded_img)))

get_occluded_objects(ROOT_PATH + '/Exp_8', all_occluded_img, glob.glob(OCCLUSION_PATH + "/*.png"), class_paths_dict)
print("after Exp_8: " + str(len(all_occluded_img)))

get_occluded_objects(ROOT_PATH + '/Exp_9', all_occluded_img, glob.glob(OCCLUSION_PATH + "/*.png"), class_paths_dict)
print("after Exp_9: " + str(len(all_occluded_img)))

unique_paths = list(dict.fromkeys(all_occluded_img))
print("all unique paths for small and occluded objects: " + str(len(unique_paths)))


#save class path dict as json
#with open('class_path_dict.json', 'w') as outfile:
#    json.dump(class_paths_dict, outfile)
#save the counts of each class
class_dict = json.load(open('/home/jiayi/ObjectRecognition/data_statistic/class_path_dict.json'))
new_dict = {}
for i in class_dict:
    if not i.split('_')[1].isdigit():
        class_name = i.split('_')[0] +"_" + i.split('_')[1]
    else:
        class_name = i.split('_')[0]
    if class_name not in new_dict:
        new_dict[class_name] = []
    new_dict[class_name].append(len(class_dict[i]))

for i in new_dict:
    counts = new_dict[i]
    size = 0
    for c in counts:
        size += c
    new_dict[i] = size
    
#with open('class_occlusion_count.json', 'w') as outfile:
#    json.dump(new_dict, outfile)


#background_count = list()
#for p in unique_paths:
#    b = p.split('/')[-3].split('_')[-2]
#    background_count.append(b)    

#counter = {i:background_count.count(i) for i in background_count}
#print(counter)
#get_class_sizes(unique_paths)

##get all small and occluded image paths
file = open('/home/jiayi/ObjectRecognition/small_occluded_paths', "r")
small_occluded = list()
f = file.readlines()
for l in f:
    small_occluded.append(l[:-1])
print(len(small_occluded))  

small_occluded_img = list()       
get_occluded_objects(ROOT_PATH + '/Exp_3', small_occluded_img, small_occluded, {})
print("after Exp_3: " + str(len(small_occluded_img)))
get_occluded_objects(ROOT_PATH + '/Exp_5', small_occluded_img, small_occluded, {})
print("after Exp_5: " + str(len(small_occluded_img)))

get_occluded_objects(ROOT_PATH + '/Exp_6', small_occluded_img, small_occluded, {})
print("after Exp_6: " + str(len(small_occluded_img)))

#get_occluded_objects(ROOT_PATH + '/Exp_7', all_occluded_img, glob.glob(OCCLUSION_PATH + "/*.png"))
#print("after Exp_7: " + str(len(all_occluded_img)))

get_occluded_objects(ROOT_PATH + '/Exp_8', small_occluded_img, small_occluded, {})
print("after Exp_8: " + str(len(small_occluded_img)))

get_occluded_objects(ROOT_PATH + '/Exp_9', small_occluded_img, small_occluded, {})
print("after Exp_9: " + str(len(small_occluded_img)))

unique_small_occluded_paths = list(dict.fromkeys(small_occluded_img, {}))
print("all unique paths for small and occluded objects: " + str(len(unique_small_occluded_paths)))

background_count = list()
for p in unique_small_occluded_paths:
    b = p.split('/')[-3].split('_')[-2]
    background_count.append(b)    

counter = {i:background_count.count(i) for i in background_count}
print(counter)
get_class_sizes(unique_small_occluded_paths)
#
#set_1, set_2 = set(unique_paths), set(unique_small_occluded_paths)
#print("duplicate: " + str(len(list(set_1 & set_2))))
#
#test_data = open('/home/jiayi/ObjectRecognition/test.txt', "w+")
#for i in unique_paths:
#    test_data.write(i + '\n')
#test_data.close()





