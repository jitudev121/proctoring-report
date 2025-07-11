import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def is_partial_face(frame, min_visibility_ratio=0.15):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    height, width = frame.shape[:2]
    frame_area = height * width

    for (x, y, w, h) in faces:
        face_area = w * h
        visibility_ratio = face_area / frame_area
        if visibility_ratio < min_visibility_ratio:
            return True
    return False
