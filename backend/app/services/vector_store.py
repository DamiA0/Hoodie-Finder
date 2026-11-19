import chromadb

client = chromadb.PersistentClient(path="data/chroma")
col = client.get_or_create_collection("hoodies", metadata={"hnsw:space": "cosine"})


def add_product(product, vector):
    meta = {k: (v if isinstance(v, (str, int, float)) else str(v))
            for k, v in product.items() if v is not None and k != "sizes"}
    col.upsert(ids=[product["url"]], embeddings=[vector], metadatas=[meta])


def query(vector, n=30, max_price=None):
    if col.count() == 0:
        return []
    where = {"price": {"$lte": max_price}} if max_price else None
    r = col.query(query_embeddings=[vector], n_results=min(n, col.count()), where=where)
    return [dict(m, similarity=round(1 - d, 3))
            for m, d in zip(r["metadatas"][0], r["distances"][0])]