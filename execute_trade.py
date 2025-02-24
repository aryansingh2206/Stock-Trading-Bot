import alpaca_trade_api as tradeapi
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import os

# Alpaca API credentials
API_KEY = "PK2MMSUPDEH0GFYK41Z9"
API_SECRET = "bSmBfwyhfjn4jbywZWVJH0RjkhrZc1WHf2KokuNH"
BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version="v2")

# Load trained models
models = {}
for symbol in ["AAPL", "TSLA", "MSFT"]:
    model_path = f"lstm_model_{symbol}.h5"
    if os.path.exists(model_path):
        models[symbol] = tf.keras.models.load_model(model_path)

# Load historical stock data from CSV
df = pd.read_csv("lstm_preprocessed_data.csv")

# Fetch historical data for a given stock symbol
def fetch_historical_data(symbol):
    stock_data = df[df["symbol"] == symbol]
    
    if stock_data.empty:
        raise ValueError(f"🚨 No historical data found for {symbol}.")
    
    if "close" not in stock_data.columns:
        raise ValueError(f"🚨 'close' column missing for {symbol}. Data: \n{stock_data.head()}")

    return stock_data["close"].values[-10:]  # Get last 10 closing prices

# Normalize data
def normalize_data(data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    return scaler.fit_transform(np.array(data).reshape(-1, 1)), scaler

# Check if a position exists for a stock
def get_position(symbol):
    try:
        position = api.get_position(symbol)
        return float(position.qty)
    except tradeapi.rest.APIError:
        return 0  # No position exists

# Place a trade order on Alpaca
def place_order(symbol, action, latest_price):
    try:
        position_size = get_position(symbol)

        # Prevent unnecessary sells
        if action == "sell" and position_size <= 0:
            print(f"⚠️ Skipping Sell: No existing position in {symbol}.")
            return

        # Close short before buying
        if action == "buy" and position_size < 0:
            print(f"🔄 Closing Short Position in {symbol} before Buying.")
            api.submit_order(
                symbol=symbol,
                qty=abs(position_size),  
                side="buy",
                type="market",
                time_in_force="gtc"
            )

        # Place new order
        api.submit_order(
            symbol=symbol,
            qty=1,  # Adjust quantity as needed
            side=action,
            type="market",
            time_in_force="gtc"
        )
        print(f"✅ {action.capitalize()} order placed for {symbol} at ${latest_price:.2f}")

    except Exception as e:
        print(f"🚨 Failed to place order for {symbol}: {e}")

# Make a trading decision
for symbol in models:
    print(f"\n🔍 Checking trade opportunity for {symbol}...")

    try:
        close_prices = fetch_historical_data(symbol)

        if len(close_prices) < 10:
            print(f"⚠️ Not enough valid historical data for {symbol}. Skipping...")
            continue

        # Normalize data
        scaled_data, scaler = normalize_data(close_prices)

        # Reshape input for LSTM
        X_input = np.array(scaled_data).reshape(1, 10, 1)

        # Predict next day's price
        predicted_scaled_price = models[symbol].predict(X_input)
        predicted_price = scaler.inverse_transform(predicted_scaled_price)[0][0]

        latest_price = close_prices[-1]  # Most recent actual closing price

        print(f"📊 Predicted Price: ${predicted_price:.2f}, Latest Price: ${latest_price:.2f}")

        # Trading logic
        if predicted_price > latest_price:
            print(f"📈 Buy Signal Detected for {symbol}")
            place_order(symbol, "buy", latest_price)

        elif predicted_price < latest_price:
            print(f"📉 Sell Signal Detected for {symbol}")
            place_order(symbol, "sell", latest_price)

        else:
            print(f"⏸️ No trade executed for {symbol}, predicted price is similar to latest price.")

    except Exception as e:
        print(f"🚨 Error processing {symbol}: {e}")
