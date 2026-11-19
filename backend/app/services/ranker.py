def rank(candidates, attrs):
    colour = attrs["colour"]["name"]
    want_zip = "zip" in attrs["closure"]["label"]
    for c in candidates:
        name = c.get("name", "").lower()
        bonus = 0.05 if colour in name else 0
        bonus += 0.05 if ("zip" in name) == want_zip else 0
        c["score"] = round(c["similarity"] + bonus, 3)
    return sorted(candidates, key=lambda c: c["score"], reverse=True)