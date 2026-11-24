
import csv
import time
from pathlib import Path

from search_dcoument import search_documents

QUERIES = [
    "Household water chlorination",
    "Safe drinking water storage",
    "Waterborne disease prevention",
    "Water quality monitoring",
    "Sanitation and hygiene in schools",
    "Household water filtration",
    "Drinking water contamination",
    "Handwashing and disease prevention",
    "Emergency drinking water treatment",
    "Safe sanitation practices",
    "Solar water disinfection",
    "Prevention of cholera",
    "Rainwater harvesting",
    "Wastewater treatment",
    "Rural drinking water supply",
    "Microbial contamination of water",
    "Menstrual hygiene management",
    "How can I make drinking water safe at home?",
    "How can communities prevent diarrhoeal diseases?",
    "How do I make flood water safe to drink?"
]

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "evaluation"
OUTPUT_DIR.mkdir(exist_ok=True)

results_file = OUTPUT_DIR / "retrieval_results.csv"
timing_file = OUTPUT_DIR / "response_times.csv"

all_results = []
timing_results = []

# Warm-up request
search_documents("drinking water", top_k=10)

for index, query in enumerate(QUERIES, start=1):

    query_id = f"Q{index:02d}"

    start_time = time.perf_counter()

    results = search_documents(
        query=query,
        top_k=10
    )

    elapsed_ms = (
        time.perf_counter() - start_time
    ) * 1000

    timing_results.append({
        "query_id": query_id,
        "query": query,
        "results_count": len(results),
        "response_time_ms": round(elapsed_ms, 3)
    })

    for rank, result in enumerate(results, start=1):

        all_results.append({
            "query_id": query_id,
            "query": query,
            "rank": rank,
            "chunk_id": result["chunk_id"],
            "document_id": result["document_id"],
            "title": result["title"],
            "source": result["source"],
            "filename": result["filename"],
            "bm25_score": result["score"],
            "text": result["text"],
            "relevance": ""
        })

    print(
        f"{query_id}: {len(results)} results | "
        f"{elapsed_ms:.2f} ms"
    )

result_fields = [
    "query_id", "query", "rank", "chunk_id",
    "document_id", "title", "source", "filename",
    "bm25_score", "text", "relevance"
]

with open(
    results_file, "w", newline="", encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file, fieldnames=result_fields
    )

    writer.writeheader()
    writer.writerows(all_results)

with open(
    timing_file, "w", newline="", encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "query_id",
            "query",
            "results_count",
            "response_time_ms"
        ]
    )

    writer.writeheader()
    writer.writerows(timing_results)

print("\nEvaluation data collection completed!")
print("Total queries:", len(QUERIES))
print("Total retrieved passages:", len(all_results))
print("Results saved to:", results_file)
print("Response times saved to:", timing_file)
