# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 11:21:24 2019

@author: hy52188
"""
from __future__ import print_function, division
import os
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import json
from PIL import Image
import skimage
import cv2

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")
from classes import classes

class Mydataset(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, root_dir, idxs, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        final =pd.read_csv('/home/cytuser/code/panorama/pretrained-models.pytorch-master/classification_data/final.csv')
        final['label'] = final['label'].apply(lambda x: classes(x))
        self.img_infos = final.loc[idxs]
        self.img_infos = self.img_infos.reset_index()
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.img_infos)
    
    def load_annotations(self, ann_file):
        return json.load(open(ann_file))

    def trim(im):
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)
        else:
            return im


    def __getitem__(self, idx):
        img_info = self.img_infos.loc[idx]
        img_name = os.path.join(self.root_dir,img_info['filename'])
        img = skimage.io.imread(img_name,as_gray=True)
        shp = min(img.shape[:-1])
        #img = skimage.io.imread(img_name)
        #img = skimage.transform.resize(img,(224,224))
        #image=cv2.addWeighted (img,10, cv2.GaussianBlur( img , (0,0) , 224/10) ,-10 ,128)
        img=cv2.addWeighted (img,10, cv2.GaussianBlur( img , (0,0) , shp*0.3) ,-10 ,128)
        image = skimage.transform.resize(img,(224,224))
        image = Image.fromarray(np.uint8(image))
        #image = Image.open(img_name)
        #image = image.convert('RGB')
        label = img_info['label']
        #print(img_info['filename'])
        #landmarks = np.array([landmarks])
        #landmarks = landmarks.astype('float').reshape(-1, 2)

        if self.transform:
            #print('here')
            image = self.transform(image)
        #print(image.view())
        #sample = {'image': image , 'label': label}

        return image,label


    def __getitem__old(self, idx):
        img_info = self.img_infos.loc[idx]
        img_name = os.path.join(self.root_dir,img_info['filename'])
        img = skimage.io.imread(img_name,as_gray=True)
        shp = min(img.shape[:-1])
        #img = skimage.io.imread(img_name)
        img = skimage.transform.resize(img,(224,224))
        image=cv2.addWeighted (img,10, cv2.GaussianBlur( img , (0,0) , 224/10) ,-10 ,128)
        image = Image.fromarray(np.uint8(image))
        #image = Image.open(img_name)
        #image = image.convert('RGB')
        label = img_info['label']
        #print(img_info['filename'])
        #landmarks = np.array([landmarks])
        #landmarks = landmarks.astype('float').reshape(-1, 2)

        if self.transform:
            #print('here')
            image = self.transform(image)
        #print(image.view())
        #sample = {'image': image , 'label': label}

        return image,label