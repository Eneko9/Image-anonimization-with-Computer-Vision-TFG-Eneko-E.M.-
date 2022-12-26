from fastapi import FastAPI, File, UploadFile, Request, Form
import shutil
import os
import io
import cv2
from starlette.responses import StreamingResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pathlib import Path
from pydantic import BaseModel
import FacePlateBlur.facePlateDetector as fpd
from typing import List
from PIL import Image

relative = os.getcwd()

app = FastAPI()

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
    resultsPath = relative + os.path.sep + "static" + os.path.sep + "results"
    for f in os.listdir(resultsPath):
        os.remove(os.path.join(resultsPath, f))
    picPath = relative + os.path.sep + "static" + os.path.sep + "pictures"
    for f in os.listdir(picPath):
        os.remove(os.path.join(picPath, f))
    zipPath = relative + os.path.sep + "static" + os.path.sep + "detections.zip"
    if os.path.exists(zipPath):
        os.remove(zipPath)
    yoloPath = os.getcwd() + "/yolov7"
    multiclassModel = fpd.loadYolo(yoloPath)
    for file in files:
        path = "static" + os.path.sep  + "pictures" + os.path.sep + f'{file.filename}'
        with open( path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        points, classes = fpd.detection(path,multiclassModel)
        img = fpd.hideObject(cv2.imread(path),points,classes)
        path =  relative + os.path.sep + "static" + os.path.sep + "results" + os.path.sep + f'{file.filename}'
        cv2.imwrite(path,img)
    shutil.make_archive( relative + os.path.sep + "static" + os.path.sep +'detections', 'zip', relative + os.path.sep + "static" + os.path.sep + "results")
    path = "detections.zip"
    return templates.TemplateResponse("returnImg.html",{"request":request,"path": path})
