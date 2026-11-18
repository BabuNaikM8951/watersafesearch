# WaterSafe Search

A Streamlit application for searching water, sanitation, and hygiene (WASH) passages from WHO, UNICEF, and CDC PDF documents. It indexes document chunks in OpenSearch and ranks results using BM25.

## Features

- Search document titles and passage text.
- Filter results by WHO, UNICEF, or CDC.
- Choose how many results to display.
- View a passage preview and expand it to read the full text.

## Requirements

- Python 3.10 or later
- A running OpenSearch instance that the project can reach
- The source PDF collection, placed locally under `dataset/raw/`

## Setup

From the project directory, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Configure the OpenSearch connection in a `.env` file in the project root:

```dotenv
OPENSEARCH_URL=http://localhost:9200
OPENSEARCH_USERNAME=
OPENSEARCH_PASSWORD=
OPENSEARCH_PROTOCOL=http
```

For an authenticated or remote OpenSearch instance, set the URL and credentials for that instance. Keep `.env` private; it is excluded from Git.

## Add and index documents

The PDF collection and generated JSON files are not included in this repository. Add PDFs to the matching source folders:

```text
dataset/raw/
├── cdc/
├── unicef/
└── who/
```

Run these commands from the project root to extract text, split documents into chunks, and upload the chunks to OpenSearch:

```bash
python exctract_document.py
python chunk_document.py
python index.py
```

The scripts create `dataset/processed/documents.json` and `dataset/processed/chunks.json`. The index name is `watersafe` when no username and password are configured. When both credentials are set, the username is prefixed to the index name.

To check the OpenSearch connection:

```bash
python test_connection.py
```

## Run the application

After OpenSearch is running and the chunks have been indexed:

```bash
streamlit run app.py
```

Streamlit prints a local URL (usually `http://localhost:8501`) where you can use the search interface.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit search interface |
| `search_dcoument.py` | OpenSearch BM25 query and command-line search |
| `connection_settings.py` | Loads OpenSearch settings from `.env` |
| `exctract_document.py` | Extracts text and metadata from source PDFs |
| `chunk_document.py` | Splits extracted text into overlapping chunks |
| `index.py` | Uploads chunks to OpenSearch |
| `check_pdfs.py` | Checks local PDFs for readable text |
| `test_connection.py` | Tests the OpenSearch connection |

## Notes

- Search requires an existing OpenSearch index populated by `index.py`.
- Source PDFs, processed data, virtual environments, and local configuration are excluded from Git.
- The sidebar currently displays fixed corpus totals (49 PDFs and 4,200 chunks); those figures do not update automatically when the local collection changes.
