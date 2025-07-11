import cv2
from datetime import datetime
import os
import logging
import warnings

# Suppress FutureWarnings from PyTorch
warnings.filterwarnings("ignore", category=FutureWarning)

# Import detectors
from detectors.detect_face_visibility import is_face_visible
from detectors.detect_partial_face import is_partial_face
from detectors.detect_looking_away_opencv import is_looking_away
from detectors.detect_multiple_persons import detect_person_count_yolo
from detectors.detect_phone_usage import detect_phone
from detectors.detect_away_duration import AwayTracker
from detectors.event_tracker import EventTracker

# Trackers for different detection events
partial_face_tracker = EventTracker("Partial face detected")
looking_away_tracker = EventTracker("Candidate looking away")
no_face_tracker = EventTracker("No face detected")
phone_tracker = EventTracker("Phone detected", log_level="ERROR")
multi_person_tracker = EventTracker("Multiple persons detected", log_level="ERROR")


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
LOG_PATH = "reports/test2_proctoring.log"

logger = setup_logger(LOG_PATH)

logger.info("===== Starting Proctoring Session =====")
logger.info(f"Video: {VIDEO_PATH}")

cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = 0
away_tracker = AwayTracker()

frame_interval = int(fps)  # ✔ Check every 10 seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Only process every 10 seconds
    if frame_count % frame_interval != 0:
        continue

    timestamp = frame_count / fps
    frame_time_obj = datetime.utcfromtimestamp(timestamp)
    frame_time_str = frame_time_obj.strftime('%H:%M:%S')

    # Run detectors
    face_visible = is_face_visible(frame)
    partial_face = is_partial_face(frame)
    looking_away = is_looking_away(frame)
    phone_visible = detect_phone(frame)
    person_count = detect_person_count_yolo(frame)

    # Track & log away-return events
    just_returned = away_tracker.update(face_visible, frame_time_obj)
    if just_returned:
        start, end, duration = just_returned
        logger.warning(
            f"Candidate was away from screen from {start.strftime('%H:%M:%S')} to {end.strftime('%H:%M:%S')} — duration: {str(duration)}"
        )

    # Logging detections
    if not face_visible:
        logger.warning(f"No face detected at : [{frame_time_str}]")
    elif partial_face:
        logger.warning(f"Partial face detected at : [{frame_time_str}]")
    elif looking_away:
        logger.warning(f"Candidate looking away at : [{frame_time_str}]")

    if person_count > 1:
        logger.error(f"Multiple persons detected: {person_count} at : [{frame_time_str}]")
    elif person_count < 1:
        logger.warning(f"No person detected at : [{frame_time_str}]")

    if phone_visible:
        logger.error(f"Phone detected at : [{frame_time_str}]")

# Finalize any ongoing away status
away_tracker.finalize(frame_time_obj)

logger.info(f"Total away-from-screen time: {str(away_tracker.get_total_away_time())}")
logger.info("===== Proctoring Session Ended =====")

cap.release()
print(f"✅ Log saved at: {LOG_PATH}")
