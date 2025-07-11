import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def is_looking_away(frame, center_tolerance=100):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    height, width = frame.shape[:2]
    frame_center_x = width // 2

    for (x, y, w, h) in faces:
        face_center_x = x + w // 2
        if abs(face_center_x - frame_center_x) > center_tolerance:
            return True
    return False
