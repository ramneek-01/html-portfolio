# CommerceIQ — Demand Forecasting & Inventory Intelligence

A SKU-level demand forecasting workflow with an inventory decision-support layer.

## Features
- Daily sales validation and lag, rolling, and calendar features.
- Random Forest forecasts compared with a 7-day seasonal-naive baseline using a chronological holdout.
- Short-horizon forecasts and replenishment suggestions based on lead-time demand and safety stock.
- Streamlit dashboard, command-line interface, CSV export, synthetic-data generator, and tests.

## Run
```bash
pip install -r requirements.txt
python sample_data.py
python -m commerceiq.cli --data data/daily_sales.csv --horizon 14 --output outputs/forecast.csv
streamlit run app.py
pytest
```

Expected columns: `date, sku, units_sold, unit_price, stock_on_hand, lead_time_days`.

The included data is synthetic. Validate the model against real historical data before relying on forecasts for purchasing decisions.
