import yfinance as yf
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from typing import Optional, Dict, Any
from config import Config
from demo_data import DemoDataGenerator

class DataFetcher:
    """Handles data fetching from multiple sources with fallback support"""
    
    def __init__(self, demo_mode: bool = False):
        self.config = Config()
        self.last_request_time = 0
        self.min_request_interval = 12  # 12 seconds between Alpha Vantage requests (5 per minute limit)
        self.demo_mode = demo_mode
        self.demo_generator = DemoDataGenerator() if demo_mode else None
    
    def get_market_data(self, timeframe: str = '1d') -> Optional[pd.DataFrame]:
        """
        Fetch market data with Alpha Vantage primary and Yahoo Finance fallback
        
        Args:
            timeframe: Chart timeframe ('1d', '2d', '5d')
            
        Returns:
            DataFrame with OHLCV data or None if failed
        """
        print(f"📊 Fetching gold market data for {timeframe} timeframe...")
        
        # Use demo data if in demo mode
        if self.demo_mode:
            print("🎭 Using demo data for testing...")
            data = self.demo_generator.generate_demo_data(timeframe)
            print(f"✅ Demo data generated successfully ({len(data)} data points)")
            return data
        
        # Try Alpha Vantage first if API key is available
        if self.config.ALPHA_VANTAGE_API_KEY:
            print("🔄 Attempting Alpha Vantage data fetch...")
            data = self._fetch_alpha_vantage_data(timeframe)
            if data is not None:
                print("✅ Alpha Vantage data fetch successful")
                return data
            else:
                print("⚠️  Alpha Vantage failed, falling back to Yahoo Finance...")
        else:
            print("⚠️  No Alpha Vantage API key, using Yahoo Finance...")
        
        # Fallback to Yahoo Finance
        print("🔄 Fetching from Yahoo Finance...")
        data = self._fetch_yahoo_data(timeframe)
        if data is not None:
            print("✅ Yahoo Finance data fetch successful")
            return data
        else:
            print("❌ Both data sources failed, switching to demo mode...")
            # Final fallback to demo data
            print("🎭 Using demo data as final fallback...")
            data = DemoDataGenerator().generate_demo_data(timeframe)
            print(f"✅ Demo data generated successfully ({len(data)} data points)")
            return data
    
    def _fetch_alpha_vantage_data(self, timeframe: str) -> Optional[pd.DataFrame]:
        """Fetch data from Alpha Vantage API"""
        try:
            # Rate limiting
            current_time = time.time()
            if current_time - self.last_request_time < self.min_request_interval:
                wait_time = self.min_request_interval - (current_time - self.last_request_time)
                print(f"⏳ Rate limiting: waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
            
            # Get interval from config
            interval = self.config.TIMEFRAME_MAPPING[timeframe]['av_interval']
            
            # Alpha Vantage API parameters
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': self.config.AV_SYMBOL,
                'interval': interval,
                'apikey': self.config.ALPHA_VANTAGE_API_KEY,
                'outputsize': 'full'
            }
            
            response = requests.get(self.config.ALPHA_VANTAGE_BASE_URL, params=params, timeout=30)
            self.last_request_time = time.time()
            
            if response.status_code != 200:
                print(f"❌ Alpha Vantage API error: {response.status_code}")
                return None
            
            data = response.json()
            
            # Check for API errors
            if 'Error Message' in data:
                print(f"❌ Alpha Vantage error: {data['Error Message']}")
                return None
            
            if 'Note' in data:
                print(f"⚠️  Alpha Vantage rate limit: {data['Note']}")
                return None
            
            # Extract time series data
            time_series_key = f'Time Series ({interval})'
            if time_series_key not in data:
                print(f"❌ No time series data found in Alpha Vantage response")
                return None
            
            time_series = data[time_series_key]
            
            # Convert to DataFrame
            df_data = []
            for timestamp, values in time_series.items():
                df_data.append({
                    'timestamp': pd.to_datetime(timestamp),
                    'open': float(values['1. open']),
                    'high': float(values['2. high']),
                    'low': float(values['3. low']),
                    'close': float(values['4. close']),
                    'volume': int(values['5. volume'])
                })
            
            df = pd.DataFrame(df_data)
            df.set_index('timestamp', inplace=True)
            df.sort_index(inplace=True)
            
            # Filter data based on timeframe
            df = self._filter_by_timeframe(df, timeframe)
            
            return df
            
        except Exception as e:
            print(f"❌ Alpha Vantage fetch error: {str(e)}")
            return None
    
    def _fetch_yahoo_data(self, timeframe: str) -> Optional[pd.DataFrame]:
        """Fetch data from Yahoo Finance"""
        try:
            # Get parameters from config
            interval = self.config.TIMEFRAME_MAPPING[timeframe]['yahoo_interval']
            period = self.config.TIMEFRAME_MAPPING[timeframe]['yahoo_period']
            
            # Create ticker object
            ticker = yf.Ticker(self.config.YAHOO_SYMBOL)
            
            # Fetch data
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                print("❌ No data received from Yahoo Finance")
                return None
            
            # Standardize column names
            data.columns = data.columns.str.lower()
            data.reset_index(inplace=True)
            
            # Rename columns to match our standard
            column_mapping = {
                'datetime': 'timestamp',
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'close': 'close',
                'volume': 'volume'
            }
            
            data.rename(columns=column_mapping, inplace=True)
            data.set_index('timestamp', inplace=True)
            
            return data
            
        except Exception as e:
            print(f"❌ Yahoo Finance fetch error: {str(e)}")
            return None
    
    def _filter_by_timeframe(self, df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """Filter DataFrame based on timeframe"""
        if timeframe == '1d':
            cutoff = datetime.now() - timedelta(days=1)
        elif timeframe == '2d':
            cutoff = datetime.now() - timedelta(days=2)
        elif timeframe == '5d':
            cutoff = datetime.now() - timedelta(days=5)
        else:
            return df
        
        return df[df.index >= cutoff]
    
    def get_current_price(self) -> Optional[float]:
        """Get current gold price"""
        try:
            ticker = yf.Ticker(self.config.YAHOO_SYMBOL)
            data = ticker.history(period='1d', interval='1m')
            if not data.empty:
                return float(data['Close'].iloc[-1])
            return None
        except Exception as e:
            print(f"❌ Error fetching current price: {str(e)}")
            return None
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate that the data is suitable for analysis"""
        if df is None or df.empty:
            return False
        
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_columns):
            print(f"❌ Missing required columns. Found: {list(df.columns)}")
            return False
        
        if len(df) < 50:  # Need at least 50 data points for reliable indicators
            print(f"❌ Insufficient data points: {len(df)} (minimum 50 required)")
            return False
        
        return True
