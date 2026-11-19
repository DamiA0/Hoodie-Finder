import io
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
from app.services import segmenter, colour, attributes, embedder, vector_store, ranker

router = APIRouter()
DEBUG_DIR = Path("data/debug")
DEBUG_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/analyse")
async def analyse(file: UploadFile = File(...), max_price: float | None = None):
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(400, "Please upload a JPG, PNG or WEBP image")

    img = Image.open(io.BytesIO(await file.read())).convert("RGB")
    crop, mask = segmenter.crop_upper_clothes(img)
    if crop is None:
        raise HTTPException(422, "No hoodie/top found - try a clearer photo")

    crop.save(DEBUG_DIR / "last_crop.jpg")
    attrs = attributes.classify(crop)
    attrs["colour"] = colour.dominant_colour(img, mask)

    vec = embedder.embed_image(crop)
    matches = ranker.rank(vector_store.query(vec, n=30, max_price=max_price), attrs)
    return {"attributes": attrs, "results": matches[:12]}