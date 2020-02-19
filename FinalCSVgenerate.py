# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:14:13 2020

@author: gs52078
"""


import pandas as pd
import skimage.io as io
import matplotlib.pyplot as plt
import cv2
import gc
import numpy as np
import skimage
import skimage.feature as feature
import glob
import os
from skimage.color import rgb2gray
from PIL import Image, ImageChops

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def extract_bboxes(mask):
    """Compute bounding boxes from masks.
    mask: [height, width, num_instances]. Mask pixels are either 1 or 0.

    Returns: bbox array [num_instances, (y1, x1, y2, x2)].
    """
    boxes = np.zeros([mask.shape[-1], 4], dtype=np.int32)
    for i in range(mask.shape[-1]):
        m = mask[:, :, i]
        # Bounding box.
        horizontal_indicies = np.where(np.any(m, axis=0))[0]
        vertical_indicies = np.where(np.any(m, axis=1))[0]
        if horizontal_indicies.shape[0]:
            x1, x2 = horizontal_indicies[[0, -1]]
            y1, y2 = vertical_indicies[[0, -1]]
            # x2 and y2 should not be part of the box. Increment by 1.
            x2 += 1
            y2 += 1
        else:
            # No mask for this instance. Might happen due to
            # resizing or cropping. Set bbox to zeros
            x1, x2, y1, y2 = 0, 0, 0, 0
        #for keras tensorflow
        #boxes[i] = np.array([y1, x1, y2, x2]) 
        #for pytorch
        boxes[i] = np.array([x1, y1, x2, y2])
    return boxes.astype(np.int32)

def functionfinal():
    path = 'D:/Harish/code/DTS/dts_data'
    out = 'D:/Harish/code/DTS/new_classification/'
    ignore = []
    complete = []
    image_info = {}
    filename = []
    labels = []
    ignore_ = []
    for a in annotations:
        polygons = [r['shape_attributes'] for r in a['regions'].values()]
        values = [r['region_attributes'] for r in a['regions'].values() if r['region_attributes']]
        if len(values)>0:
            if 'class' in values[0].keys():
                classes = [r['class'].strip().lower() for r in values if r['class'].strip().lower()!='']
            elif 'Class' in values[0].keys():
                classes = [r['Class'].strip().lower() for r in values if r['Class'].strip().lower()!='']
            #elif 'color' in values[0].keys():
            #    continue
        for com_ in com[1:]:
            classes = [r.replace(com_.lower(),'') for r in classes]
        classes = [r.replace('_','') for r in classes]
        classes = [r.replace(' ','') for r in classes]
        classes = [r.replace(',','') for r in classes]
        classes = [r.replace(';','') for r in classes]
        classes = [r.replace('poor','') for r in classes]
        classes = [r.replace('obstructedbybox','') for r in classes]
        #classes = ['streetname' for r in classes if 'streetname' in r]
        #classes = ['trafficlight' for r in classes if 'trafficlight' in r]
        if a['filename'] in ignore:
            continue
        image_path = os.path.join(path, a['filename'])
        if not os.path.exists(image_path):
            print('here')
            ignore.append(a['filename'])
            print(a['filename'])
            continue
            
        image = skimage.io.imread(image_path)
        height, width = image.shape[:2]
        #print(a['filename'])
        if len(polygons) != len(classes):
            print(a['filename'])
            continue
        for p in range(0,len(polygons)):
            if polygons[p]['name'] == 'polygon':
                po = polygons[p]
                mask = np.zeros([height, width, 1],dtype=np.uint8)
                rr, cc = skimage.draw.polygon(po['all_points_y'], po['all_points_x'])
                mask[rr, cc, 0] = 1
                x1,y1,x2,y2 = extract_bboxes(mask)[0]
                
            if polygons[p]['name'] == 'rect':
                po = polygons[p]
                x1,y1,x2,y2 = po['x'],po['y'],po['x']+po['width'],po['y']+po['height']
                
            if classes[p].lower() not in ignore_:
                image_info = {}
                ann = {}
                image_info['filename'] = str(p)+a['filename']
                #print(bbox[p])
                #x1, y1, x2, y2 = bbox[p]
                image_info['width'] = x2-x1
                image_info['height'] = y2-y1
                ann['labels'] =  classes[p]
                #ann['labels'] =  np.array([class_dict[classes[p].lower()]], dtype=np.int32)
                image_info['ann'] =ann
                crop_img = image[y1:y2, x1:x2].copy()
                print(crop_img.shape)
                if 0 in crop_img.shape:
                    print('here2')
                    print(a['filename'])
                    continue
                crop_img = cv2.cvtColor(crop_img,cv2.COLOR_BGR2RGB)
                cv2.imwrite(out+image_info['filename'] ,crop_img)
                complete.append(image_info)
                
    return True

if __name__ == "__main__":
    annotations1= json.load(open('D:/Harish/code/DTS/via_region_data.json'))
    annotations = list(annotations1.values())
    annotations = [a for a in annotations if a['regions']]
    len(annotations)
    functionfinal(argument)