import numpy as np
import base64
from io import BytesIO
from PIL import Image

def read_image_from_bytes(file_bytes):
    img = Image.open(BytesIO(file_bytes)).convert("RGB")
    return np.array(img)

def preprocess(img_np, target_size=(224,224)):
    img = Image.fromarray(np.uint8(img_np))
    img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
    img_norm = np.array(img_resized).astype("float32") / 255.0
    return np.expand_dims(img_norm, axis=0)

def to_base64_png(img_np):
    """Convert numpy array to base64 PNG"""
    # Ensure image is in the right format
    if isinstance(img_np, np.ndarray):
        img = Image.fromarray(np.uint8(img_np))
    else:
        img = img_np
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def overlay_heatmap_on_image(orig_img, heatmap, alpha=0.5):
    """Overlay heatmap on original image using PIL"""
    # Normalize heatmap to 0-255
    heatmap_normalized = np.uint8(255 * heatmap)
    
    # Apply colormap manually (red for high values)
    heatmap_rgb = np.zeros((*heatmap_normalized.shape, 3), dtype=np.uint8)
    heatmap_rgb[:, :, 0] = heatmap_normalized  # Red channel
    heatmap_rgb[:, :, 1] = 0  # Green channel
    heatmap_rgb[:, :, 2] = np.uint8(255 * (1 - heatmap))  # Blue channel
    
    # Resize images to match
    heatmap_img = Image.fromarray(heatmap_rgb)
    orig_img_pil = Image.fromarray(np.uint8(orig_img))
    heatmap_img = heatmap_img.resize(orig_img_pil.size, Image.Resampling.LANCZOS)
    
    # Blend images
    blended = Image.blend(orig_img_pil, heatmap_img, alpha)
    return np.array(blended)
