import cv2
import numpy as np
import math
import os
import torch
import traceback

#relative = os.getcwd() + os.path.sep + "Face-PlateDetector" + os.path.sep + "FacePlateBlur" #local
relative = os.getcwd() + os.path.sep + "FacePlateBlur" #local

#yoloPath = '/Users/mentxaka/yolov5' #path yolo de Oier
#yoloPath = r"C:\Users\eneko\yolov5" #path yolo de Eneko

def loadYolo(yoloPath):
    weightsPath = relative + os.path.sep + "weights" + os.path.sep + "best4.pt" 
    #weightsPath = "/Users/mentxaka/Github/TK-VisionArtificial/Face-PlateDetector/FaceBlur/weights/best.pt"
    return torch.hub.load(yoloPath, 'custom', path=weightsPath, source='local',force_reload=True)  # default

def detection(path, model):
    results = model(path)
    results.print()
    positionsArray = []
    classArray = []
    i = 0
    while True:       
        try:
            x0, y0, x1, y1, _, classType = results.xyxy[0][i].numpy().astype(int)
            x00,y00,x11,y11,classType = int(x0),int(y0), int(x1), int(y1), int(classType)
            positionsArray.append([(x00,y00),(x11,y11)])
            classArray.append(classType)
            i+=1
        except Exception:
            break
    return positionsArray, classArray

def faceblur(img, width, height, x0, y0, x1, y1):
    centro = (int(x0+((x1-x0)/2)),int(y0+((y1-y0)/2)))
    radio = int((math.sqrt(width * width + height * height) // 2)/1.5)
    cv2.circle(img, centro, radio, (255, 255, 255), -1)

def hideObject(img,points,classes):
    index = 0
    for p in points:
        if(classes[index]==0):
            mask = np.zeros(img.shape, dtype='uint8')
            width = p[1][0]-p[0][0]
            height = p[1][1]-p[0][1]
            mask_img = np.zeros(img.shape, dtype='uint8')
            faceblur(mask_img,width,height,p[0][0],p[0][1],p[1][0],p[1][1])
            img_all_blurred = cv2.medianBlur(img, 99)
            img = np.where(mask_img > 0, img_all_blurred, img)
        elif(classes[index]==1):
            cv2.rectangle(img, p[0], p[1], (255, 255, 255), -1)
        index+=1
    return img