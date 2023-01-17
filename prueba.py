from ultralytics import YOLO

model = YOLO(r"yolov8n.pt")
print("--------------------------")
outputs = model.predict(r"static\pictures\1 (22).png", return_outputs= True)

for output in outputs:
    for detection in output['det']:
        top_x, top_y, bottom_x, bottom_y, accuracy, type = detection
        print(top_x, top_y, bottom_x, bottom_y, type)
#treat the outputs as a Python generator
# https://github.com/ultralytics/ultralytics/issues/324