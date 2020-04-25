# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 17:42:44 2020

@author: jiayi
"""
from scipy import ndarray
import skimage as sk
from skimage import img_as_ubyte
import json
import cv2
import numpy as np

    
def horizontal_flip(image_array: ndarray):
    # horizontal flip doesn't need skimage, it's easy as flipping the image array of pixels !
    return image_array[:, ::-1]
    
def extract_boxes(filename):
    boxes=list()
    annotations = json.load(open(filename))

    for anno in annotations['annotations']:
        xmin = int(anno['x'])
        xmax = int(anno['x'] + anno['width'])
        ymin = int(anno['y'])
        ymax = int(anno['y'] + anno['height'])
        coors = [xmin, ymin, xmax, ymax]
        boxes.append(coors)
        
    #width = 640
    #height = 480
    
    return boxes

train_file = open('train.txt', "r")
train = train_file.readlines()
train_paths = list()
flipped_train = open('flipped_train.txt', "w+")
num_generated_files = 0
for p in train:
    p = p.split('\n')[0]
    #train_paths.append(p)
    image_to_transform = sk.io.imread(p)
    transformed_image = horizontal_flip(image_to_transform)
    new_file_path = '%s/flipped_image_%s.png' % ("/home/jiayi/aridDataset/flipped", num_generated_files)
    new_json_path = '%s/flipped_image_%s.json' % ("/home/jiayi/aridDataset/flipped", num_generated_files)
    num_generated_files += 1
    sk.io.imsave(new_file_path,img_as_ubyte(transformed_image))
    flipped_train.write(new_file_path + '\n')
    image_name = p.split('/')[-1].split('.')[0]
    json_path = p.split('/rgb')[0] + '/' + image_name + '.json'
    annotations = json.load(open(json_path))
    boxes = list()
    flipped_annotations = {'annotations': [], 'class': 'image', 'filename': new_file_path.split('/')[-1]}
    for anno in annotations['annotations']:
        flipped_annotations['annotations'].append({'x': 640 - (anno['x'] + anno['width']), 'y': anno['y'], 'id': anno['id'], 'type':'rect', 'class': 'obj', 'height': anno['height'], 'width': anno['width']})
    
    with open(new_json_path, 'w') as outfile:
        json.dump(flipped_annotations, outfile)
        
flipped_train.close()

#boxes = extract_boxes("/home/jiayi/aridDataset/arid_40k_scene_dataset/Exp_1/wp_1_2_15/wp_1_2_15_019.json")

#image = cv2.imread(new_file_path) 
#image = np.array(image)
#
#for box in boxes:
#    print(box)
#    cv2.rectangle(image,(box[0], box[1]),(box[2], box[3]),(255, 0, 0), 2)
#            
#cv2.imshow('result', image)
#cv2.waitKey()