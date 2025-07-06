import joblib

def predict(df):
    model = joblib.load('model/lgbm_model.pkl')
    features = ['SMA_ratio', 'momentum', 'rsi', 'macd_diff', 'volatility', 'volume_ratio']
    df['probability'] = model.predict_proba(df[features])[:, 1]
    return df[df['probability'] > 0.8]
