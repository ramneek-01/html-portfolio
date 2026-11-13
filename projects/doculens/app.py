import streamlit as st
import pandas as pd
from doculens.engine import DocumentIndex
st.set_page_config(page_title="DocuLens",layout="wide")
st.title("DocuLens | Local Document Search")
st.caption("Evidence-first retrieval with TF-IDF. Results are passages, not generated answers.")
folder=st.text_input("Document folder","sample_docs")
if st.button("Build / refresh index"):
    try:
        idx=DocumentIndex();n=idx.ingest(folder);idx.save(".doculens_index");st.success(f"Indexed {n} passages")
    except Exception as e:st.error(str(e))
q=st.text_input("Search documents");k=st.slider("Results",1,10,5)
if st.button("Search"):
    try:
        for r in DocumentIndex.load(".doculens_index").search(q,k):
            label=r["source"]+(f" · page {r['page']}" if r["page"] else "")
            with st.expander(f"{label} · relevance {r['score']}"):st.write(r["text"])
    except Exception as e:st.error(str(e))
