import json
import time
from tqdm import tqdm
from app.retrievers.pinecone_retriever import PineconeRetriever
from app.config_loader import Config

DATA_FILE = "data/vietnam_travel_dataset.json"
BATCH_SIZE = 32


def main():
    retriever = PineconeRetriever()
    index = retriever.index

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        nodes = json.load(f)

    items = []
    for node in nodes:
        semantic_text = node.get("semantic_text") or (node.get("description") or "")[:1000]
        if not semantic_text.strip():
            continue
        meta = {
            "id": node.get("id"),
            "type": node.get("type"),
            "name": node.get("name"),
            "city": node.get("city", node.get("region", "")),
            "tags": node.get("tags", []),
        }
        items.append((node["id"], semantic_text, meta))

    print(f"Preparing to upsert {len(items)} items to Pinecone...")

    for i in tqdm(range(0, len(items), BATCH_SIZE), desc="Uploading"):
        batch = items[i : i + BATCH_SIZE]
        ids = [item[0] for item in batch]
        texts = [item[1] for item in batch]
        metas = [item[2] for item in batch]

        embeddings = retriever.get_embedding(texts[0]) if len(texts) == 1 else [
            retriever.get_embedding(t) for t in texts
        ]

        vectors = [
            {"id": _id, "values": emb, "metadata": meta}
            for _id, emb, meta in zip(ids, embeddings, metas)
        ]
        index.upsert(vectors)
        time.sleep(0.2)

    print("All items uploaded successfully!")


if __name__ == "__main__":
    main()
