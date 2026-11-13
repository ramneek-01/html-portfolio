from __future__ import annotations
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

REQUIRED = {"date", "sku", "units_sold", "unit_price", "stock_on_hand", "lead_time_days"}
FEATURES = ["lag_1", "lag_7", "lag_14", "lag_28", "rolling_mean_7", "rolling_std_7", "day_of_week", "day_of_year", "month", "unit_price"]

def load_sales(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    df["date"] = pd.to_datetime(df["date"], errors="raise")
    for col in REQUIRED - {"date", "sku"}:
        df[col] = pd.to_numeric(df[col], errors="raise")
    if (df[["units_sold", "stock_on_hand", "lead_time_days"]] < 0).any().any():
        raise ValueError("Sales, stock, and lead time must be non-negative")
    return df.sort_values(["sku", "date"]).reset_index(drop=True)

def add_features(frame: pd.DataFrame) -> pd.DataFrame:
    df = frame.sort_values(["sku", "date"]).copy()
    g = df.groupby("sku", sort=False)["units_sold"]
    for lag in (1, 7, 14, 28):
        df[f"lag_{lag}"] = g.shift(lag)
    shifted = g.shift(1)
    df["rolling_mean_7"] = shifted.groupby(df["sku"]).transform(lambda s: s.rolling(7, min_periods=3).mean())
    df["rolling_std_7"] = shifted.groupby(df["sku"]).transform(lambda s: s.rolling(7, min_periods=3).std()).fillna(0)
    df["day_of_week"] = df.date.dt.dayofweek
    df["day_of_year"] = df.date.dt.dayofyear
    df["month"] = df.date.dt.month
    return df

def evaluate(frame: pd.DataFrame, test_days: int = 28) -> dict:
    if test_days < 1: raise ValueError("test_days must be positive")
    data = add_features(frame).dropna(subset=FEATURES)
    if data.empty: raise ValueError("Not enough history; 29 daily observations per SKU are recommended")
    cutoff = data.date.max() - pd.Timedelta(days=test_days - 1)
    train, test = data[data.date < cutoff], data[data.date >= cutoff]
    if train.empty or test.empty: raise ValueError("Insufficient data for chronological split")
    model = RandomForestRegressor(n_estimators=250, min_samples_leaf=2, random_state=42, n_jobs=-1)
    model.fit(train[FEATURES], train.units_sold)
    pred = np.maximum(0, model.predict(test[FEATURES]))
    return {"mae": float(mean_absolute_error(test.units_sold, pred)),
            "rmse": float(mean_squared_error(test.units_sold, pred) ** .5),
            "seasonal_naive_mae": float(mean_absolute_error(test.units_sold, test.lag_7)),
            "train_rows": len(train), "test_rows": len(test), "cutoff": str(cutoff.date())}

def forecast(frame: pd.DataFrame, horizon: int = 14) -> pd.DataFrame:
    if not 1 <= horizon <= 90: raise ValueError("horizon must be between 1 and 90")
    feat = add_features(frame)
    train = feat.dropna(subset=FEATURES)
    if train.empty: raise ValueError("Not enough history to build lag features")
    model = RandomForestRegressor(n_estimators=250, min_samples_leaf=2, random_state=42, n_jobs=-1)
    model.fit(train[FEATURES], train.units_sold)
    rows = []
    for sku, hist in frame.sort_values("date").groupby("sku"):
        hist = hist.sort_values("date").copy()
        last = hist.iloc[-1]
        for step in range(1, horizon + 1):
            d = last.date + pd.Timedelta(days=step)
            vals = hist.units_sold.to_numpy(float)
            lag = lambda n: float(vals[-n]) if len(vals) >= n else float(np.mean(vals))
            recent = vals[-7:]
            x = pd.DataFrame([{"lag_1":lag(1),"lag_7":lag(7),"lag_14":lag(14),"lag_28":lag(28),
                "rolling_mean_7":float(np.mean(recent)),"rolling_std_7":float(np.std(recent)),
                "day_of_week":d.dayofweek,"day_of_year":d.dayofyear,"month":d.month,"unit_price":float(last.unit_price)}])
            y = max(0.0, float(model.predict(x[FEATURES])[0]))
            rows.append({"date":d,"sku":sku,"forecast_units":round(y,2),
                         "stock_on_hand":float(last.stock_on_hand),"lead_time_days":int(last.lead_time_days)})
            hist = pd.concat([hist, pd.DataFrame([{"date":d,"sku":sku,"units_sold":y,
                "unit_price":last.unit_price,"stock_on_hand":last.stock_on_hand,"lead_time_days":last.lead_time_days}])], ignore_index=True)
    out = pd.DataFrame(rows)
    summary = out.groupby("sku").agg(stock=("stock_on_hand","first"), lead=("lead_time_days","first")).reset_index()
    lead = out[out.groupby("sku").cumcount() < out.sku.map(summary.set_index("sku").lead)]
    demand = lead.groupby("sku").forecast_units.sum().rename("lead_demand")
    summary = summary.merge(demand, on="sku", how="left").fillna({"lead_demand":0})
    summary["reorder_point"] = (summary.lead_demand * 1.2).round()
    summary["suggested_reorder_units"] = (summary.reorder_point - summary.stock).clip(lower=0)
    return out.merge(summary[["sku","reorder_point","suggested_reorder_units"]], on="sku")
