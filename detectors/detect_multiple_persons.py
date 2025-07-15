from ultralytics import YOLO
import cv2

# Load YOLOv8 model (e.g., yolov8n.pt or yolov8s.pt)
model = YOLO("yolov8n.pt")  # Use 'yolov8n.pt' for speed or 'yolov8s.pt' for better accuracy

def detect_person_count_yolo(frame):
    # Run YOLOv8 inference
    results = model.predict(source=frame, imgsz=416, conf=0.5, verbose=False)

    # Get number of people detected
    count = 0
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            if cls_id == 0:  # 0 = person in COCO
                count += 1
    return count
