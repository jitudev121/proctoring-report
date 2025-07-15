import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection

def is_partial_face(frame, min_visibility_ratio=0.15):
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(frame_rgb)

        if not results.detections:
            return False

        height, width = frame.shape[:2]
        frame_area = height * width

        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            face_width = int(bbox.width * width)
            face_height = int(bbox.height * height)
            face_area = face_width * face_height

            visibility_ratio = face_area / frame_area

            if visibility_ratio < min_visibility_ratio:
                return True
    return False
