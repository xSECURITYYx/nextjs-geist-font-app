#!/usr/bin/env python3
"""
Gold Trading Bot AI - Main Entry Point
Advanced Technical Analysis for Gold Futures Trading

Usage:
    python main.py                    # Interactive mode
    python main.py quick [timeframe]  # Quick analysis (1d, 2d, 5d)
    python main.py multi              # Multi-timeframe analysis
    python main.py backtest [timeframe] # Backtest mode
    python main.py info               # System information

Examples:
    python main.py                    # Start interactive CLI
    python main.py quick 1d           # Quick 1-day analysis
    python main.py multi              # Analyze all timeframes
    python main.py backtest 5d        # Backtest with 5-day data
"""

import sys
import os

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Import and run the trading bot
from trading_bot import main

if __name__ == "__main__":
    main()
