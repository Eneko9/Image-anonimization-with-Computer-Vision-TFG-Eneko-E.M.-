import cv2
import numpy as np
import math
import os
from ultralytics import YOLO

relative = os.getcwd() + os.path.sep + "FacePlateBlur" #locals
root = os.getcwd()
def loadYolo(weights):
    model = YOLO(weights) #cargar el modelo de yolo
    return model

def detection(path, model, testing=False):
    if testing:
        results = model.predict(path, save=True, save_txt=True)#for testing, it saves the results in Yolo format in order to compare with expected results
    elif not testing:
        results = model.predict(path) #for production, it doesn't save the results
    #results = model.predict(path)
    positionsArray = []
    classArray = []
    i = 0
    while True:       
        try:
            x0, y0, x1, y1= results[0].boxes.xyxy.numpy().astype(int)[i]
            cls = results[0].boxes.cls.numpy().astype(int)[i]
            x00,y00,x11,y11,classType = int(x0),int(y0), int(x1), int(y1), int(cls)
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