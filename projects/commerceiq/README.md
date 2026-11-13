# CommerceIQ — Demand Forecasting & Inventory Intelligence

A reproducible SKU-level demand forecasting workflow with an inventory decision-support layer.

## Capabilities
- Validates daily SKU sales data and engineers backward-looking lag, rolling, and calendar features.
- Compares a Random Forest regressor with a 7-day seasonal-naive baseline using a chronological holdout.
- Generates recursive short-horizon forecasts and replenishment suggestions using lead-time demand plus a configurable safety-stock buffer.
- Includes a Streamlit dashboard, CLI, CSV export, synthetic-data generator, and tests.

## Run
```bash
pip install -r requirements.txt
python sample_data.py
python -m commerceiq.cli --data data/daily_sales.csv --horizon 14 --output outputs/forecast.csv
streamlit run app.py
pytest
```

Schema: `date, sku, units_sold, unit_price, stock_on_hand, lead_time_days`.

The generated demonstration data is synthetic. Evaluate on real historical data with rolling-origin validation before using forecasts for operational decisions.
