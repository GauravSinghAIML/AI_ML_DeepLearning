# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 10:43:58 2020

@author: gs52078
"""

import pandas as pd
dataframe = pd.read_csv("D:\\Data_DTS\\final_New.csv")
UnqData = dataframe['Lebel'].unique()
dic = UnqData.set_index('0').T.to_dict('int')
import glob
import cv2
cv_img = []
for img in glob.glob("D:/GauravSingh_OldComuterBackup/TDATA/classification_data/*.jpg"):
    n= cv2.imread(img)
    cv_img.append(n)

imList = glob.glob("D:/GauravSingh_OldComuterBackup/TDATA/classification_data/*.jpg")

dataframeTem = dataframe
sorData = dataframe.sort_values('filename')

imageListData0 = sorData.iloc[0].values[0]
co = 0
aa =""
listFile = []
widthList = []
heightList = []
labelList =[]
for i in range(1,len(sorData)):
    #print("------------------------------")
    #print(imageListData0)
    aa = sorData.iloc[i].values[0]
    ww0 = sorData.iloc[i-1].values[1]
    hh0 = sorData.iloc[i-1].values[2]
    ll0 = sorData.iloc[i-1].values[3]
    if(imageListData0==aa):
        listFile.append(str(co)+imageListData0)
        widthList.append(ww0)
        heightList.append(hh0)
        labelList.append(ll0)
        #sorData1["filename"]= sorData1["filename"].replace(sorData1.iloc[i-1].values[0], str(co)+imageListData0)
        #print(str(co)+imageListData0)
        co=co+1
    else:
        #sorData1.loc[i-1,0] = str(co)+imageListData0
        listFile.append(str(co)+imageListData0)
        widthList.append(ww0)
        heightList.append(hh0)
        labelList.append(ll0)
        #sorData1["filename"]= sorData1["filename"].replace(sorData1.iloc[i-1].values[0], str(co)+imageListData0)
        print(str(co)+imageListData0)
        print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
        imageListData0=aa
        #ww0 = ww
        #hh0 = hh
        #ll0 = ll
        co = 0
else:
    #sorData1.loc[i-1,0] = str(co)+imageListData0
    listFile.append(str(co)+imageListData0)
    widthList.append(ww0)
    heightList.append(hh0)
    labelList.append(ll0)
data = {'filename':listFile,
        'width':widthList,
        'height':heightList,
        'label':labelList}
df = pd.DataFrame(data)
export_csv = df.to_csv (r'D:\Data_DTS\export_dataframe.csv', index = None, header=True)