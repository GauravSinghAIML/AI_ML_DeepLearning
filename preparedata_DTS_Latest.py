# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 15:50:57 2020

@author: gs52078
"""


#DTS Latest Processing

import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold
import json
import torchvision.transforms as transforms
import numpy as np
import os
import skimage
import skimage.io as io
import cv2
import xlrd
import pandas as pd
from mmcv.image import imread, imwrite, imrescale
import mmcv
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import random
from skimage.exposure import histogram,equalize_hist,equalize_adapthist,rescale_intensity,is_low_contrast

from imgaug import augmenters as iaa
import imgaug as ia
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from imgaug.augmentables import Keypoint, KeypointsOnImage
#aug = iaa.Sometimes(0.5, [iaa.Affine(scale=(0.2, 0.7))])
#iaa.Sequential([iaa.Affine(scale=(0.2, 0.7))])
aug1 = iaa.Affine(rotate=90)
aug2 = iaa.Affine(rotate=-90)
aug3 = iaa.Affine(rotate=180)

from mmcv.opencv_info import USE_OPENCV2

if not USE_OPENCV2:
    from cv2 import IMREAD_COLOR, IMREAD_GRAYSCALE, IMREAD_UNCHANGED
else:
    from cv2 import CV_LOAD_IMAGE_COLOR as IMREAD_COLOR
    from cv2 import CV_LOAD_IMAGE_GRAYSCALE as IMREAD_GRAYSCALE
    from cv2 import CV_LOAD_IMAGE_UNCHANGED as IMREAD_UNCHANGED


annotations1 = json.load(open('D:/Harish/code/Poles/data/FINAL.json'))
#annotations2 = json.load(open('D:/Harish/code/panorama/cyclo_data/gaurav.json'))
#annotations2 = json.load(open('D:/Harish/code/panorama/mmdetection-master/train_data/via_region_anuhya.json'))
#annotations3 = json.load(open('D:/Harish/code/panorama/mmdetection-master/train_data/via_region_data.json'))
annotations = list(annotations1.values()) #+ list(annotations2.values())+ list(annotations3.values())
annotations_a = [a for a in annotations if a['regions']]
annotations_b = [a for a in annotations if not a['regions']]
len(annotations_a)