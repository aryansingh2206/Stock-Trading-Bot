import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import numpy as np
import pandas as pd

# Suppress unnecessary TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Check GPU availability
print("🔍 Checking GPU availability...")
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"✅ GPU detected: {gpus[0]}")
else:
    print("⚠️ No GPU detected, running on CPU (training may be slower).")

# Load preprocessed data
df = pd.read_csv("preprocessed_stock_data.csv")

# Function to create sequences for LSTM
def create_sequences(data, seq_length=10):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

# Train a model for each stock
models = {}
seq_length = 10  # Using 10 days of data to predict the next day

for symbol in df["symbol"].unique():
    print(f"\n📊 Training LSTM model for {symbol}...")

    stock_data = df[df["symbol"] == symbol]["close"].values

    if len(stock_data) <= seq_length:
        print(f"⚠️ Not enough data for {symbol}. Skipping.")
        continue

    X, y = create_sequences(stock_data, seq_length)

    # Reshape for LSTM input
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # Define LSTM model
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(seq_length, 1)),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train model with verbose logging
    model.fit(X, y, epochs=20, batch_size=16, verbose=1)

    # Save model
    model.save(f"lstm_model_{symbol}.h5")
    models[symbol] = model

    print(f"✅ Model trained and saved for {symbol}")

print("\n🎉 All models trained successfully!")
