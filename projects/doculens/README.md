# DocuLens — Local Document Search

A local tool for indexing PDF, Markdown, and text files and retrieving relevant passages with source metadata.

## Features
- PDF page extraction and folder ingestion.
- Text chunking with overlap.
- TF-IDF indexing and cosine-similarity ranking.
- Source filename and PDF page references.
- Command-line interface and optional Streamlit UI.

## Run
```bash
pip install -r requirements.txt
python -m doculens.cli index ./sample_docs --index-dir ./.doculens_index
python -m doculens.cli search "how is model drift monitored?" --index-dir ./.doculens_index
streamlit run app.py
pytest
```

DocuLens retrieves passages; it does not generate answers. Review retrieved text in context. Protect local indexes if they contain sensitive documents.
