
from pathlib import Path
import pymupdf
import json


RAW_FOLDER = Path("dataset/raw")


OUTPUT_FILE = Path("dataset/processed/documents.json")

documents = []

for pdf_path in sorted(RAW_FOLDER.rglob("*.pdf")):
    try:
        with pymupdf.open(pdf_path) as pdf:
            text = "\n".join(
                page.get_text() for page in pdf
            )

            document = {
                "id": f"doc_{len(documents) + 1:03d}",
                "title": pdf_path.stem,
                "source": pdf_path.parent.name,
                "filename": pdf_path.name,
                "pages": len(pdf),
                "text": text.strip()
            }

            documents.append(document)

            print(f"Extracted: {pdf_path.name}")

    except Exception as error:
        print(f"Failed: {pdf_path.name} - {error}")

# Create output folder if missing
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Save extracted documents
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(documents, file, indent=2, ensure_ascii=False)

print(f"\nTotal documents extracted: {len(documents)}")
print(f"Saved to: {OUTPUT_FILE}")
