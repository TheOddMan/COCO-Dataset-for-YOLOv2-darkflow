from pycocotools.coco import COCO
import requests
import time
import os.path
import csv

#======================================================The area you can modify
jsonPath = 'annotations'                #The directory path where coco json file is
imgdirpath = 'downloaded_images/train2017'        #The directory path where the downloaded images are stored

jsonFile = 'instances_train2017.json'       #The json file downloaded from coco


categories = ['person']             #Specify the categories you want (go to coco to see what categories you can select)
#======================================================

coco = COCO(jsonPath+"/"+jsonFile)
cats = coco.loadCats(coco.getCatIds())

catIds = coco.getCatIds(catNms=categories)
imgIds = coco.getImgIds(catIds=catIds )

images = coco.loadImgs(imgIds)
print("=============    Total images : ",len(images),"  ===========")

count_blocked = 0
count_downloaded = 0
for im in images:
    imgName = im['file_name']
    try:
        if os.path.isfile(imgdirpath+ "/" + im['file_name']):
            count_downloaded = count_downloaded+1
            name = im['file_name'].split(".")[0]
            print("Image : ",name," was already downloaded.   Pass")
            print("===================    The number of downloaded images : {}".format(str(count_downloaded)),"     ===================")
            continue

        img_data = requests.get(im['coco_url']).content
        count_downloaded  = count_downloaded +1
        with open(imgdirpath+ "/" + im['file_name'], 'wb') as handler:
            handler.write(img_data)

        print("===================      The number of downloaded images : {}".format(str(count_downloaded)),"     ===================")


    except (requests.exceptions.RequestException,ConnectionResetError) as err:
        count_blocked = count_blocked+1
        print(err)
        print(imgName," has been blocked!")
        time.sleep(60)
        continue

print("=========    Downloaded Images : ",count_downloaded,"    =========")
print("=========    Blocked Images : ",count_blocked,"  =========")#p
