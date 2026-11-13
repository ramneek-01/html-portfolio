# DocuLens — Local Document Intelligence

A local document retrieval tool that indexes PDF, Markdown, and text files, then returns ranked evidence passages with source metadata.

## Capabilities
- PDF page extraction and recursive folder ingestion.
- Passage chunking with overlap.
- TF-IDF unigram/bigram indexing and cosine-similarity ranking.
- Source filename and PDF page attribution for each result.
- CLI and optional Streamlit interface; no paid API or hosted LLM required.

## Run
```bash
pip install -r requirements.txt
python -m doculens.cli index ./sample_docs --index-dir ./.doculens_index
python -m doculens.cli search "how is model drift monitored?" --index-dir ./.doculens_index
streamlit run app.py
pytest
```

This is retrieval, not generative question answering. It returns passages for human inspection. Local indexes may contain sensitive document text; protect them accordingly.
