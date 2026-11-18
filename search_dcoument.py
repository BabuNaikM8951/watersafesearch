
import requests

from connection_settings import connection_url, auth, index_prefix

INDEX_NAME = f"{index_prefix()}watersafe"
SEARCH_URL = (
    f"{connection_url().rstrip('/')}/{INDEX_NAME}/_search"
)


def search_documents(query, top_k=10, source=None):
    """
    Search indexed PDF chunks using BM25 ranking.
    """

    if not query.strip():
        return []

    search_body = {
        "size": top_k,
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title^2", "text"]
            }
        },
        "_source": [
            "chunk_id",
            "document_id",
            "title",
            "source",
            "filename",
            "text"
        ]
    }

    # Optional filtering by document source
    if source:
        search_body["query"] = {
            "bool": {
                "must": [
                    search_body["query"]
                ],
                "filter": [
                    {
                        "term": {
                            "source": source.lower()
                        }
                    }
                ]
            }
        }

    response = requests.post(
        SEARCH_URL,
        json=search_body,
        auth=auth(),
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for hit in data["hits"]["hits"]:
        document = hit["_source"]

        results.append({
            "chunk_id": document.get("chunk_id"),
            "document_id": document.get("document_id"),
            "title": document.get("title"),
            "source": document.get("source"),
            "filename": document.get("filename"),
            "score": hit["_score"],
            "text": document.get("text", "")
        })

    return results


def display_results(results):
    """Print search results in a readable format."""

    if not results:
        print("\nNo matching documents found.")
        return

    print(f"\nFound {len(results)} results:\n")

    for position, result in enumerate(results, start=1):
        print("=" * 70)
        print(f"Result {position}")
        print(f"Title: {result['title']}")
        print(f"Source: {result['source']}")
        print(f"Filename: {result['filename']}")
        print(f"BM25 Score: {result['score']:.4f}")
        print(f"Chunk ID: {result['chunk_id']}")

        text = result["text"]
        snippet = text[:400].replace("\n", " ")

        print(f"Snippet: {snippet}...")
        print()


def main():
    print("=" * 70)
    print("WATERSAFE SEARCH ENGINE")
    print("BM25 Information Retrieval")
    print("=" * 70)

    while True:
        query = input(
            "\nEnter your search query (or 'exit'): "
        ).strip()

        if query.lower() in ("exit", "quit"):
            print("Exiting WaterSafe Search.")
            break

        if not query:
            print("Please enter a search query.")
            continue

        try:
            results = search_documents(query, top_k=10)
            display_results(results)

        except requests.exceptions.RequestException as error:
            print("Search error:", error)


if __name__ == "__main__":
    main()
