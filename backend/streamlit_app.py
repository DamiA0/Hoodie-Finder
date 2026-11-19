import streamlit as st
from PIL import Image
from app.services import segmenter, colour, attributes, embedder, vector_store, ranker

st.set_page_config(page_title="Hoodie Finder", page_icon="🧥", layout="wide")
st.title("Hoodie Finder")
st.caption("Upload a photo of a look and find similar hoodies with prices.")


def short(label):
    return (label.removeprefix("a ").removeprefix("an ")
            .removesuffix(" hoodie").removeprefix("hoodie with "))


c1, c2, c3 = st.columns([2, 1, 1])
uploaded = c1.file_uploader("Choose a photo", type=["jpg", "jpeg", "png", "webp"])
max_price = c2.number_input("Max price £ (0 = no limit)", min_value=0, value=0, step=5)
size = c3.selectbox("Your size (optional)", ["", "XS", "S", "M", "L", "XL", "XXL"])

if uploaded and st.button("Find similar hoodies", type="primary"):
    img = Image.open(uploaded).convert("RGB")
    with st.spinner("Analysing your photo... (first run can take a minute)"):
        crop, mask = segmenter.crop_upper_clothes(img)
        if crop is None:
            st.error("No hoodie/top found - try a clearer photo.")
            st.stop()
        attrs = attributes.classify(crop)
        attrs["colour"] = colour.dominant_colour(img, mask)
        vec = embedder.embed_image(crop)
        results = ranker.rank(
            vector_store.query(vec, n=30, max_price=max_price or None), attrs)[:12]

    left, right = st.columns([1, 2])
    left.image(img, caption="Your photo", use_container_width=True)
    with right:
        st.subheader("What we found")
        st.markdown(f"**Colour:** {attrs['colour']['name']} ({attrs['colour']['hex']})")
        for key, title in [("closure", "Style"), ("fit", "Fit"), ("pattern", "Pattern"), ("logo", "Logo")]:
            a = attrs[key]
            note = f" _({round(a['confidence'] * 100)}% sure)_" if a["confidence"] < 0.6 else ""
            st.markdown(f"**{title}:** {short(a['label'])}{note}")
        st.markdown(f"**Size:** {size or 'choose your size above'}")

    st.subheader(f"{len(results)} similar hoodies")
    if not results:
        st.info("No matches - try a higher max price.")
    cols = st.columns(4)
    for i, p in enumerate(results):
        with cols[i % 4]:
            if p.get("image"):
                st.image(p["image"], use_container_width=True)
            st.markdown(f"**{p.get('name', 'Hoodie')}**")
            st.caption(f"{p.get('store', '')} · {round(p['similarity'] * 100)}% match")
            st.markdown(f"### £{float(p['price']):.2f}")
            st.link_button("View at retailer", p["url"], use_container_width=True)