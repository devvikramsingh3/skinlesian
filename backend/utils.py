import numpy as np
import cv2, base64
from io import BytesIO
from PIL import Image
import tensorflow as tf

def read_image_from_bytes(file_bytes):
    img = Image.open(BytesIO(file_bytes)).convert("RGB")
    return np.array(img)

def preprocess(img_np, target_size=(224,224)):
    img_resized = cv2.resize(img_np, target_size)
    img_norm = img_resized.astype("float32") / 255.0
    return np.expand_dims(img_norm, axis=0)

def to_base64_png(cv2_bgr_img):
    _, buffer = cv2.imencode(".png", cv2_bgr_img)
    return base64.b64encode(buffer).decode("utf-8")

def overlay_heatmap_on_image(orig_img, heatmap, alpha=0.5):
    heatmap_color = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)
    orig_resized = cv2.resize(orig_img, (heatmap.shape[1], heatmap.shape[0]))
    overlay = cv2.addWeighted(orig_resized, 1 - alpha, heatmap_color, alpha, 0)
    return overlay
