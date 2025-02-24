from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd
from datetime import datetime, timedelta

# API Credentials
API_KEY = "PK2MMSUPDEH0GFYK41Z9"
API_SECRET = "bSmBfwyhfjn4jbywZWVJH0RjkhrZc1WHf2KokuNH"
BASE_URL = "https://paper-api.alpaca.markets"

# Initialize Alpaca API
api = REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# List of stocks to fetch
stock_symbols = ["AAPL", "TSLA", "MSFT"]

# Define date range
start_date = (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')

# Create an empty DataFrame to store all stock data
all_data = []

for stock_symbol in stock_symbols:
    try:
        print(f"🔍 Fetching data for {stock_symbol}...")

        # Fetch data
        barset = api.get_bars(stock_symbol, TimeFrame.Day, start=start_date, end=end_date, feed='iex').df

        if barset.empty:
            print(f"⚠️ No data from IEX for {stock_symbol}. Trying SIP feed...")
            barset = api.get_bars(stock_symbol, TimeFrame.Day, start=start_date, end=end_date, feed='sip').df

        if barset.empty:
            print(f"❌ No historical data available for {stock_symbol}. Skipping...")
            continue

        # Convert index (DatetimeIndex) to a column
        barset.reset_index(inplace=True)
        barset.rename(columns={"timestamp": "date"}, inplace=True)

        # Ensure required columns exist
        required_columns = ["date", "close", "high", "low", "open", "volume"]
        missing_columns = [col for col in required_columns if col not in barset.columns]

        if missing_columns:
            print(f"⚠️ Missing columns for {stock_symbol}: {missing_columns}. Skipping...")
            continue

        # Add stock symbol column
        barset["symbol"] = stock_symbol
        all_data.append(barset)

        print(f"✅ Fetched {len(barset)} rows for {stock_symbol}.")

    except Exception as e:
        print(f"🚨 Error fetching data for {stock_symbol}: {e}")

# Save data if available
if all_data:
    final_df = pd.concat(all_data)
    final_df.to_csv("historical_stock_data.csv", index=False)
    print("✅ Historical stock data saved to historical_stock_data.csv")
else:
    print("❌ No data fetched for any stocks.")
