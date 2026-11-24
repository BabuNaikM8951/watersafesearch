
import json
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

file_path = (
    BASE_DIR / "dataset" / "processed" / "chunks.json"
)

with open(file_path, "r", encoding="utf-8") as file:
    chunks = json.load(file)

documents = {}
chunk_counts = Counter()
word_counts = []

for chunk in chunks:
    source = chunk["source"].upper()

    documents[chunk["document_id"]] = source
    chunk_counts[source] += 1
    word_counts.append(len(chunk["text"].split()))

document_counts = Counter(documents.values())

print("=" * 50)
print("WATERSAFE DATASET STATISTICS")
print("=" * 50)

print("Total PDF documents:", len(documents))
print("Total chunks:", len(chunks))
print("Total indexed words:", sum(word_counts))

print("\nSOURCE DISTRIBUTION")

for source in sorted(document_counts):
    print(f"\nSource: {source}")
    print(f"PDF documents: {document_counts[source]}")
    print(f"Text chunks: {chunk_counts[source]}")

print("\nCHUNK STATISTICS")
print("Minimum words:", min(word_counts))
print("Maximum words:", max(word_counts))
print("Average words:", round(
    sum(word_counts) / len(word_counts), 2
))
