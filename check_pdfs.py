
from pathlib import Path
import fitz
import csv

folder = Path("/Users/babunaikm/Desktop/WaterSafeSearch/")
results = []

for pdf_file in sorted(folder.rglob("*")):
    if not pdf_file.is_file() or pdf_file.suffix.lower() != ".pdf":
        continue

    try:
        with fitz.open(pdf_file) as doc:
            pages = len(doc)
            text = "".join(page.get_text() for page in doc)
            chars = len(text.strip())

            if pages == 0:
                status = "EMPTY"
            elif chars < 100:
                status = "NO READABLE TEXT"
            else:
                status = "PASS"

            results.append([
                str(pdf_file), pages, chars, status
            ])

            print(f"{status}: {pdf_file.name} ({pages} pages)")

    except Exception as e:
        results.append([str(pdf_file), 0, 0, "ERROR"])
        print(f"ERROR: {pdf_file.name} - {e}")

with open("pdf_check_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Filename", "Pages", "Characters", "Status"])
    writer.writerows(results)

print("\nTotal PDFs checked:", len(results))
print("Results saved to pdf_check_results.csv")
