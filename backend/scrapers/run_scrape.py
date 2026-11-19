import json
from datetime import date
from pathlib import Path

from scrapers.shopify import hoodies_from_shopify

STORES = [
    {"name": "Represent", "url": "https://representclo.com"},
    {"name": "Trapstar London", "url": "https://www.trapstarlondon.com"},
    {"name": "Kith", "url": "https://kith.com"},
    {"name": "Noissey", "url": "https://www.hellstar.com"},
    {"name": "Noissey", "url": "https://sp5derworldwide.com"},
    {"name": "Vertabrae", "url": "https://www.vertabrae.com"},
    {"name": "Adanola", "url": "https://www.adanola.com"},
    {"name": "Pegador Fashion", "url": "https://www.pegadorfashion.com"},
    {"name": "Clone Clothing", "url": "https://www.thesupermade.com"},
    {"name": "No Faces Clothing", "url": "https://www.thedrenn.co.uk"},
    {"name": "Brother & Kin", "url": "https://brotherandkin.com"},
]

OUT = Path("data/catalogue.json")


def main():
    everything = []
    for s in STORES:
        print(f"Scraping {s['name']}...")
        try:
            items = hoodies_from_shopify(s["url"], s["name"])
            for item in items:
                item["checked_on"] = str(date.today())
            everything += items
        except Exception as e:
            print(f"  Skipped {s['name']}: {e}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(everything, indent=2))
    print(f"\nSaved {len(everything)} hoodies to {OUT}")


if __name__ == "__main__":
    main()