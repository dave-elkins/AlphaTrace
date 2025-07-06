import yfinance as yf
import pandas as pd

def fetch_data(ticker, period="1y", interval="1d"):
    df = yf.download(ticker, period=period, interval=interval)
    df = df.dropna()
    df['Ticker'] = ticker
    return df
