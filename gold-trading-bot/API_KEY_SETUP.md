# 🔑 Alpha Vantage API Key Setup Guide

## Quick Setup (5 minutes)

### Step 1: Get Your Free API Key
1. **Visit**: https://www.alphavantage.co/support/#api-key
2. **Click**: "Get your free API key today"
3. **Fill out the form**:
   - First Name: Your name
   - Last Name: Your last name
   - Email: Your email address
   - Organization: "Personal" or "Individual"
4. **Click**: "GET FREE API KEY"
5. **Copy your API key** (looks like: `ABCD1234EFGH5678`)

### Step 2: Configure the Bot
```bash
# Navigate to bot directory
cd gold-trading-bot

# Copy environment template
cp .env.example .env

# Edit the .env file and replace 'your_api_key_here' with your actual key
# Example: ALPHA_VANTAGE_API_KEY=ABCD1234EFGH5678
```

### Step 3: Test with Real Data
```bash
python main.py quick 1d
```

## 📊 What You Get with Alpha Vantage

### Free Tier Benefits:
- ✅ **25 API requests per day** (perfect for this bot)
- ✅ **5 requests per minute**
- ✅ **Real-time market data** (vs 15-20 min delay from Yahoo)
- ✅ **Professional data quality**
- ✅ **Reliable uptime**
- ✅ **Official API support**

### Data Quality Comparison:
| Feature | Alpha Vantage | Yahoo Finance | Demo Data |
|---------|---------------|---------------|-----------|
| Data Delay | Real-time | 15-20 minutes | N/A |
| Reliability | High | Medium | High |
| API Support | Official | Unofficial | N/A |
| Rate Limits | 25/day | Variable | Unlimited |
| Data Quality | Professional | Consumer | Simulated |

## 🛠️ Configuration Options

### Basic .env Setup:
```bash
# Required: Your Alpha Vantage API key
ALPHA_VANTAGE_API_KEY=your_actual_api_key_here

# Optional: Trading configuration
DEFAULT_SYMBOL=GLD
DEFAULT_TIMEFRAME=1d
TRADING_MODE=BACKTEST
DEFAULT_RISK_PERCENT=2.0
MAX_POSITION_SIZE=10000
```

### Advanced Configuration:
You can modify `src/config.py` for:
- Technical indicator periods (EMA, RSI)
- Risk management parameters
- Signal weighting factors
- Display colors and formatting

## 🚀 Usage After Setup

### With API Key (Real Data):
```bash
python main.py quick 1d    # Real 1-day gold analysis
python main.py multi       # Multi-timeframe real analysis
```

### Without API Key (Demo Data):
The bot automatically falls back to realistic demo data if:
- No API key is configured
- API key is invalid
- API rate limits are exceeded
- Network issues occur

## 🔒 Security Best Practices

1. **Keep your API key private** - don't share it publicly
2. **Don't commit .env to version control** (already in .gitignore)
3. **Regenerate key if compromised** (free on Alpha Vantage website)
4. **Use environment variables** in production deployments

## 💡 Pro Tips

1. **Free tier is sufficient** for this bot's usage patterns
2. **Bot works offline** with demo data for testing
3. **Upgrade to paid tier** only if you need more than 25 requests/day
4. **Monitor your usage** on the Alpha Vantage dashboard

## 🆘 Troubleshooting

### Common Issues:
- **"No API key"**: Check .env file exists and has correct key
- **"Rate limit exceeded"**: Wait or use demo mode
- **"Invalid API key"**: Verify key is correct and active
- **"Network error"**: Check internet connection

### Test Commands:
```bash
# Test API key validity
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('ALPHA_VANTAGE_API_KEY'))"

# Force demo mode for testing
python main.py quick 1d  # Will fall back to demo if API fails
```

## 📞 Support

- **Alpha Vantage Support**: https://www.alphavantage.co/support/
- **Bot Documentation**: See README.md
- **Demo Results**: See DEMO_RESULTS.md

---

**Ready to get real market data? Get your free API key now!**
🔗 https://www.alphavantage.co/support/#api-key
