import argparse,json,sys
from .analyzer import analyze_path

def main():
    p=argparse.ArgumentParser(description="Static analysis for Python source")
    p.add_argument("path");p.add_argument("--format",choices=["text","json"],default="text")
    p.add_argument("--max-complexity",type=int,default=10);p.add_argument("--fail-on-findings",action="store_true")
    a=p.parse_args();reports=analyze_path(a.path)
    if a.format=="json":print(json.dumps(reports,indent=2))
    else:
        for r in reports:
            print(f"\\n{r['file']} | {r['lines']} lines | {r['function_count']} functions")
            for f in r["functions"]:print(f"  {f['name']}:{f['line']} complexity={f['complexity']} length={f['lines']}")
            for f in r["findings"]:print(f"  [{f['severity'].upper()}] {f['rule']}:{f['line']} {f['message']}")
    findings=[f for r in reports for f in r["findings"]]
    high_complexity=any(f["complexity"]>a.max_complexity for r in reports for f in r["functions"])
    if a.fail_on_findings and (findings or high_complexity):sys.exit(1)
if __name__=="__main__":main()
