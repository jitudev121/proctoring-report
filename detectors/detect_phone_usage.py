import torch

model = torch.hub.load('yolov5', 'yolov5s', source='local')

def detect_phone(frame):
    results = model(frame)
    for *box, conf, cls in results.xyxy[0]:
        if int(cls) == 67:  # 67 is the COCO class for cell phone
            return True
    return False
