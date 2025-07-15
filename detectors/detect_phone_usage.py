from ultralytics import YOLO

# Load the YOLOv8 model (you can use 'yolov8n.pt', 'yolov8s.pt', etc.)
model = YOLO("yolov8n.pt")  # Make sure this file is downloaded or use a path/url

def detect_phone(frame):
    results = model.predict(frame, verbose=False)

    for result in results:
        boxes = result.boxes
        classes = boxes.cls.cpu().tolist()

        # 67 is the COCO class ID for 'cell phone'
        if 67 in map(int, classes):
            return True

    return False
