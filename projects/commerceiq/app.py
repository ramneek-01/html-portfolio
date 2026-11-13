import streamlit as st
import pandas as pd
from commerceiq.pipeline import load_sales,forecast,evaluate
st.set_page_config(page_title="CommerceIQ",layout="wide")
st.title("CommerceIQ | Demand & Inventory Intelligence")
st.caption("Forecasting demonstration. Validate with real historical data before operational use.")
up=st.file_uploader("Upload daily sales CSV",type="csv")
if up:
    raw=pd.read_csv(up);raw.to_csv("/tmp/commerceiq_upload.csv",index=False);path="/tmp/commerceiq_upload.csv"
else:path="data/daily_sales.csv"
try:
    df=load_sales(path);h=st.slider("Forecast horizon (days)",1,60,14)
    a,b,c=st.columns(3);a.metric("SKUs",df.sku.nunique());b.metric("History rows",len(df));c.metric("Latest date",str(df.date.max().date()))
    out=forecast(df,h);st.subheader("SKU forecasts");st.dataframe(out,use_container_width=True)
    summary=out.groupby("sku").agg(Forecast_units=("forecast_units","sum"),Reorder_point=("reorder_point","first"),Suggested_order=("suggested_reorder_units","first")).reset_index()
    st.subheader("Replenishment summary");st.dataframe(summary,use_container_width=True)
    st.download_button("Download forecast CSV",out.to_csv(index=False),"commerceiq_forecast.csv","text/csv")
    if len(df)>=60:
        with st.expander("Chronological holdout evaluation"):
            m=evaluate(df);st.write({k:v for k,v in m.items() if k!="cutoff"});st.caption(f"Holdout starts {m['cutoff']}.")
except Exception as e:st.error(str(e))
