# -*- coding: utf-8 -*-

'''
!git clone https://github.com/ultralytics/yolov5
!pip install -r /content/yolov5/requirements.txt
'''
import torch
import cv2
import os

#relative = os.getcwd() + os.path.sep + "Face-PlateDetector" + os.path.sep + "PlateBlur" #local
relative = os.getcwd() + os.path.sep + "PlateBlur" #local


def loadYolo(yoloPath):
    weightsPath = relative + os.path.sep + "weights" + os.path.sep + "plates.pt" 
    #weightsPath = "/Users/mentxaka/Github/TK-VisionArtificial/Face-PlateDetector/PlateBlur/weights/best.pt"
    return torch.hub.load(yoloPath, 'custom', path=weightsPath, source='local', force_reload=True)  # default
     
def plateDetection(path,model):
    results = model(path)
    results.print()       
    x0, y0, x1, y1, _, _ =  results.xyxy[0][0].numpy().astype(int) 
    return (int(x0),int(y0)),(int(x1),int(y1))

def plateBoxing(img,points):
    return cv2.rectangle(img, points[0], points[1], (255, 255, 255), -1)
 
