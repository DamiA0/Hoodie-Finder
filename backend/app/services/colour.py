import numpy as np
from sklearn.cluster import KMeans

NAMED = {
    "black": (20, 20, 20), "charcoal": (55, 55, 60), "grey": (128, 128, 128),
    "white": (240, 240, 240), "navy": (30, 40, 80), "blue": (50, 100, 200),
    "green": (40, 130, 60), "olive": (110, 110, 50), "red": (200, 30, 30),
    "burgundy": (110, 20, 40), "pink": (240, 150, 180), "purple": (120, 60, 160),
    "brown": (110, 70, 40), "beige": (220, 200, 170), "orange": (240, 130, 30),
    "yellow": (240, 220, 50),
}


def dominant_colour(img, mask):
    px = np.array(img)[mask].reshape(-1, 3)
    px = px[np.random.choice(len(px), min(5000, len(px)), replace=False)]
    km = KMeans(n_clusters=3, n_init=5, random_state=0).fit(px)
    centre = km.cluster_centers_[np.bincount(km.labels_).argmax()]
    name = min(NAMED, key=lambda n: np.linalg.norm(centre - np.array(NAMED[n])))
    return {"name": name, "hex": "#%02x%02x%02x" % tuple(int(c) for c in centre)}