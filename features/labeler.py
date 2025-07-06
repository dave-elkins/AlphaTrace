def label_golden_cross_momentum(df, forward_days=30):
    future_returns = df['Close'].shift(-forward_days) / df['Close'] - 1
    golden_cross = (df['SMA_50'] < df['SMA_200']) & (df['SMA_50'].shift(-forward_days) > df['SMA_200'].shift(-forward_days))
    df['target'] = ((golden_cross) & (future_returns > 0.05)).astype(int)
    return df.dropna()
