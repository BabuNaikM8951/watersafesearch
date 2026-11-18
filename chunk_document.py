
import json
from pathlib import Path

INPUT_FILE = Path("dataset/processed/documents.json")
OUTPUT_FILE = Path("dataset/processed/chunks.json")

CHUNK_SIZE = 500
OVERLAP = 100

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    documents = json.load(f)

chunks = []

for doc in documents:
    words = doc["text"].split()
    step = CHUNK_SIZE - OVERLAP

    for start in range(0, len(words), step):
        chunk_words = words[start:start + CHUNK_SIZE]

        if not chunk_words:
            continue

        chunk_id = len(chunks) + 1

        chunks.append({
            "chunk_id": chunk_id,
            "document_id": doc["id"],
            "title": doc["title"],
            "source": doc["source"],
            "filename": doc["filename"],
            "text": " ".join(chunk_words)
        })

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print("Total documents:", len(documents))
print("Total chunks created:", len(chunks))
print("Saved to:", OUTPUT_FILE)
