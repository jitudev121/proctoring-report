import cv2
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo

# Setup Detectron2 predictor
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file(
    "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
    "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
)
cfg.MODEL.DEVICE = "cpu"  # or "cuda" if using GPU

predictor = DefaultPredictor(cfg)

def detect_phone(frame):
    outputs = predictor(frame)
    classes = outputs["instances"].pred_classes.tolist()
    return 67 in classes  # 67 is class ID for cell phone
