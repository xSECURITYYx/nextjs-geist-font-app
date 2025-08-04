import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any
from config import Config

class TechnicalIndicators:
    """Calculate technical indicators for trading signals"""
    
    def __init__(self):
        self.config = Config()
    
    def calculate_ema(self, data: pd.Series, period: int) -> pd.Series:
        """
        Calculate Exponential Moving Average
        
        Args:
            data: Price series (typically close prices)
            period: EMA period
            
        Returns:
            EMA series
        """
        return data.ewm(span=period, adjust=False).mean()
    
    def calculate_rsi(self, data: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index
        
        Args:
            data: Price series (typically close prices)
            period: RSI period (default 14)
            
        Returns:
            RSI series
        """
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_atr(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Average True Range for volatility measurement
        
        Args:
            high: High price series
            low: Low price series
            close: Close price series
            period: ATR period
            
        Returns:
            ATR series
        """
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())
        
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        atr = true_range.rolling(window=period).mean()
        
        return atr
    
    def calculate_support_resistance(self, high: pd.Series, low: pd.Series, close: pd.Series, 
                                   lookback: int = 20) -> Dict[str, float]:
        """
        Calculate dynamic support and resistance levels
        
        Args:
            high: High price series
            low: Low price series
            close: Close price series
            lookback: Number of periods to look back
            
        Returns:
            Dictionary with support and resistance levels
        """
        recent_high = high.tail(lookback).max()
        recent_low = low.tail(lookback).min()
        current_price = close.iloc[-1]
        
        # Calculate pivot points
        pivot = (recent_high + recent_low + current_price) / 3
        resistance1 = 2 * pivot - recent_low
        support1 = 2 * pivot - recent_high
        
        return {
            'support': support1,
            'resistance': resistance1,
            'pivot': pivot,
            'recent_high': recent_high,
            'recent_low': recent_low
        }
    
    def calculate_volume_profile(self, volume: pd.Series, period: int = 20) -> Dict[str, float]:
        """
        Calculate volume-based indicators
        
        Args:
            volume: Volume series
            period: Period for volume analysis
            
        Returns:
            Dictionary with volume metrics
        """
        recent_volume = volume.tail(period)
        avg_volume = recent_volume.mean()
        current_volume = volume.iloc[-1]
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
        
        return {
            'current_volume': current_volume,
            'average_volume': avg_volume,
            'volume_ratio': volume_ratio,
            'is_high_volume': volume_ratio > 1.5
        }
    
    def calculate_trend_strength(self, ema_short: pd.Series, ema_long: pd.Series) -> Dict[str, Any]:
        """
        Calculate trend strength based on EMA separation
        
        Args:
            ema_short: Short EMA series
            ema_long: Long EMA series
            
        Returns:
            Dictionary with trend metrics
        """
        current_short = ema_short.iloc[-1]
        current_long = ema_long.iloc[-1]
        
        # Calculate percentage separation
        separation = abs(current_short - current_long) / current_long * 100
        
        # Determine trend direction and strength
        if current_short > current_long:
            trend_direction = 'BULLISH'
            trend_strength = min(separation / 2.0, 5.0)  # Cap at 5.0
        elif current_short < current_long:
            trend_direction = 'BEARISH'
            trend_strength = min(separation / 2.0, 5.0)  # Cap at 5.0
        else:
            trend_direction = 'NEUTRAL'
            trend_strength = 0.0
        
        return {
            'direction': trend_direction,
            'strength': trend_strength,
            'separation_percent': separation,
            'ema_short': current_short,
            'ema_long': current_long
        }
    
    def detect_ema_crossover(self, ema_short: pd.Series, ema_long: pd.Series) -> Dict[str, Any]:
        """
        Detect EMA crossover signals
        
        Args:
            ema_short: Short EMA series
            ema_long: Long EMA series
            
        Returns:
            Dictionary with crossover information
        """
        if len(ema_short) < 2 or len(ema_long) < 2:
            return {'crossover': 'NONE', 'signal_strength': 0.0}
        
        # Current and previous values
        current_short = ema_short.iloc[-1]
        current_long = ema_long.iloc[-1]
        prev_short = ema_short.iloc[-2]
        prev_long = ema_long.iloc[-2]
        
        crossover = 'NONE'
        signal_strength = 0.0
        
        # Detect crossovers
        if prev_short <= prev_long and current_short > current_long:
            crossover = 'BULLISH'
            # Strength based on how decisive the crossover is
            signal_strength = min(abs(current_short - current_long) / current_long * 100, 5.0)
        elif prev_short >= prev_long and current_short < current_long:
            crossover = 'BEARISH'
            signal_strength = min(abs(current_short - current_long) / current_long * 100, 5.0)
        
        return {
            'crossover': crossover,
            'signal_strength': signal_strength,
            'current_separation': abs(current_short - current_long),
            'previous_separation': abs(prev_short - prev_long)
        }
    
    def analyze_rsi_conditions(self, rsi: pd.Series) -> Dict[str, Any]:
        """
        Analyze RSI conditions for trading signals
        
        Args:
            rsi: RSI series
            
        Returns:
            Dictionary with RSI analysis
        """
        current_rsi = rsi.iloc[-1]
        
        # Determine RSI condition
        if current_rsi >= self.config.RSI_OVERBOUGHT:
            condition = 'OVERBOUGHT'
            signal_bias = 'SELL'
        elif current_rsi <= self.config.RSI_OVERSOLD:
            condition = 'OVERSOLD'
            signal_bias = 'BUY'
        else:
            condition = 'NEUTRAL'
            signal_bias = 'NEUTRAL'
        
        # Calculate RSI momentum (change from previous period)
        rsi_momentum = rsi.iloc[-1] - rsi.iloc[-2] if len(rsi) >= 2 else 0
        
        return {
            'current_rsi': current_rsi,
            'condition': condition,
            'signal_bias': signal_bias,
            'momentum': rsi_momentum,
            'is_overbought': current_rsi >= self.config.RSI_OVERBOUGHT,
            'is_oversold': current_rsi <= self.config.RSI_OVERSOLD
        }
    
    def calculate_all_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate all technical indicators for the given data
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            Dictionary with all calculated indicators
        """
        try:
            # Calculate EMAs
            ema_short = self.calculate_ema(df['close'], self.config.EMA_SHORT_PERIOD)
            ema_long = self.calculate_ema(df['close'], self.config.EMA_LONG_PERIOD)
            
            # Calculate RSI
            rsi = self.calculate_rsi(df['close'], self.config.RSI_PERIOD)
            
            # Calculate ATR
            atr = self.calculate_atr(df['high'], df['low'], df['close'])
            
            # Calculate support/resistance
            support_resistance = self.calculate_support_resistance(
                df['high'], df['low'], df['close']
            )
            
            # Calculate volume profile
            volume_profile = self.calculate_volume_profile(df['volume'])
            
            # Analyze trend strength
            trend_analysis = self.calculate_trend_strength(ema_short, ema_long)
            
            # Detect EMA crossover
            crossover_analysis = self.detect_ema_crossover(ema_short, ema_long)
            
            # Analyze RSI conditions
            rsi_analysis = self.analyze_rsi_conditions(rsi)
            
            return {
                'ema_short': ema_short,
                'ema_long': ema_long,
                'rsi': rsi,
                'atr': atr,
                'current_price': df['close'].iloc[-1],
                'support_resistance': support_resistance,
                'volume_profile': volume_profile,
                'trend_analysis': trend_analysis,
                'crossover_analysis': crossover_analysis,
                'rsi_analysis': rsi_analysis,
                'timestamp': df.index[-1]
            }
            
        except Exception as e:
            print(f"❌ Error calculating indicators: {str(e)}")
            return {}
