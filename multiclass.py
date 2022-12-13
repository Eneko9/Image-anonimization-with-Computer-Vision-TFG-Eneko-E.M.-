import FacePlateBlur.facePlateDetector as fpd
import cv2
import time
import os 
from os import listdir

#yoloPath = '/Users/mentxaka/yolov5' 
#yoloPath = "/content/yolov5"
yoloPath = r"C:\Users\eneko\yolov5" 

multiclassModel = fpd.loadYolo(yoloPath)

#inPATH = "/Users/mentxaka/Github/TK-VisionArtificial/Face-PlateDetector/Arona_persona.jpg"
#outPATH = "/Users/mentxaka/Github/TK-VisionArtificial/Face-PlateDetector/mod_Arona_persona.jpg"

inPATH = r"C:\Users\eneko\GitHub\TK-VisionArtificial\Face-PlateDetector\input_imgs"
outPATH = r"C:\Users\eneko\GitHub\TK-VisionArtificial\Face-PlateDetector\output_imgs"

start_time = time.time()*1000

for image in os.listdir(inPATH):
    filename = inPATH + os.sep + image
    points, classes = fpd.detection(filename,multiclassModel)
    img = fpd.hideObject(cv2.imread(filename),points,classes)
    cv2.imwrite(outPATH + os.path.sep + image,img)

print("MultiClass --- %s miliseconds ---" % str((time.time()*1000 - start_time)))


