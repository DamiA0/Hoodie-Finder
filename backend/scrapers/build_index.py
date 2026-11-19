import hashlib
import io
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from PIL import Image

from app.services import embedder, vector_store
from scrapers.polite import UA

CATALOGUE = Path("data/catalogue.json")
IMG_DIR = Path("data/images")
IMG_DIR.mkdir(parents=True, exist_ok=True)
BATCH = 32


def load_image(url):
    path = IMG_DIR / (hashlib.md5(url.encode()).hexdigest() + ".jpg")
    try:
        if not path.exists():
            r = httpx.get(url, headers={"User-Agent": UA}, timeout=30, follow_redirects=True)
            r.raise_for_status()
            img = Image.open(io.BytesIO(r.content)).convert("RGB")
            img.thumbnail((512, 512))          # smaller = faster, still plenty for matching
            img.save(path)
        return Image.open(path).convert("RGB")
    except Exception:
        return None


def main():
    products = [p for p in json.loads(CATALOGUE.read_text()) if p.get("image") and p.get("url")]
    if len(sys.argv) > 1:
        products = products[: int(sys.argv[1])]

    already = set(vector_store.col.get(include=[])["ids"])
    todo = [p for p in products if p["url"] not in already]
    print(f"{len(products)} hoodies, {len(already)} already indexed, {len(todo)} to do")

    done = 0
    with ThreadPoolExecutor(max_workers=8) as pool:
        for start in range(0, len(todo), BATCH):
            chunk = todo[start:start + BATCH]
            imgs = list(pool.map(lambda p: load_image(p["image"]), chunk))
            pairs = [(p, i) for p, i in zip(chunk, imgs) if i is not None]
            if not pairs:
                continue
            vectors = embedder.embed_images([i for _, i in pairs])
            for (p, _), vec in zip(pairs, vectors):
                vector_store.add_product(p, vec)
            done += len(pairs)
            print(f"  {done}/{len(todo)} indexed")

    print(f"\nFinished: {vector_store.col.count()} hoodies in the index")


if __name__ == "__main__":
    main()