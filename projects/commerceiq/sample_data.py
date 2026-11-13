from datetime import date,timedelta
import csv,math
from pathlib import Path
out=Path("data/daily_sales.csv");out.parent.mkdir(parents=True,exist_ok=True)
with out.open("w",newline="") as f:
    w=csv.writer(f);w.writerow(["date","sku","units_sold","unit_price","stock_on_hand","lead_time_days"])
    for j,sku in enumerate(["SKU-A","SKU-B","SKU-C"]):
        for i in range(150):
            units=max(0,round(18+j*7+2.5*math.sin(2*math.pi*i/7)+1.2*math.sin(2*math.pi*i/30)+((i*7+j*3)%5)-2))
            w.writerow([(date(2025,1,1)+timedelta(days=i)).isoformat(),sku,units,[1499,2499,899][j],[75,110,40][j],[5,8,3][j]])
print(f"Wrote demonstration data to {out}")
