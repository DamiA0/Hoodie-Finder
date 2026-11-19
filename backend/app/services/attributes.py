import torch
from app.services.embedder import model, tokenizer, preprocess

QUESTIONS = {
    "garment": ["a hoodie", "a sweatshirt without a hood", "a t-shirt", "a jacket", "a shirt"],
    "closure": ["a pullover hoodie", "a full zip-up hoodie", "a quarter-zip top"],
    "fit": ["an oversized baggy hoodie", "a regular fit hoodie",
            "a slim fit hoodie", "a cropped hoodie"],
    "pattern": ["a plain solid colour hoodie", "a hoodie with a large graphic print",
                "a striped hoodie", "a camouflage hoodie", "a tie-dye hoodie"],
    "logo": ["a hoodie with a large logo", "a hoodie with a small chest logo",
             "a hoodie with no logo"],
}


@torch.no_grad()
def classify(crop):
    img = model.encode_image(preprocess(crop).unsqueeze(0), normalize=True)
    out = {}
    for key, labels in QUESTIONS.items():
        txt = model.encode_text(tokenizer(labels), normalize=True)
        probs = (100.0 * img @ txt.T).softmax(dim=-1)[0]
        i = int(probs.argmax())
        out[key] = {"label": labels[i], "confidence": round(float(probs[i]), 2)}
    out["size"] = {"label": "can't be read from a photo - choose your size", "confidence": None}
    return out