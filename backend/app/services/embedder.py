import open_clip
import torch

# Downloads ~800 MB the first time, then loads from cache
MODEL_NAME = "hf-hub:Marqo/marqo-fashionSigLIP"
model, _, preprocess = open_clip.create_model_and_transforms(MODEL_NAME)
tokenizer = open_clip.get_tokenizer(MODEL_NAME)
model.eval()


@torch.no_grad()
def embed_image(img):
    return model.encode_image(preprocess(img).unsqueeze(0), normalize=True)[0].tolist()

@torch.no_grad()
def embed_images(imgs):
    batch = torch.stack([preprocess(i) for i in imgs])
    return model.encode_image(batch, normalize=True).tolist()