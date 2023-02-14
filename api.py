from fastapi import FastAPI, File, UploadFile, Request, Form
import shutil
import os
import cv2
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import FacePlateBlur.facePlateDetector as fpd
from typing import List
relative = os.getcwd()

app = FastAPI()

multiclassModel = fpd.loadYolo(r"FacePlateBlur\weights\v8\best3.pt")


app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def detector(request: Request):
    return templates.TemplateResponse("uploadImg2.html", {"request":request})

@app.post("/detector/response/",  response_class=HTMLResponse)
def detectorResponse(request: Request, files: List[UploadFile]= File(...)):
    
    yoloAnnotations = relative + os.path.sep + "runs" + os.path.sep + "detect" + os.path.sep + "predict" + os.path.sep + "labels"
    yoloAnnotations2 = relative + os.path.sep + "static" + os.path.sep + "annotationResults"
    for f in os.listdir(yoloAnnotations2):
        os.remove(os.path.join(yoloAnnotations2, f))
    
    resultsPath = relative + os.path.sep + "static" + os.path.sep + "results"
    for f in os.listdir(resultsPath):
        os.remove(os.path.join(resultsPath, f))
    
    zipPath = relative + os.path.sep + "static" + os.path.sep + "detections.zip"
    if os.path.exists(zipPath):
        os.remove(zipPath)

    filenames = []
    #iterate in all the files recieved in order to detect and hide the plates and faces.
    for file in files:
        filenames.append(file.filename)
        path = "static" + os.path.sep  + "pictures" + os.path.sep + f'{file.filename}'
        with open( path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        points, classes = fpd.detection(path,multiclassModel) #detect the objects in the image
        img = fpd.hideObject(cv2.imread(path),points,classes) #hide the deteced objects 
        path =  relative + os.path.sep + "static" + os.path.sep + "results" + os.path.sep + f'{file.filename}'
        cv2.imwrite(path,img)
    
    #once detected and hided, the results are stored in a .zip file
    shutil.make_archive( relative + os.path.sep + "static" + os.path.sep +'detections', 'zip', relative + os.path.sep + "static" + os.path.sep + "results")
    path = "detections.zip"

    #delete de results, picture files in case they exist
    picPath = relative + os.path.sep + "static" + os.path.sep + "pictures"
    for f in os.listdir(picPath):
        os.remove(os.path.join(picPath, f))
    yoloAnnotations = relative + os.path.sep + "runs" + os.path.sep + "detect" + os.path.sep + "predict" + os.path.sep + "labels"
    yoloAnnotations2 = relative + os.path.sep + "static" + os.path.sep + "annotationResults"
    for f in os.listdir(yoloAnnotations):
        os.rename(os.path.join(yoloAnnotations, f),os.path.join(yoloAnnotations2, f))
    shutil.rmtree(relative + os.path.sep + "runs", ignore_errors=False, onerror=None)
    return templates.TemplateResponse("returnImg.html",{"request":request,"path": path,"filenames":filenames})



@app.post("detectImg",  response_class=FileResponse)
def detectorResponse(request: Request, file:UploadFile = File(...)):

    path = "static" + os.path.sep  + "pictures" + os.path.sep + f'{file.filename}'
    
    points, classes = fpd.detection(path,multiclassModel) #detect the objects in the image
    img = fpd.hideObject(cv2.imread(path),points,classes) #hide the deteced objects 
    path =  relative + os.path.sep + "static" + os.path.sep + "results" + os.path.sep + f'{file.filename}'
    cv2.imwrite(path,img)
    
    return FileResponse(path)