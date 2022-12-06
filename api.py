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
    return templates.TemplateResponse("uploadImg.html", {"request":request})

@app.post("/detector/response/",  response_class=HTMLResponse)
def detectorResponse(request: Request, file: UploadFile = File(...)):
    path = "static" + os.path.sep  + "pictures" + os.path.sep + f'{file.filename}'
    with open( path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    yoloPath = os.getcwd() + "/yolov5"
    multiclassModel = fpd.loadYolo(yoloPath)
    points = fpd.multiclassDetection(path,multiclassModel)
    img = fpd.multiclassBoxing(cv2.imread(path),points)
    path =  relative + os.path.sep + "static" + os.path.sep + "results" + os.path.sep + f'{file.filename}'
    cv2.imwrite(path,img)
    path = "results/"+ f'{file.filename}'
    return templates.TemplateResponse("returnImg.html",{"request":request,"path": path})
