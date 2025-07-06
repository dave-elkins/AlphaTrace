import lightgbm as lgb
from sklearn.model_selection import train_test_split
import joblib

def train(df):
    features = ['SMA_ratio', 'momentum', 'rsi', 'macd_diff', 'volatility', 'volume_ratio']
    X = df[features]
    y = df['target']

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, stratify=y)

    model = lgb.LGBMClassifier()
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], early_stopping_rounds=10, verbose=False)

    joblib.dump(model, 'model/lgbm_model.pkl')
    print("Model trained and saved.")
