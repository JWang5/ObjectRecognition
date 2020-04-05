# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 01:09:28 2020

@author: jiayi
"""
import os
import sys
import cv2
import glob
import json
import matplotlib.pyplot as plt
import numpy as np
from numpy import zeros
from numpy import asarray
from numpy import expand_dims
import colorsys
import argparse
#import imutils
import random
import cv2
import os
import time
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from keras.models import load_model
from os import listdir
import random


ROOT_DIR = os.path.abspath(".")

sys.path.append(ROOT_DIR)
sys.path.insert(0, '/home/jiayi/Mask_RCNN')
from mrcnn.config import Config
from mrcnn import visualize
from mrcnn.visualize import display_instances
from mrcnn.utils import extract_bboxes
from mrcnn.model import mold_image
from mrcnn.utils import compute_ap


import mrcnn
from mrcnn.utils import Dataset
from mrcnn.model import MaskRCNN
from mrcnn import model as modellib, utils

DATA_ROOT_PATH = "/content/Mask_RCNN/aridDataset/arid_40k_scene_dataset"
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

def get_object_classes():  
    classes = []
    for root,_,files in os.walk(DATA_ROOT_PATH):
      if root.split('/')[-1] == 'crops':
        for o in os.listdir(root):
          if o not in classes:
            classes.append(o)
    return classes
    
    
def get_paths():
    #image_paths =[]
    #json_paths = []
    paths = list()
    #path = os.path.join(DATA_ROOT_PATH, 'Exp_1')
    for root,_,files in os.walk(DATA_ROOT_PATH):
      random.shuffle(files)
      for f in files:
        if f.split('.')[-1] == 'png' and root.split('/')[-1] == 'rgb':
          f = os.path.join(root, f)
          #image_paths.append(f)
          image_id = f.split('/')[-1].split('.')[0]
          anno_path = os.path.join(root.split('rgb')[0], image_id) + '.json'
          path = {"image_path": f, "anno_path": anno_path}
          paths.append(path)
    random.shuffle(paths)
    return paths

def get_jsons():
    jsons = []
    for root,_,files in os.walk(DATA_ROOT_PATH):
        for f in files:
            if f.split('.')[-1] == 'json':
                f = os.path.join(root, f)
                jsons.append(f)
    return jsons
    
def find_image(image_list, image_id):
    for img in image_list:
        if img['id'] == image_id:
            return img

paths = get_paths()

class AridDataSet(utils.Dataset):
    def load_dataset(self, is_train=True):
        #index = 1
        #add all classes 
        classes = get_object_classes()
        for c in classes:   
            self.add_class("arid", classes.index(c), c)
            #index += 1
        #image_paths, json_paths = get_paths()
        #count = 0
        for i in range(0,len(paths)):
            #count += 1
            #index = path.index(path)
            if is_train and i >= len(paths)*0.8:
                continue
            if not is_train and i < len(paths)*0.8:
                continue
            #image_id = image.split('/')[-1].split('.')[0]
            ann_path = paths[i]["anno_path"]
            self.add_image('arid', image_id=i, path=paths[i]["image_path"], annotation=ann_path)
    
    def extract_boxes(self, filename):
        boxes=list()
        classes = list()
        annotations = json.load(open(filename))
        #annotations=list(annotations.values())
        #annotations = annotations[0]
        for anno in annotations['annotations']:
          if anno['id'] is None:
            continue
          xmin = int(anno['x'])
          xmax = int(anno['x'] + anno['width'])
          ymin = int(anno['y'])
          ymax = int(anno['y'] + anno['height'])
          coors = [xmin, ymin, xmax, ymax]
          boxes.append(coors)
          classes.append(anno['id'])
                    
        width = 640
        height = 480
        
        return boxes, width, height, classes
        
    def load_mask(self, index):
        info = self.image_info[index]        
        anno_path = info['annotation']
        boxes,w,h, classes = self.extract_boxes(anno_path)
        masks = zeros([h,w,len(boxes)], dtype='uint8')
        class_ids = list()  
        for i in range(len(boxes)):
            obj = classes[i]
            box = boxes[i]
            row_s, row_e = box[1], box[3]
            col_s, col_e = box[0], box[2]
            masks[row_s:row_e, col_s:col_e, i] = 1
            class_ids.append(self.class_names.index(obj))
        #info = self.image_info[1]
        return masks, asarray(class_ids, dtype='int32')
        
    def image_reference(self, index):
        info = self.image_info[index]        
        return info['path']
            


train_set = AridDataSet()    
train_set.load_dataset(is_train=True)
train_set.prepare()
print('Train: %d' % len(train_set.image_ids))

test_set = AridDataSet()
test_set.load_dataset(is_train=False)
test_set.prepare()
print('Test: %d' % len(test_set.image_ids))

class PredictionConfig(Config):
	# define the name of the configuration
	NAME = "arid_cfg"
	# number of classes (background + kangaroo)
	NUM_CLASSES = len(get_object_classes()) + 1
	# simplify GPU config
	GPU_COUNT = 1
	IMAGES_PER_GPU = 1
 
 
# plot a number of photos with ground truth and predictions
def plot_actual_vs_predicted(dataset, model, cfg, n_images=5):
	# load image and mask
	for i in range(n_images):
		# load the image and mask
		image = dataset.load_image(i)
		mask, _ = dataset.load_mask(i)
		# convert pixel values (e.g. center)
		scaled_image = mold_image(image, cfg)
		# convert image into one sample
		sample = expand_dims(scaled_image, 0)
		# make prediction
		yhat = model.detect(sample, verbose=0)[0]
		# define subplot
		pyplot.subplot(n_images, 2, i*2+1)
		# plot raw pixel data
		pyplot.imshow(image)
		pyplot.title('Actual')
		# plot masks
		for j in range(mask.shape[2]):
			pyplot.imshow(mask[:, :, j], cmap='gray', alpha=0.3)
		# get the context for drawing boxes
		pyplot.subplot(n_images, 2, i*2+2)
		# plot raw pixel data
		pyplot.imshow(image)
		pyplot.title('Predicted')
		ax = pyplot.gca()
		# plot each box
		for box in yhat['rois']:
			# get coordinates
			y1, x1, y2, x2 = box
			# calculate width and height of the box
			width, height = x2 - x1, y2 - y1
			# create the shape
			rect = Rectangle((x1, y1), width, height, fill=False, color='red')
			# draw the box
			ax.add_patch(rect)
	# show the figure
	pyplot.show()

# load the train dataset

# load the test dataset

# create config
cfg = PredictionConfig()

# define the model
model = MaskRCNN(mode='inference', model_dir='./', config=cfg)

model_path = '/home/jiayi/ObjectRecognition/mrcnn/mask_rcnn_arid_cfg_0040.h5'
model.load_weights(model_path, by_name=True, exclude=[ "mrcnn_class_logits", "mrcnn_bbox_fc", "mrcnn_bbox", "mrcnn_mask"])
# plot predictions for train dataset
# plot predictions for test dataset
plot_actual_vs_predicted(test_set, model, cfg)