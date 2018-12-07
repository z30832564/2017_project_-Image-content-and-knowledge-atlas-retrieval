# coding=utf-8
from search.colordescriptor import ColorDescriptor

import glob
import cv2
import pymongo

# mongodb数据库初始化
db = pymongo.MongoClient()
features = db.features
index = db.features.tindex

cd = ColorDescriptor((8, 3, 3))


import pymongo
import pandas as pd
data = pd.read_table('data1.txt', sep='\s+')
columns = list(data.columns)
# mongodb数据库初始化

# glob遍历数据集图片，生成数据集存入MongoDB数据库中
def jstz(imagePath):
    ID = imagePath[imagePath.rfind("/") + 1:]
    imageID = ID[:10]
    image = cv2.imread(imagePath)
    image = cv2.Canny(image, image.shape[0], image.shape[1])
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.imwrite(imageID+'.jpg',image)

    # #提取特征值
    _features = cd.describe(image)
    _features = [float(f) for f in _features]
    return imageID, _features


for i in range(len(data)):
    f = {}
    for j in range(len(columns)):
        f[columns[j]] = str(data.loc[i][j])
    path = str(data.loc[i][4])
    imageID_,features_ = jstz(imagePath=path)
    f['_id'] = imageID_
    f[imageID_] = features_
    index.insert_one(f)