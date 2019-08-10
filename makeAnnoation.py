from pycocotools.coco import COCO
import requests
import time
import os.path
import csv

jsonPath = 'coco/annotations'
jsonFile = 'instances_train2017.json'
imgdirname = jsonFile.split('_')[1].split('.')[0]
imgdirpath = 'coco/downloaded_images'
desLabelPath = 'coco/labels'

coco = COCO(jsonPath+'/'+jsonFile)
cats = coco.loadCats(coco.getCatIds())

catIds = coco.getCatIds(catNms=['person'])
imgIds = coco.getImgIds(catIds=catIds )
images = coco.loadImgs(imgIds)

count = 0
for im in images:
    imgName = im['file_name']
    # try:
    if os.path.isfile(imgdirpath+'/'+imgdirname+'/'+im['file_name']):
        # print("Image : ",imgName," is already downloaded.   Pass")
        name = im['file_name'].split(".")[0]
        print("Processing ",name)
        annIds = coco.getAnnIds(imgIds=im['id'], catIds=catIds, iscrowd=None)
        anns = coco.loadAnns(annIds)
        imgWidth = im["width"]
        imgHeight = im['height']

        # with open("{}/{}/{}/{}.txt".format("coco","labels",imgdirname,name),mode='w') as label:
        with open(desLabelPath+"/"+imgdirname+"/"+name+".txt", mode='w') as label:
            for ann in anns:
                x = ann['bbox'][0]
                x_ = x/imgWidth
                y = ann['bbox'][1]
                y_ = y/imgHeight
                ab_width = ann['bbox'][2]
                ab_width_ = ab_width/imgWidth
                ab_height = ann['bbox'][3]
                ab_height_ = ab_height/imgHeight

                writestring = "0 {} {} {} {}\n".format(str(x_),str(y_),str(ab_width_),str(ab_height_))

                label.writelines(writestring)

