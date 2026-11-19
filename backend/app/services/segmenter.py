import numpy as np
from PIL import Image
from transformers import pipeline

# Loads the model once when the server starts (downloads ~100 MB the first time)
_seg = pipeline("image-segmentation", model="mattmdjaga/segformer_b2_clothes")


def crop_upper_clothes(img: Image.Image):
    """Return (cropped hoodie image on white background, mask) or (None, None)."""
    results = _seg(img)
    masks = {r["label"]: np.array(r["mask"]) > 0 for r in results}
    mask = masks.get("Upper-clothes")

    if mask is None or mask.sum() < 500:
        return None, None

    ys, xs = np.where(mask)
    box = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))

    white = Image.new("RGB", img.size, "white")
    white.paste(img, mask=Image.fromarray((mask * 255).astype("uint8")))
    return white.crop(box), mask