import pandas as pd
import glob
from features.engineer import add_technical_indicators
from features.labeler import label_golden_cross_momentum
from model.train_model import train

def load_all_labeled_data(data_dir="data/raw"):
    all_dfs = []
    for file in glob.glob(f"{data_dir}/*.csv"):
        df = pd.read_csv(file, parse_dates=["timestamp"])
        df = df.sort_values("timestamp")
        df = add_technical_indicators(df)
        df = label_golden_cross_momentum(df)
        if not df.empty:
            all_dfs.append(df)
    return pd.concat(all_dfs, ignore_index=True)

if __name__ == "__main__":
    full_df = load_all_labeled_data()
    train(full_df)
