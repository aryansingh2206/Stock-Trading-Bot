import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load historical stock data
df = pd.read_csv("historical_stock_data.csv")

# Ensure timestamp is in datetime format
df["timestamp"] = pd.to_datetime(df["date"])
df = df.sort_values(by=["symbol", "timestamp"])  # Sort data for each stock

# Normalize 'close' price for each stock separately
scalers = {}
scaled_data = []

for symbol in df["symbol"].unique():
    stock_data = df[df["symbol"] == symbol].copy()  # Avoid SettingWithCopyWarning
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    stock_data.loc[:, "scaled_close"] = scaler.fit_transform(stock_data[["close"]])  # Safe modification

    scalers[symbol] = scaler
    scaled_data.append(stock_data)

# Combine data back
df = pd.concat(scaled_data, ignore_index=True)

# Save preprocessed data
df.to_csv("lstm_preprocessed_data.csv", index=False)
print("✅ Data preprocessing complete. Ready for LSTM training.")
