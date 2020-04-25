# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 22:57:56 2020

@author: jiayi
"""
import os
import glob
import PIL
import json

train_file = open('train.txt', "r")
train = train_file.readlines()
train_paths = list()
for p in train:
    p = p.split('\n')[0]
    train_paths.append(p)
    
ROOT_PATH = "/home/jiayi/aridDataset/arid_40k_scene_dataset"
 
EXP1_ROOT = ROOT_PATH + "/Exp_1"
EXP2_ROOT = ROOT_PATH + "/Exp_2"
EXP4_ROOT = ROOT_PATH + "/Exp_4"
EXP7_ROOT = ROOT_PATH + "/Exp_7"

def create_json(root, img_path):
    obj_id = img_path.split('/')[-2]
    filename =  img_path.split('/')[-1].split('.')[0]
    json_path = root.split('rgb')[0] + filename + ".json" 
    image = PIL.Image.open(img_path)
    width, height = image.size
    annotation = {
      "annotations": [
        {
          "class": "obj",
          "height": height,
          "id": obj_id,
          "type": "rect",
          "width": width,
          "x": 0,
          "y": 0
        }],   
        "class": "image",
        "filename": filename + ".png"}
    #print(annotation)
    with open(json_path, 'w') as outfile:
        json.dump(annotation, outfile)
    
    

def get_crops(source_path):
    crops_list = list()
    for root,_,files in os.walk(source_path):
        if root.split('/')[-1] == "crops":
            for f in glob.glob(root + "/*/*.png"):
                #if source_path is not EXP1_ROOT:
                    #create_json(root, f)
                crops_list.append(f)
    return crops_list
#
#crops = list()
#crops += get_crops(EXP1_ROOT)
#crops += get_crops(EXP2_ROOT)
#crops += get_crops(EXP7_ROOT)
#crops += get_crops(EXP4_ROOT)
#
#print(len(crops))


#file = open('augmented_train.txt', 'w+')
#for img in glob.glob("/home/jiayi/aridDataset/augmented/*.png"):
#    file.write(img + "\n")
#    
#file.close()

#file = open('crop_train.txt', 'w+')
#index_crop = 0
#while index_crop <= 1000:
#    file.write(crops[index_crop] + "\n")
#    index_crop += 1
#file.close()
flipped = []
for f in glob.glob('/home/jiayi/aridDataset/flip/*.png'):
    flipped.append(f)
    

import random
from scipy import ndarray
import skimage as sk
from skimage import img_as_ubyte
from skimage import transform
from skimage import util
#
def random_rotation(image_array: ndarray):
    # pick a random degree of rotation between 25% on the left and 25% on the right
    random_degree = random.uniform(-25, 25)
    return sk.transform.rotate(image_array, random_degree)

def random_noise(image_array: ndarray):
    # add random noise to the image
    return sk.util.random_noise(image_array)

def horizontal_flip(image_array: ndarray):
    # horizontal flip doesn't need skimage, it's easy as flipping the image array of pixels !
    return image_array[:, ::-1]
    
# dictionary of the transformations functions we defined earlier
available_transformations = {
    #'rotate': random_rotation,
    'noise': random_noise
    #'horizontal_flip': horizontal_flip
}

num_generated_files = 0

while num_generated_files <= 1000:
    # random image from the folder
    image_path = random.choice(flipped)
    #obj_id = image_path.split('/')[-2]
    # read image as an two dimensional array of pixels
    image_to_transform = sk.io.imread(image_path)
    # random num of transformations to apply
    num_transformations_to_apply = random.randint(1, len(available_transformations))
    
    num_transformations = 0
    transformed_image = None
    while num_transformations <= num_transformations_to_apply:
        # choose a random transformation to apply for a single image
        key = random.choice(list(available_transformations))
        transformed_image = available_transformations[key](image_to_transform)
        num_transformations += 1
    
    # define a name for our new file
    new_file_path = image_path
    sk.io.imsave(new_file_path,img_as_ubyte(transformed_image))

# write image to the disk
    #sk.io.imsave(new_file_path, transformed_image)
#    image = PIL.Image.open(new_file_path)
#    width, height = image.size
#    print(width, height)
#    annotation = {
#      "annotations": [
#        {
#          "class": "obj",
#          "height": height,
#          "id": obj_id,
#          "type": "rect",
#          "width": width,
#          "x": 0,
#          "y": 0
#        }],   
#        "class": "image",
#        "filename": image_path.split('/')[-1]}
#    
#    json_path = image_path.split('.')[0] + '.json'
#    with open(json_path, 'w') as outfile:
#        json.dump(annotation, outfile)

    num_generated_files += 1


















