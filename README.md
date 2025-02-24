## 📈 Stock Trading Bot 🚀  

An **AI-powered automated stock trading bot** that uses **LSTM neural networks** to predict stock prices and execute trades using the **Alpaca API**.  

---

### ✨ Features  
✅ **Live Trading & Paper Trading** – Supports both real and simulated trading with **Alpaca**.  
✅ **AI-Powered Predictions** – Uses **LSTM (Long Short-Term Memory) models** to predict stock prices.  
✅ **Automated Trade Execution** – Places buy/sell orders based on predictions and trading logic.  
✅ **Stock Market Data Processing** – Fetches and normalizes historical stock data for training.  
✅ **Risk Management** – Avoids wash trades, handles existing positions, and prevents unnecessary orders.  

---

### 📜 How It Works  
1️⃣ **Fetch Historical Data** – Retrieves past stock prices to use as input for prediction.  
2️⃣ **Preprocess Data** – Normalizes and reshapes data for LSTM model training.  
3️⃣ **Train & Load LSTM Model** – Uses TensorFlow/Keras to predict future stock prices.  
4️⃣ **Make Trade Decisions** – Determines whether to buy/sell based on predicted vs. actual prices.  
5️⃣ **Execute Trades** – Uses the Alpaca API to place market orders.  

---

### 🛠️ Tech Stack  
- **Programming Language**: Python  
- **AI/ML Framework**: TensorFlow, Keras, Scikit-Learn  
- **Data Handling**: Pandas, NumPy  
- **Stock Trading API**: Alpaca  
- **Visualization**: Matplotlib, Seaborn  

---

### 🚀 Installation & Setup  

#### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/aryansingh2206/Stock-Trading-Bot.git
cd Stock-Trading-Bot
```

#### **2️⃣ Create Virtual Environment**  
```bash
python -m venv trading-bot-env
source trading-bot-env/bin/activate  # Mac/Linux
trading-bot-env\Scripts\activate     # Windows
```

#### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

#### **4️⃣ Set Up API Keys**  
Replace the placeholders in `config.py` with your **Alpaca API Key & Secret**:  
```python
API_KEY = "your_alpaca_api_key"
API_SECRET = "your_alpaca_secret_key"
BASE_URL = "https://paper-api.alpaca.markets"  # Use "https://api.alpaca.markets" for live trading
```

#### **5️⃣ Train the LSTM Model (Optional)**
To train a new AI model, run:  
```bash
python train_model.py
```

#### **6️⃣ Start the Trading Bot**  
```bash
python execute_trade.py
```

---

### 🏆 Example Output  
```
🔍 Checking trade opportunity for AAPL...
📊 Predicted Price: $239.40, Latest Price: $245.68
📉 Sell Signal Detected for AAPL
⚠️ Skipping Sell: No existing position in AAPL.

🔍 Checking trade opportunity for TSLA...
📊 Predicted Price: $345.17, Latest Price: $337.66
📈 Buy Signal Detected for TSLA
✅ Buy order placed for TSLA at $337.66
```

---

### 🔥 Future Improvements  
🚀 **Enhance Model Accuracy** – Fine-tune LSTM hyperparameters for better predictions.  
📊 **Real-Time Data Streaming** – Implement WebSocket for live price tracking.  
💡 **Multi-Stock Portfolio Management** – Support for diversified trading strategies.  
🔔 **Alerts & Notifications** – Send buy/sell alerts via email, Discord, or Telegram.  

---

### 🤝 Contributing  
Feel free to submit pull requests or suggest improvements! 🚀  

1. **Fork the repo**  
2. **Create a new branch** (`feature-branch`)  
3. **Commit your changes** (`git commit -m "Added feature XYZ"`)  
4. **Push to your branch** (`git push origin feature-branch`)  
5. **Submit a pull request**  

---
### Screenshots
![image](https://github.com/user-attachments/assets/d6bd97f4-daad-4707-9095-966cd7157f8c)

### 🌟 Support  
💬 Have questions? Open an issue or reach out to me on **GitHub Discussions**! 😊  

---
