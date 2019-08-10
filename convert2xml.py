import os
import cv2
from lxml import etree
import xml.etree.cElementTree as ET
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

def write_xml(folder,image,im, anns, savedir):
    height, width, depth = image.shape

    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'folder').text = folder
    ET.SubElement(annotation, 'filename').text = im['file_name']
    ET.SubElement(annotation, 'segmented').text = '0'
    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(im["width"])
    ET.SubElement(size, 'height').text = str(im["height"])
    ET.SubElement(size, 'depth').text = str(depth)

    for ann in anns:
        ob = ET.SubElement(annotation, 'object')
        ET.SubElement(ob, 'name').text = "person"
        ET.SubElement(ob, 'pose').text = 'Unspecified'
        ET.SubElement(ob, 'truncated').text = '0'
        ET.SubElement(ob, 'difficult').text = '0'
        bbox = ET.SubElement(ob, 'bndbox')
        ET.SubElement(bbox, 'xmin').text = str(ann['bbox'][0])
        ET.SubElement(bbox, 'ymin').text = str(ann['bbox'][1])
        ET.SubElement(bbox, 'xmax').text = str(ann['bbox'][0] + ann['bbox'][2])
        ET.SubElement(bbox, 'ymax').text = str(ann['bbox'][1] + ann['bbox'][3])

    # for obj, topl, botr in zip(anns, tl, br):
    #     ob = ET.SubElement(annotation, 'object')
    #     ET.SubElement(ob, 'name').text = obj
    #     ET.SubElement(ob, 'pose').text = 'Unspecified'
    #     ET.SubElement(ob, 'truncated').text = '0'
    #     ET.SubElement(ob, 'difficult').text = '0'
    #     bbox = ET.SubElement(ob, 'bndbox')
    #     ET.SubElement(bbox, 'xmin').text = ann['bbox'][0]
    #     ET.SubElement(bbox, 'ymin').text = ann['bbox'][1]
    #     ET.SubElement(bbox, 'xmax').text = ann['bbox'][0] + ann['bbox'][2]
    #     ET.SubElement(bbox, 'ymax').text = ann['bbox'][1] = ann['bbox'][3]

    xml_str = ET.tostring(annotation)
    root = etree.fromstring(xml_str)
    xml_str = etree.tostring(root, pretty_print=True)
    save_path = os.path.join(savedir, im['file_name'].replace('jpg', 'xml'))
    with open(save_path, 'wb') as temp_xml:
        temp_xml.write(xml_str)


if __name__ == '__main__':

    folder = 'images'
    for im in images:
        imgName = im['file_name']
        # try:
        if os.path.isfile(imgdirpath + '/' + imgdirname + '/' + im['file_name']):
            # print("Image : ",imgName," is already downloaded.   Pass")
            name = im['file_name'].split(".")[0]
            print("Processing ", name)
            annIds = coco.getAnnIds(imgIds=im['id'], catIds=catIds, iscrowd=None)
            anns = coco.loadAnns(annIds)

            p = cv2.imread(imgdirpath + '/' + imgdirname + '/' + im['file_name'])

            write_xml("D:\\XinYu\\Face\\customYOLO\\darkflow\\personDetect\\downloaded_images\\train2017",
                      p,im,anns,"darkflow\\personDetect\\annotations")

