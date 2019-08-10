from pycocotools.coco import COCO
import requests
import time
import os.path
import csv

path = 'coco/downloaded_images/train2017'
filenames = [img for img in glob.glob(path+"/*.jpg")]


for f in filenames:
    print(f)

    # with open(desLabelPath+"/"+imgdirname+"/"+name+".txt", mode='w') as label:


