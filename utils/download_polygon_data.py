import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

API_KEY = os.getenv("POLYGON_API_KEY")
BASE_URL = "https://api.polygon.io/v2/aggs/ticker"

OUTPUT_DIR = "data/raw"
TICKERS_FILE = "data/sp500_polygon_valid.txt"

def download_polygon_agg(ticker, timespan="day", multiplier=1, from_days_ago=365):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=from_days_ago)

    url = f"{BASE_URL}/{ticker}/range/{multiplier}/{timespan}/{start_date.date()}/{end_date.date()}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 50000,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error fetching {ticker}: {response.status_code}")
        return None

    results = response.json().get("results", [])
    if not results:
        return None

    df = pd.DataFrame(results)
    df["timestamp"] = pd.to_datetime(df["t"], unit="ms")
    df = df.rename(columns={
        "o": "Open",
        "h": "High",
        "l": "Low",
        "c": "Close",
        "v": "Volume"
    })
    return df[["timestamp", "Open", "High", "Low", "Close", "Volume"]]


def download_all_tickers():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(TICKERS_FILE, "r") as f:
        tickers = [line.strip() for line in f.readlines()]

    for i, ticker in enumerate(tickers):
        file_path = f"{OUTPUT_DIR}/{ticker}.csv"
        if os.path.exists(file_path):
            print(f"[{i+1}/{len(tickers)}] Skipping {ticker}, already exists.")
            continue

        print(f"[{i+1}/{len(tickers)}] Downloading {ticker}...")
        df = download_polygon_agg(ticker)
        if df is not None:
            df.to_csv(file_path, index=False)
        else:
            print(f"  ⚠️ No data returned for {ticker}")
        time.sleep(0.5)  # Respect API rate limits


if __name__ == "__main__":
    download_all_tickers()
