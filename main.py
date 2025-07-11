import cv2
from datetime import datetime
import os
import logging
import warnings

# Suppress FutureWarnings from PyTorch
warnings.filterwarnings("ignore", category=FutureWarning)
from detectors.event_tracker import EventTracker


# Import detectors
from detectors.detect_face_visibility import is_face_visible
from detectors.detect_partial_face import is_partial_face
from detectors.detect_looking_away_opencv import is_looking_away
from detectors.detect_multiple_persons import detect_person_count_yolo
from detectors.detect_phone_usage import detect_phone

# Setup logger
def setup_logger(log_file='reports/default.log'):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%H:%M:%S'
    )
    return logging.getLogger()

# Paths
VIDEO_PATH = "video_input/test2.mp4"
LOG_PATH = "reports/test1_proctoring.log"

logger = setup_logger(LOG_PATH)

logger.info("===== Starting Proctoring Session =====")
logger.info(f"Video: {VIDEO_PATH}")

cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)

frame_count = 0

frame_interval = int(fps*2)  # ✔ Check every 10 seconds

# Create event trackers
trackers = {
    "no_face": EventTracker("Face not detected"),
    "partial_face": EventTracker("Partial face"),
    "looking_away": EventTracker("Candidate looking away"),
    "multiple_persons": EventTracker("Multiple persons detected"),
    "no_person": EventTracker("No person detected"),
    "phone": EventTracker("Phone usage")
}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Only process every 10 seconds
    if frame_count % frame_interval != 0:
        continue

    timestamp = frame_count / fps
    frame_time = datetime.utcfromtimestamp(timestamp).strftime('%H:%M:%S')

    # Run detectors
    face_visible = is_face_visible(frame)
    partial_face = is_partial_face(frame)
    looking_away = is_looking_away(frame)
    # multi_person = detect_multiple_faces_yolo(frame)
    phone_visible = detect_phone(frame)
    person_count = detect_person_count_yolo(frame)

    trackers["no_face"].update(not face_visible, timestamp, logger)
    trackers["partial_face"].update(partial_face, timestamp, logger)
    trackers["looking_away"].update(looking_away, timestamp, logger)
    trackers["phone"].update(phone_visible, timestamp, logger)
    trackers["multiple_persons"].update(person_count > 1, timestamp, logger)
    trackers["no_person"].update(person_count < 1, timestamp, logger)


logger.info("===== Proctoring Session Ended =====")

final_time = frame_count / fps
for tracker in trackers.values():
    tracker.finalize(logger, final_time)
cap.release()
print(f" Log saved at: {LOG_PATH}")
