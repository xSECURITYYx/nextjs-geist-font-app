# 🏆 Gold Trading Bot AI

Advanced Python-based trading bot that analyzes live and historical market data to generate trading signals for Gold Futures (GC=F). Uses technical indicators like EMA crossovers and RSI to provide Buy, Sell, or Hold recommendations with comprehensive risk management.

## 🚀 Features

- **Multi-Source Data**: Primary Alpha Vantage API with Yahoo Finance fallback
- **Advanced Technical Analysis**: EMA-9/21 crossovers, RSI, ATR, Support/Resistance
- **Smart Signal Generation**: Weighted composite signals with confidence scoring
- **Risk Management**: Dynamic stop-loss and take-profit calculations
- **Multiple Timeframes**: 1-day (5m), 2-day (15m), 5-day (30m) analysis
- **Interactive CLI**: User-friendly command-line interface
- **Backtest Support**: Historical performance analysis
- **Real-time Ready**: Prepared for live trading integration

## 📊 How It Works

### 1. Data Collection
- Fetches OHLCV data from Alpha Vantage (primary) or Yahoo Finance (fallback)
- Supports multiple timeframes with appropriate intervals
- Validates data quality before analysis

### 2. Technical Analysis
- **EMA Analysis**: 9-period and 21-period exponential moving averages
- **RSI Analysis**: 14-period Relative Strength Index
- **Volume Analysis**: Volume confirmation and anomaly detection
- **Support/Resistance**: Dynamic level calculation
- **ATR**: Average True Range for volatility measurement

### 3. Signal Generation
- Weighted composite scoring system
- Signal strength rating (1-10)
- Confidence scoring based on indicator consensus
- Multi-factor confirmation requirements

### 4. Risk Management
- ATR-based stop-loss calculation
- Dynamic take-profit levels
- Risk/reward ratio optimization
- Position sizing recommendations

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or download the project**
```bash
cd gold-trading-bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API (Optional but Recommended)**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your Alpha Vantage API key
# Get free API key at: https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

4. **Run the bot**
```bash
python main.py
```

## 🎮 Usage

### Interactive Mode (Default)
```bash
python main.py
```
Launches the interactive CLI with menu options for different analysis types.

### Quick Analysis
```bash
python main.py quick [timeframe]
```
- `python main.py quick 1d` - 1-day analysis with 5-minute candles
- `python main.py quick 2d` - 2-day analysis with 15-minute candles  
- `python main.py quick 5d` - 5-day analysis with 30-minute candles

### Multi-Timeframe Analysis
```bash
python main.py multi
```
Analyzes all timeframes and provides consensus signals.

### Backtest Mode
```bash
python main.py backtest [timeframe]
```
Runs historical analysis for backtesting purposes.

### System Information
```bash
python main.py info
```
Displays configuration and system status.

## 📈 Signal Interpretation

### Signal Types
- **🟢 BUY**: Bullish indicators align, potential upward movement
- **🔴 SELL**: Bearish indicators align, potential downward movement  
- **🟡 HOLD**: Mixed signals or insufficient confirmation

### Signal Strength (1-10)
- **8-10**: Very strong signal with high probability
- **6-7**: Strong signal with good probability
- **4-5**: Moderate signal, proceed with caution
- **1-3**: Weak signal, consider waiting

### Confidence Score (1-10)
- **8-10**: High confidence, multiple indicators agree
- **6-7**: Good confidence, most indicators agree
- **4-5**: Moderate confidence, mixed indicators
- **1-3**: Low confidence, conflicting signals

## ⚙️ Configuration

### Environment Variables (.env)
```bash
# API Configuration
ALPHA_VANTAGE_API_KEY=your_api_key_here

# Trading Configuration  
DEFAULT_SYMBOL=GC=F
DEFAULT_TIMEFRAME=1d
TRADING_MODE=BACKTEST

# Risk Management
DEFAULT_RISK_PERCENT=2.0
MAX_POSITION_SIZE=10000
```

### Technical Indicator Settings
- **EMA Periods**: 9 (short), 21 (long)
- **RSI Period**: 14
- **RSI Levels**: Oversold 30, Overbought 70
- **ATR Period**: 14
- **Stop Loss**: 2x ATR
- **Take Profit**: 2:1 risk/reward ratio

## 📊 Sample Output

```
🔍 GOLD TRADING ANALYSIS - 2024-01-15 14:30:25
================================================================================

📈 CURRENT MARKET STATUS:
   Gold Price (GC=F): $2,045.30
   Analysis Time: 14:30:25 UTC

🎯 TRADING SIGNAL:
   🟢 Signal: BUY
   📊 Strength: 7.2/10
   🎯 Confidence: 8.1/10
   💡 Recommendation: STRONG BUY - High confidence signal (Score: 8.1/10)

🔧 TECHNICAL ANALYSIS BREAKDOWN:
   📈 EMA Analysis:
      • Signal: BUY (Strength: 6.8)
      • Trend: BULLISH (Strength: 7.2)
      • EMA-9 crossed above EMA-21

   📊 RSI Analysis:
      • Signal: BUY (Strength: 5.4)
      • Current RSI: 45.2 (NEUTRAL)
      • Momentum: +8.3

⚠️  RISK MANAGEMENT:
   🛑 Stop Loss: $2,031.45 (-0.7%)
   🎯 Take Profit: $2,072.90 (+1.3%)
   💰 Risk Amount: $13.85
   🏆 Reward Amount: $27.60
   ⚖️  Risk/Reward Ratio: 1:2.0
```

## 🔧 Technical Details

### Data Sources
1. **Alpha Vantage** (Primary)
   - Professional-grade data
   - Real-time updates
   - 5 requests/minute free tier
   - Requires API key

2. **Yahoo Finance** (Fallback)
   - Free, no API key required
   - 15-20 minute delay
   - Good for development/testing
   - Rate limiting protection

### Architecture
```
main.py
├── src/
│   ├── config.py          # Configuration management
│   ├── data_fetcher.py    # Multi-source data fetching
│   ├── indicators.py      # Technical indicator calculations
│   ├── signal_generator.py # Signal analysis and generation
│   ├── cli.py            # Command-line interface
│   └── trading_bot.py    # Main bot orchestrator
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README.md            # This file
```

## 🚨 Important Disclaimers

### Educational Purpose Only
This bot is designed for **educational and research purposes only**. It is not financial advice and should not be used as the sole basis for trading decisions.

### Risk Warning
- Trading gold futures involves substantial risk
- Past performance does not guarantee future results
- Always do your own research and risk assessment
- Never risk more than you can afford to lose
- Consider consulting with a financial advisor

### No Warranty
This software is provided "as is" without any warranty. The authors are not responsible for any trading losses or damages.

## 🔮 Future Enhancements

- [ ] Live broker integration (Alpaca, Interactive Brokers)
- [ ] Web dashboard interface
- [ ] Email/SMS notifications
- [ ] Machine learning model integration
- [ ] Portfolio management features
- [ ] Advanced backtesting with performance metrics
- [ ] Real-time streaming data
- [ ] Multiple asset support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions or support:
- Create an issue on the project repository
- Check the documentation in this README
- Review the code comments for technical details

---

**Happy Trading! 🏆📈**

*Remember: The best traders combine technical analysis with fundamental analysis and proper risk management.*
