import pandas as pd
import glob
from features.engineer import add_technical_indicators
from features.labeler import label_golden_cross_momentum

def prepare_backtest_input(data_dir="data/raw", output_file="data/backtest_dataset.csv"):
    all_dfs = []
    for path in glob.glob(f"{data_dir}/*.csv"):
        ticker = os.path.basename(path).replace(".csv", "")
        df = pd.read_csv(path, parse_dates=["timestamp"])
        df["Ticker"] = ticker
        df = df.sort_values("timestamp")
        df = add_technical_indicators(df)
        df = label_golden_cross_momentum(df)
        all_dfs.append(df)
    combined = pd.concat(all_dfs, ignore_index=True)
    combined.to_csv(output_file, index=False)
    print(f"Saved backtest dataset to {output_file}")

if __name__ == "__main__":
    prepare_backtest_input()
