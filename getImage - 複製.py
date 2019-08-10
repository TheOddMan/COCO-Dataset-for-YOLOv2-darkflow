from pycocotools.coco import COCO
import requests
import time
import os.path
import csv

jsonPath = 'coco/annotations'
imgdirpath = 'coco/downloaded_images'

jsonFile = 'instances_train2017.json'
imgDir = "train2017"


coco = COCO(jsonPath+"/"+jsonFile)
cats = coco.loadCats(coco.getCatIds())
# nms=[cat['name'] for cat in cats]
# print('COCO categories: \n{}\n'.format(' '.join(nms)))
#
# catIds = coco.getCatIds(catNms=['person'])
# imgIds = coco.getImgIds(catIds=catIds )
imgIds = coco.getImgIds()
images = coco.loadImgs(imgIds)
print(len(images))


# print("imgIds: ", imgIds)
# print("images: ", images)
# print(len(imgIds))
count = 0
count_downloaded = 0
for im in images:
    imgName = im['file_name']
    try:
        if os.path.isfile(imgdirpath +"/" + imgDir + "/" + im['file_name']):
            count_downloaded = count_downloaded+1
            name = im['file_name'].split(".")[0]
            print("Image : ",name," is already downloaded.   Pass")
            print("===================The number of downloaded images : {}".format(str(count_downloaded)))
            continue

        img_data = requests.get(im['coco_url']).content
        count  = count +1
        with open(imgdirpath +"/" + imgDir + "/" + im['file_name'], 'wb') as handler:
            handler.write(img_data)
        print("The number of downloading images : {}",str(count))
    except (requests.exceptions.RequestException,ConnectionResetError) as err:
        print(err)
        print(str(count+count_downloaded),"  images have been downloaded.")
        # print("im: ", name)
        print("has been blocked!")
        time.sleep(60)
        continue
