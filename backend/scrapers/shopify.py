from scrapers.polite import get


def hoodies_from_shopify(base_url, store_name, currency="GBP", max_pages=10):
    out = []
    for page in range(1, max_pages + 1):
        url = f"{base_url}/products.json?limit=250&page={page}"
        products = get(url).json().get("products", [])
        if not products:
            break
        for p in products:
            text = " ".join([p["title"], p.get("product_type", ""), " ".join(p.get("tags", []))]).lower()
            if "hood" not in text:
                continue
            v = p["variants"][0]
            out.append({
                "store": store_name,
                "name": p["title"],
                "brand": p.get("vendor"),
                "price": float(v["price"]),
                "currency": currency,
                "image": p["images"][0]["src"] if p["images"] else None,
                "url": f"{base_url}/products/{p['handle']}",
                "sizes": [x["title"] for x in p["variants"] if x.get("available")],
            })
        print(f"  {store_name}: page {page} done, {len(out)} hoodies so far")
    return out