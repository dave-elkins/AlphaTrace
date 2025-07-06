import requests
import pandas as pd
import os

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")  # Make sure this is set

def get_all_us_common_stocks():
    print("Fetching all US common stocks from Polygon...")
    url = "https://api.polygon.io/v3/reference/tickers"
    params = {
        "market": "stocks",
        "active": "true",
        "type": "CS",  # Common stock
        "limit": 1000,
        "apiKey": POLYGON_API_KEY
    }

    tickers = []
    while True:
        response = requests.get(url, params=params)
        data = response.json()
        tickers.extend([item['ticker'] for item in data.get("results", [])])
        if "next_url" in data:
            url = data["next_url"] + f"&apiKey={POLYGON_API_KEY}"
            params = None  # Polygon requires you to include the key directly in the next_url
        else:
            break

    return set(tickers)


def get_sp500_from_wikipedia():
    print("Scraping S&P 500 tickers from Wikipedia...")
    sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(sp500_url)
    tickers = tables[0]['Symbol'].tolist()
    tickers = [t.replace(".", "-") for t in tickers]  # e.g., BRK.B → BRK-B
    return set(tickers)


def get_valid_sp500_tickers():
    polygon_tickers = get_all_us_common_stocks()
    sp500_tickers = get_sp500_from_wikipedia()
    valid = sp500_tickers.intersection(polygon_tickers)
    print(f"Found {len(valid)} valid S&P 500 tickers from Polygon.")
    return sorted(valid)


if __name__ == "__main__":
    tickers = get_valid_sp500_tickers()
    with open("data/sp500_polygon_valid.txt", "w") as f:
        for t in tickers:
            f.write(t + "\n")
