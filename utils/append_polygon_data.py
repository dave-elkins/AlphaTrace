import os
import pandas as pd
import requests
from datetime import datetime, timedelta
import time

API_KEY = os.getenv("POLYGON_API_KEY")
BASE_URL = "https://api.polygon.io/v2/aggs/ticker"
DATA_DIR = "data/raw"

def fetch_latest_bar(ticker, from_date, to_date):
    url = f"{BASE_URL}/{ticker}/range/1/day/{from_date}/{to_date}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 5000,
        "apiKey": API_KEY
    }
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json().get("results", [])
        if not data:
            return None
        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df["t"], unit="ms")
        df = df.rename(columns={
            "o": "Open", "h": "High", "l": "Low", "c": "Close", "v": "Volume"
        })
        return df[["timestamp", "Open", "High", "Low", "Close", "Volume"]]
    return None

def append_latest_data():
    for fname in os.listdir(DATA_DIR):
        if not fname.endswith(".csv"):
            continue
        ticker = fname.replace(".csv", "")
        df = pd.read_csv(f"{DATA_DIR}/{fname}", parse_dates=["timestamp"])
        last_date = df["timestamp"].max().date()
        today = datetime.now().date()

        if last_date >= today:
            continue

        print(f"Updating {ticker} from {last_date + timedelta(days=1)} to {today}...")
        new_data = fetch_latest_bar(ticker, last_date + timedelta(days=1), today)
        if new_data is not None:
            combined = pd.concat([df, new_data], ignore_index=True)
            combined = combined.drop_duplicates(subset=["timestamp"]).sort_values("timestamp")
            combined.to_csv(f"{DATA_DIR}/{ticker}.csv", index=False)
        time.sleep(0.5)

if __name__ == "__main__":
    append_latest_data()
