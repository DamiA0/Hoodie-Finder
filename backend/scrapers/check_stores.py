import time

from scrapers.polite import UA, allowed
import httpx

CANDIDATES = [
    "https://representclo.com",
    "https://www.brokenplanet.com",
    "https://www.trapstarlondon.com",
    "https://www.gymshark.com",
    "https://kith.com",
    "https://www.dailypaperclothing.com",
    "https://www.hellstar.com",
    "https://sp5derworldwide.com",
    "https://www.syna-world.com",
    "https://www.minusmanyclothing.com",
    "https://www.vertabrae.com",
    "https://www.unknownlondon.com",
    "https://www.zoneoutclothing.com",
    "https://www.ma-strum.com",
    "https://www.adanola.com",
    "https://www.pegadorfashion.com",
    "https://www.cloneclothing.co.uk",
    "https://www.nofacesclothing.com",
    "https://www.thesupermade.com",
    "https://www.thedrenn.co.uk",
    "https://www.missguided.com",
    "https://brotherandkin.com",
    "https://noissey.com",
]


def check(base):
    url = f"{base}/products.json?limit=250"
    try:
        if not allowed(url):
            return "❌ robots.txt says no"
        r = httpx.get(url, headers={"User-Agent": UA}, timeout=20, follow_redirects=True)
        if r.status_code != 200:
            return f"❌ blocked/not Shopify ({r.status_code})"
        products = r.json().get("products", [])
        hoodies = [p for p in products if "hood" in (p["title"] + " " + p.get("product_type", "")).lower()]
        return f"✅ works - {len(products)} products, {len(hoodies)} hoodies on page 1"
    except Exception as e:
        return f"❌ error ({type(e).__name__})"


if __name__ == "__main__":
    for base in CANDIDATES:
        print(f"{base:45} {check(base)}")
        time.sleep(2)