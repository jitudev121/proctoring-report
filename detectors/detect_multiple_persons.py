
import torch
import os

# Load YOLO model once
yolo_path = os.path.abspath("yolov5")  # Adjust if needed
model = torch.hub.load(yolo_path, 'yolov5s', source='local')
model.classes = [0]  # Only detect 'person'

def detect_person_count_yolo(frame):
    results = model(frame, size=416)  # smaller size = faster
    count = 0
    for *box, conf, cls in results.xyxy[0]:
        if int(cls) == 0:  # 0 = person
            count += 1
    return count