import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection

def is_looking_away(frame, center_tolerance=100):
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(frame_rgb)

        if not results.detections:
            return False  # No face detected

        detection = results.detections[0]  # Only consider the first face
        bbox = detection.location_data.relative_bounding_box

        height, width = frame.shape[:2]
        frame_center_x = width // 2

        # Get face center in absolute pixel value
        face_x = int(bbox.xmin * width)
        face_width = int(bbox.width * width)
        face_center_x = face_x + face_width // 2

        return abs(face_center_x - frame_center_x) > center_tolerance
