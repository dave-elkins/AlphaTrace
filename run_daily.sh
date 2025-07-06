#!/bin/bash

echo "Running daily stock pipeline..."

source .env

# Pull/Update S&P 500 ticker list
python utils/get_sp500_polygon.py

# Download historical OHLCV data
python utils/download_polygon_data.py

# Append new daily bars to raw data
python utils/append_polygon_data.py

# Train model from local historical data
python model/train_from_csv.py

# Run predictions via Streamlit
streamlit run app/streamlit_app.py

