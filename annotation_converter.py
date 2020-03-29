# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 22:48:14 2020

@author: jiayi
"""
import os
import json
from PIL import Image

ROOT_PATH = "/home/jiayi/aridDataset/arid_40k_scene_dataset"
DATA_ROOT_PATH = "/home/jiayi/aridDataset/arid_40k_scene_dataset/Exp_10"


def get_object_classes():  
    classes = []
    for root,_,files in os.walk(ROOT_PATH):
      if root.split('/')[-1] == 'crops':
        for o in os.listdir(root):
            if not o.split('_')[1].isdigit():
                class_name = o.split('_')[0] +"_" + o.split('_')[1]
            else:
                class_name = o.split('_')[0]
            if class_name not in classes:
                classes.append(class_name)
    return classes
    
#classes = get_object_classes()
    
classes = ['cap', 'soda_can', 'scissors', 'notebook', 'camera', 'marker', 'flashlight', 'greens', 'apple', 'pitcher', 'food_jar', 'keyboard', 'food_bag', 'comb', 'kleenex', 'bowl', 'toothbrush', 'bell_pepper', 'toothpaste', 'hand_towel', 'cereal_box', 'coffee_mug', 'pear', 'calculator', 'mushroom', 'peach', 'rubber_eraser', 'pliers', 'potato', 'cell_phone', 'food_box', 'garlic', 'stapler', 'shampoo', 'binder', 'tomato', 'ball', 'orange', 'lime', 'sponge', 'food_can', 'plate', 'lemon', 'lightbulb', 'glue_stick', 'onion', 'food_cup', 'banana', 'dry_battery', 'water_bottle', 'instant_noodles']
print(classes, len(classes))

def findClassId(class_name):
    class_id = classes.index(class_name)
    return class_id
    
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

#def converToYoloFormat(lines, image_path):
#    for line in lines:
#    #print('lenth of line is: ')
#    #print(len(line))
#    #print('\n')
#        elems = line.split(' ')
#        if(len(elems) >= 2):
#        #if(len(line) >= 2):
#            print(line + "\n")
#            elems = line.split(' ')
#            print(elems)
#            xmin = elems[0]
#            xmax = elems[2]
#            ymin = elems[1]
#            ymax = elems[3]
#            print(elems[0])
#            #
#            #t = magic.from_file(img_path)
#            #wh= re.search('(\d+) x (\d+)', t).groups()
#            im=Image.open(img_path)
#            w= int(im.size[0])
#            h= int(im.size[1])
#            #w = int(xmax) - int(xmin)
#            #h = int(ymax) - int(ymin)
#            # print(xmin)
#            print(w, h)
#            print(float(xmin), float(xmax), float(ymin), float(ymax))
#            b = (float(xmin), float(xmax), float(ymin), float(ymax))
#            bb = convert((w,h), b)
#            print(bb)
        
        
        
def main():
    for root,_,json_files in os.walk(DATA_ROOT_PATH):
        txt_root = root + "/rgb"
        for json_file in json_files:
            if json_file.split('.')[-1] == 'json':
                file_name = json_file.split('/')[-1].split('.')[0] 
                txt_name = file_name + ".txt"
                txt_path = os.path.join(txt_root, txt_name)
                
                json_path = os.path.join(root, json_file)
                annotations = json.load(open(json_path))
                file = open(txt_path, "w+")
                
                for anno in annotations['annotations']:
                    class_name = anno['id']
                    if class_name is None:
                        continue
                    #class_name = class_name.split('_')[:-1]
                    if not class_name.split('_')[1].isdigit():
                        class_name = class_name.split('_')[0] +"_" + class_name.split('_')[1]
                    else:
                        class_name = class_name.split('_')[0]
                    class_id = findClassId(class_name)
                    xmin = int(anno['x'])
                    xmax = int(anno['x'] + anno['width'])
                    ymin = int(anno['y'])
                    ymax = int(anno['y'] + anno['height'])
                    
                    image_path = txt_root + "/" + file_name + ".png"
                    im=Image.open(image_path)
                    w= int(im.size[0])
                    h= int(im.size[1])
                    b = (float(xmin), float(xmax), float(ymin), float(ymax))
                    bb = convert((w,h), b)
                    print(json_path, class_id, bb)
                    file.write(str(class_id) + " " + " ".join([str(a) for a in bb]) + '\n')
                
                file.close()

file = open("/home/jiayi/darknet/cfg/arid-obj.names", "w")        
for c in classes:
    file.write(c + "\n")

file.close()
            