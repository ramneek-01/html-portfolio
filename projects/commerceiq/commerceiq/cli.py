import argparse
from pathlib import Path
from .pipeline import load_sales, forecast

def main():
    p=argparse.ArgumentParser(description="Forecast SKU demand and suggest replenishment.")
    p.add_argument("--data",required=True); p.add_argument("--horizon",type=int,default=14)
    p.add_argument("--output",default="outputs/forecast.csv")
    a=p.parse_args(); result=forecast(load_sales(a.data),a.horizon)
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); result.to_csv(out,index=False)
    print(f"Saved {len(result)} rows to {out}")
if __name__=="__main__": main()
