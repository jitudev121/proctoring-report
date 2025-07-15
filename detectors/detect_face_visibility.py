import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection

def is_face_visible(frame):
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(frame_rgb)
        return results.detections is not None and len(results.detections) > 0
