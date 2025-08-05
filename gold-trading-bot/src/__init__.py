"""
Gold Trading Bot AI - Source Package
Advanced Technical Analysis for Gold Futures Trading
"""

__version__ = "1.0.0"
__author__ = "Gold Trading Bot AI"
__description__ = "Advanced Python-based gold trading bot with technical analysis"

# Package imports for easier access
from config import Config
from data_fetcher import DataFetcher
from indicators import TechnicalIndicators
from signal_generator import SignalGenerator
from trading_bot import GoldTradingBot
from cli import TradingBotCLI

__all__ = [
    'Config',
    'DataFetcher', 
    'TechnicalIndicators',
    'SignalGenerator',
    'GoldTradingBot',
    'TradingBotCLI'
]
