import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any

class DemoDataGenerator:
    """Generate realistic demo data for testing the trading bot"""
    
    def __init__(self):
        self.base_price = 200.0  # Base price for GLD ETF
        
    def generate_demo_data(self, timeframe: str = '1d', num_points: int = 100) -> pd.DataFrame:
        """
        Generate realistic OHLCV data for demo purposes
        
        Args:
            timeframe: Chart timeframe ('1d', '2d', '5d')
            num_points: Number of data points to generate
            
        Returns:
            DataFrame with OHLCV data
        """
        # Set intervals based on timeframe
        if timeframe == '1d':
            interval_minutes = 5
            start_time = datetime.now() - timedelta(days=1)
        elif timeframe == '2d':
            interval_minutes = 15
            start_time = datetime.now() - timedelta(days=2)
        else:  # 5d
            interval_minutes = 30
            start_time = datetime.now() - timedelta(days=5)
        
        # Generate timestamps
        timestamps = []
        current_time = start_time
        for i in range(num_points):
            timestamps.append(current_time)
            current_time += timedelta(minutes=interval_minutes)
        
        # Generate realistic price data with trends and volatility
        np.random.seed(42)  # For reproducible demo data
        
        # Create a trending price series
        trend = np.linspace(0, 5, num_points)  # Slight upward trend
        noise = np.random.normal(0, 2, num_points)  # Random volatility
        cyclical = 3 * np.sin(np.linspace(0, 4*np.pi, num_points))  # Cyclical pattern
        
        # Generate close prices
        close_prices = self.base_price + trend + noise + cyclical
        
        # Generate OHLC data
        data = []
        for i, (timestamp, close) in enumerate(zip(timestamps, close_prices)):
            # Generate realistic OHLC based on close price
            volatility = np.random.uniform(0.5, 2.0)
            
            high = close + np.random.uniform(0, volatility)
            low = close - np.random.uniform(0, volatility)
            
            if i == 0:
                open_price = close + np.random.uniform(-0.5, 0.5)
            else:
                # Open close to previous close
                open_price = close_prices[i-1] + np.random.uniform(-0.3, 0.3)
            
            # Ensure OHLC relationships are correct
            high = max(high, open_price, close)
            low = min(low, open_price, close)
            
            # Generate volume (higher volume on bigger price moves)
            price_change = abs(close - (close_prices[i-1] if i > 0 else close))
            base_volume = np.random.uniform(1000000, 3000000)
            volume_multiplier = 1 + (price_change / close) * 10
            volume = int(base_volume * volume_multiplier)
            
            data.append({
                'timestamp': timestamp,
                'open': round(open_price, 2),
                'high': round(high, 2),
                'low': round(low, 2),
                'close': round(close, 2),
                'volume': volume
            })
        
        # Create DataFrame
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        
        return df
    
    def generate_trending_data(self, direction: str = 'bullish', timeframe: str = '1d') -> pd.DataFrame:
        """
        Generate data with specific trend for testing signals
        
        Args:
            direction: 'bullish', 'bearish', or 'sideways'
            timeframe: Chart timeframe
            
        Returns:
            DataFrame with trending data
        """
        num_points = 100
        
        if direction == 'bullish':
            # Strong upward trend with EMA crossover
            trend = np.linspace(0, 15, num_points)
            noise = np.random.normal(0, 1, num_points)
        elif direction == 'bearish':
            # Strong downward trend
            trend = np.linspace(0, -15, num_points)
            noise = np.random.normal(0, 1, num_points)
        else:  # sideways
            # Sideways movement
            trend = np.random.normal(0, 0.5, num_points)
            noise = np.random.normal(0, 2, num_points)
        
        # Generate timestamps
        start_time = datetime.now() - timedelta(days=1)
        timestamps = [start_time + timedelta(minutes=5*i) for i in range(num_points)]
        
        # Generate close prices
        close_prices = self.base_price + trend + noise
        
        # Generate OHLCV data
        data = []
        for i, (timestamp, close) in enumerate(zip(timestamps, close_prices)):
            volatility = np.random.uniform(0.3, 1.0)
            
            high = close + np.random.uniform(0, volatility)
            low = close - np.random.uniform(0, volatility)
            open_price = close_prices[i-1] + np.random.uniform(-0.2, 0.2) if i > 0 else close
            
            high = max(high, open_price, close)
            low = min(low, open_price, close)
            
            volume = np.random.randint(1000000, 4000000)
            
            data.append({
                'timestamp': timestamp,
                'open': round(open_price, 2),
                'high': round(high, 2),
                'low': round(low, 2),
                'close': round(close, 2),
                'volume': volume
            })
        
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        
        return df
    
    def get_demo_scenarios(self) -> Dict[str, Any]:
        """Get different demo scenarios for testing"""
        return {
            'bullish_breakout': {
                'name': 'Bullish Breakout',
                'description': 'Strong upward trend with EMA crossover',
                'data': self.generate_trending_data('bullish')
            },
            'bearish_breakdown': {
                'name': 'Bearish Breakdown', 
                'description': 'Strong downward trend',
                'data': self.generate_trending_data('bearish')
            },
            'sideways_market': {
                'name': 'Sideways Market',
                'description': 'Range-bound trading',
                'data': self.generate_trending_data('sideways')
            },
            'normal_market': {
                'name': 'Normal Market',
                'description': 'Regular market conditions',
                'data': self.generate_demo_data('1d')
            }
        }
