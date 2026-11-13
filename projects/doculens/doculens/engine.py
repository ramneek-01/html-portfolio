from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import re, joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class Passage:
    text: str
    source: str
    page: int | None = None

class DocumentIndex:
    def __init__(self):
        self.passages=[]
        self.vectorizer=TfidfVectorizer(stop_words="english",ngram_range=(1,2),max_features=50000,sublinear_tf=True)
        self.matrix=None
    @staticmethod
    def split(text: str,max_words: int=120,overlap: int=25):
        words=re.findall(r"\\S+",text)
        if not words:return []
        step=max(1,max_words-overlap); chunks=[]
        for i in range(0,len(words),step):
            chunks.append(" ".join(words[i:i+max_words]))
            if i+max_words>=len(words):break
        return chunks
    def add_text(self,text,source,page=None):
        self.passages.extend(Passage(x,source,page) for x in self.split(text))
    def ingest(self,folder):
        base=Path(folder)
        if not base.exists():raise FileNotFoundError(folder)
        for path in sorted(base.rglob("*")):
            if not path.is_file():continue
            if path.suffix.lower() in {".txt",".md"}:
                self.add_text(path.read_text(encoding="utf-8",errors="ignore"),str(path.relative_to(base)))
            elif path.suffix.lower()==".pdf":
                from pypdf import PdfReader
                for n,page in enumerate(PdfReader(str(path)).pages,1):
                    self.add_text(page.extract_text() or "",str(path.relative_to(base)),n)
        if not self.passages:raise ValueError("No readable text found")
        self.matrix=self.vectorizer.fit_transform([p.text for p in self.passages])
        return len(self.passages)
    def search(self,query,top_k=5):
        if self.matrix is None:raise RuntimeError("Index is empty")
        if not query.strip():raise ValueError("Query cannot be empty")
        scores=cosine_similarity(self.vectorizer.transform([query]),self.matrix).ravel()
        order=scores.argsort()[::-1][:max(1,top_k)]
        return [{**asdict(self.passages[i]),"score":round(float(scores[i]),4)} for i in order if scores[i]>0]
    def save(self,directory):
        p=Path(directory);p.mkdir(parents=True,exist_ok=True)
        joblib.dump({"passages":[asdict(x) for x in self.passages],"vectorizer":self.vectorizer,"matrix":self.matrix},p/"index.joblib")
    @classmethod
    def load(cls,directory):
        data=joblib.load(Path(directory)/"index.joblib");obj=cls()
        obj.passages=[Passage(**x) for x in data["passages"]];obj.vectorizer=data["vectorizer"];obj.matrix=data["matrix"]
        return obj
