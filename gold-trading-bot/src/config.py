import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the Gold Trading Bot"""
    
    # API Configuration
    ALPHA_VANTAGE_API_KEY = os.getenv('PKU6TCDSOZ3CIDXKZ7NM', '')
    ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co/query'
    
    # Trading Configuration
    DEFAULT_SYMBOL = 'GLD'   # Gold ETF (more reliable than futures)
    YAHOO_SYMBOL = 'GLD'     # Yahoo Finance symbol
    AV_SYMBOL = 'GLD'        # Alpha Vantage uses GLD ETF as proxy for gold
    
    # Timeframe Mappings
    TIMEFRAME_MAPPING = {
        '1d': {
            'yahoo_interval': '5m',
            'yahoo_period': '1d',
            'av_interval': '5min',
            'description': '1-day chart with 5-minute candles'
        },
        '2d': {
            'yahoo_interval': '15m',
            'yahoo_period': '2d',
            'av_interval': '15min',
            'description': '2-day chart with 15-minute candles'
        },
        '5d': {
            'yahoo_interval': '30m',
            'yahoo_period': '5d',
            'av_interval': '30min',
            'description': '5-day (weekly) chart with 30-minute candles'
        }
    }
    
    # Technical Indicator Settings
    EMA_SHORT_PERIOD = 9
    EMA_LONG_PERIOD = 21
    RSI_PERIOD = 14
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30
    
    # Signal Scoring Weights
    SIGNAL_WEIGHTS = {
        'ema_crossover': 0.4,
        'rsi_confirmation': 0.3,
        'volume_confirmation': 0.2,
        'trend_strength': 0.1
    }
    
    # Risk Management
    DEFAULT_RISK_PERCENT = float(os.getenv('DEFAULT_RISK_PERCENT', 2.0))
    MAX_POSITION_SIZE = float(os.getenv('MAX_POSITION_SIZE', 10000))
    STOP_LOSS_ATR_MULTIPLIER = 2.0
    TAKE_PROFIT_RATIO = 2.0  # Risk:Reward ratio
    
    # Trading Modes
    TRADING_MODE = os.getenv('TRADING_MODE', 'BACKTEST')  # BACKTEST or REALTIME
    
    # Display Settings
    COLORS = {
        'BUY': '\033[92m',      # Green
        'SELL': '\033[91m',     # Red
        'HOLD': '\033[93m',     # Yellow
        'INFO': '\033[94m',     # Blue
        'RESET': '\033[0m'      # Reset
    }
