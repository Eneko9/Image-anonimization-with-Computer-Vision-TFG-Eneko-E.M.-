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
    weightsPath = relative + os.path.sep + "weights" + os.path.sep + "best2.pt" 
    #weightsPath = "/Users/mentxaka/Github/TK-VisionArtificial/Face-PlateDetector/FaceBlur/weights/best.pt"
    return torch.hub.load(yoloPath, 'custom', path=weightsPath, source='local',force_reload=True)  # default

def multiclassDetection(path, model):
    results = model(path)
    results.print()
    positionsArray = []
    i = 0
    while True:       
        try:
            x0, y0, x1, y1, _, _ = results.xyxy[0][i].numpy().astype(int)
            x00,y00,x11,y11 = int(x0),int(y0), int(x1), int(y1)
            positionsArray.append([(x00,y00),(x11,y11)])
            i+=1
        except Exception:
            break
    return positionsArray

def multiclassBoxing(img,points):
    for p in points:
        cv2.rectangle(img, p[0], p[1], (255, 255, 255), -1)
    return img

