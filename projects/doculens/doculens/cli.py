import argparse
from .engine import DocumentIndex

def main():
    p=argparse.ArgumentParser(prog="doculens");s=p.add_subparsers(dest="cmd",required=True)
    i=s.add_parser("index");i.add_argument("folder");i.add_argument("--index-dir",default=".doculens_index")
    q=s.add_parser("search");q.add_argument("query");q.add_argument("--index-dir",default=".doculens_index");q.add_argument("--top-k",type=int,default=5)
    a=p.parse_args()
    if a.cmd=="index":
        x=DocumentIndex();n=x.ingest(a.folder);x.save(a.index_dir);print(f"Indexed {n} passages")
    else:
        for n,r in enumerate(DocumentIndex.load(a.index_dir).search(a.query,a.top_k),1):
            page=f", page {r['page']}" if r["page"] else ""
            print(f"{n}. [{r['source']}{page}] score={r['score']}\\n{r['text']}\\n")
if __name__=="__main__":main()
