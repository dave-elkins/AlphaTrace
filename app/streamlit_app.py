import streamlit as st
import pandas as pd
from model.predictor import predict
from utils.fetch_data import fetch_data
from features.engineer import add_technical_indicators

st.title("📈 Golden Cross Predictor")

tickers = st.multiselect("Select stocks", ["AAPL", "MSFT", "NVDA", "TSLA", "GOOG", "AMZN"])
results = []

for ticker in tickers:
    df = fetch_data(ticker)
    df = add_technical_indicators(df)
    df = predict(df)
    if not df.empty:
        df['Ticker'] = ticker
        results.append(df[['Ticker', 'Close', 'probability']].iloc[-1])

if results:
    st.write(pd.DataFrame(results))
else:
    st.info("No high-probability candidates today.")
