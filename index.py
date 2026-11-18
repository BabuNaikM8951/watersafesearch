
import json
from pathlib import Path

import requests

from connection_settings import connection_url, auth, index_prefix

# Project configuration
BASE_DIR = Path(__file__).resolve().parent
CHUNKS_FILE = BASE_DIR / "dataset" / "processed" / "chunks.json"

INDEX_NAME = f"{index_prefix()}watersafe"
BULK_URL = f"{connection_url().rstrip('/')}/_bulk"

BATCH_SIZE = 200


def load_chunks():
    """Load text chunks from the JSON file."""

    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {CHUNKS_FILE}"
        )

    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    if not isinstance(chunks, list):
        raise ValueError(
            "Expected chunks.json to contain a JSON list."
        )

    print(f"Total chunks loaded: {len(chunks)}")

    if chunks:
        print("First chunk fields:", list(chunks[0].keys()))

    return chunks


def prepare_bulk_data(chunks):
    """Convert chunks into OpenSearch bulk format."""

    lines = []

    for chunk in chunks:
        # Create a stable ID for each chunk
        chunk_id = chunk.get("chunk_id")

        if chunk_id is None:
            raise ValueError(
                "A chunk is missing its chunk_id."
            )

        action = {
            "index": {
                "_index": INDEX_NAME,
                "_id": str(chunk_id)
            }
        }

        document = {
            "chunk_id": chunk_id,
            "document_id": str(
                chunk.get("document_id", "")
            ),
            "title": chunk.get("title", ""),
            "source": chunk.get("source", ""),
            "filename": chunk.get("filename", ""),
            "text": chunk.get("text", "")
        }

        lines.append(json.dumps(action, ensure_ascii=False))
        lines.append(json.dumps(document, ensure_ascii=False))

    return "\n".join(lines) + "\n"


def upload_batch(batch, batch_number):
    """Upload a batch of chunks using the Bulk API."""

    payload = prepare_bulk_data(batch)

    response = requests.post(
        BULK_URL,
        data=payload.encode("utf-8"),
        headers={
            "Content-Type": "application/x-ndjson"
        },
        auth=auth(),
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    if result.get("errors"):
        failures = []

        for item in result.get("items", []):
            operation = item.get("index", {})

            if operation.get("error"):
                failures.append(operation)

        print(
            f"Batch {batch_number} contains "
            f"{len(failures)} failed documents."
        )

        for failure in failures[:3]:
            print(failure)

        raise RuntimeError(
            "Bulk upload failed. Check the errors above."
        )

    print(
        f"Batch {batch_number}: "
        f"{len(batch)} chunks uploaded successfully."
    )


def main():
    chunks = load_chunks()

    if not chunks:
        print("No chunks available for indexing.")
        return

    total_batches = (
        len(chunks) + BATCH_SIZE - 1
    ) // BATCH_SIZE

    print("Index name:", INDEX_NAME)
    print("Total batches:", total_batches)

    for start in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[start:start + BATCH_SIZE]

        batch_number = start // BATCH_SIZE + 1

        upload_batch(batch, batch_number)

    # Refresh index to make documents searchable
    refresh_url = (
        f"{connection_url().rstrip('/')}/"
        f"{INDEX_NAME}/_refresh"
    )

    refresh_response = requests.post(
        refresh_url,
        auth=auth(),
        timeout=30
    )

    refresh_response.raise_for_status()

    print("\nIndexing completed successfully!")
    print(f"Total chunks processed: {len(chunks)}")


if __name__ == "__main__":
    main()
