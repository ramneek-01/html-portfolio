import pandas as pd
import pytest
from commerceiq.pipeline import add_features,forecast,load_sales

def sample(n=80):
    return pd.DataFrame([{"date":d,"sku":"SKU-A","units_sold":10+i%7,"unit_price":99.0,"stock_on_hand":20,"lead_time_days":5} for i,d in enumerate(pd.date_range("2025-01-01",periods=n))])

def test_features_are_backward_looking():
    d=add_features(sample());assert d.iloc[35].lag_1==d.iloc[34].units_sold;assert d.iloc[35].lag_7==d.iloc[28].units_sold

def test_forecast_shape_and_nonnegative():
    out=forecast(sample(),7);assert len(out)==7;assert (out.forecast_units>=0).all();assert "suggested_reorder_units" in out

def test_rejects_missing_columns(tmp_path):
    p=tmp_path/"bad.csv";pd.DataFrame({"date":["2025-01-01"]}).to_csv(p,index=False)
    with pytest.raises(ValueError):load_sales(str(p))
