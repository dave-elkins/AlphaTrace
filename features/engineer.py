import pandas as pd
import ta

def add_technical_indicators(df):
    df = df.copy()
    df['SMA_50'] = df['Close'].rolling(50).mean()
    df['SMA_200'] = df['Close'].rolling(200).mean()
    df['SMA_ratio'] = df['SMA_50'] / df['SMA_200']
    df['momentum'] = df['Close'].pct_change(10)

    df['rsi'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    macd = ta.trend.MACD(df['Close'])
    df['macd_diff'] = macd.macd_diff()

    df['volatility'] = df['Close'].rolling(10).std()
    df['volume_avg'] = df['Volume'].rolling(20).mean()
    df['volume_ratio'] = df['Volume'] / df['volume_avg']
    
    return df.dropna()
