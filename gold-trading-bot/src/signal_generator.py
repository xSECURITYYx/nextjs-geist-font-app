import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from config import Config
from indicators import TechnicalIndicators

class SignalGenerator:
    """Generate trading signals based on technical analysis"""
    
    def __init__(self):
        self.config = Config()
        self.indicators = TechnicalIndicators()
    
    def generate_signal(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive trading signal based on multiple indicators
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            Dictionary with signal information
        """
        # Calculate all indicators
        indicator_data = self.indicators.calculate_all_indicators(df)
        
        if not indicator_data:
            return self._create_error_signal("Failed to calculate indicators")
        
        # Analyze individual components
        ema_signal = self._analyze_ema_signal(indicator_data)
        rsi_signal = self._analyze_rsi_signal(indicator_data)
        volume_signal = self._analyze_volume_signal(indicator_data)
        trend_signal = self._analyze_trend_signal(indicator_data)
        
        # Calculate composite signal
        composite_signal = self._calculate_composite_signal(
            ema_signal, rsi_signal, volume_signal, trend_signal
        )
        
        # Generate risk management levels
        risk_levels = self._calculate_risk_levels(df, indicator_data, composite_signal)
        
        # Create final signal package
        final_signal = {
            'timestamp': indicator_data['timestamp'],
            'current_price': indicator_data['current_price'],
            'signal': composite_signal['signal'],
            'signal_strength': composite_signal['strength'],
            'confidence': composite_signal['confidence'],
            'components': {
                'ema': ema_signal,
                'rsi': rsi_signal,
                'volume': volume_signal,
                'trend': trend_signal
            },
            'risk_management': risk_levels,
            'market_context': self._get_market_context(indicator_data),
            'recommendation': self._generate_recommendation(composite_signal, risk_levels)
        }
        
        return final_signal
    
    def _analyze_ema_signal(self, indicator_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze EMA crossover signals"""
        crossover = indicator_data['crossover_analysis']
        trend = indicator_data['trend_analysis']
        
        signal = 'HOLD'
        strength = 0.0
        reasoning = []
        
        if crossover['crossover'] == 'BULLISH':
            signal = 'BUY'
            strength = crossover['signal_strength']
            reasoning.append(f"EMA-{self.config.EMA_SHORT_PERIOD} crossed above EMA-{self.config.EMA_LONG_PERIOD}")
        elif crossover['crossover'] == 'BEARISH':
            signal = 'SELL'
            strength = crossover['signal_strength']
            reasoning.append(f"EMA-{self.config.EMA_SHORT_PERIOD} crossed below EMA-{self.config.EMA_LONG_PERIOD}")
        else:
            # No crossover, check trend strength
            if trend['direction'] == 'BULLISH' and trend['strength'] > 2.0:
                signal = 'BUY'
                strength = trend['strength'] * 0.5  # Reduced strength for trend-only signals
                reasoning.append(f"Strong bullish trend (separation: {trend['separation_percent']:.2f}%)")
            elif trend['direction'] == 'BEARISH' and trend['strength'] > 2.0:
                signal = 'SELL'
                strength = trend['strength'] * 0.5
                reasoning.append(f"Strong bearish trend (separation: {trend['separation_percent']:.2f}%)")
            else:
                reasoning.append("No significant EMA signal")
        
        return {
            'signal': signal,
            'strength': strength,
            'reasoning': reasoning,
            'crossover_type': crossover['crossover'],
            'trend_direction': trend['direction'],
            'trend_strength': trend['strength']
        }
    
    def _analyze_rsi_signal(self, indicator_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze RSI-based signals"""
        rsi_data = indicator_data['rsi_analysis']
        
        signal = 'HOLD'
        strength = 0.0
        reasoning = []
        
        current_rsi = rsi_data['current_rsi']
        
        if rsi_data['is_oversold']:
            signal = 'BUY'
            strength = (self.config.RSI_OVERSOLD - current_rsi) / 10  # Strength based on how oversold
            reasoning.append(f"RSI oversold at {current_rsi:.1f}")
        elif rsi_data['is_overbought']:
            signal = 'SELL'
            strength = (current_rsi - self.config.RSI_OVERBOUGHT) / 10  # Strength based on how overbought
            reasoning.append(f"RSI overbought at {current_rsi:.1f}")
        else:
            # Check RSI momentum
            if rsi_data['momentum'] > 5 and current_rsi < 60:
                signal = 'BUY'
                strength = min(rsi_data['momentum'] / 10, 2.0)
                reasoning.append(f"Strong RSI momentum (+{rsi_data['momentum']:.1f})")
            elif rsi_data['momentum'] < -5 and current_rsi > 40:
                signal = 'SELL'
                strength = min(abs(rsi_data['momentum']) / 10, 2.0)
                reasoning.append(f"Negative RSI momentum ({rsi_data['momentum']:.1f})")
            else:
                reasoning.append(f"RSI neutral at {current_rsi:.1f}")
        
        return {
            'signal': signal,
            'strength': strength,
            'reasoning': reasoning,
            'current_rsi': current_rsi,
            'condition': rsi_data['condition'],
            'momentum': rsi_data['momentum']
        }
    
    def _analyze_volume_signal(self, indicator_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze volume-based confirmation"""
        volume_data = indicator_data['volume_profile']
        
        signal = 'NEUTRAL'
        strength = 0.0
        reasoning = []
        
        volume_ratio = volume_data['volume_ratio']
        
        if volume_data['is_high_volume']:
            strength = min((volume_ratio - 1.0) * 2, 3.0)  # Cap at 3.0
            reasoning.append(f"High volume confirmation ({volume_ratio:.1f}x average)")
        elif volume_ratio < 0.5:
            strength = -1.0  # Negative strength for low volume
            reasoning.append(f"Low volume warning ({volume_ratio:.1f}x average)")
        else:
            reasoning.append(f"Normal volume ({volume_ratio:.1f}x average)")
        
        return {
            'signal': signal,
            'strength': strength,
            'reasoning': reasoning,
            'volume_ratio': volume_ratio,
            'is_high_volume': volume_data['is_high_volume']
        }
    
    def _analyze_trend_signal(self, indicator_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze overall trend context"""
        trend_data = indicator_data['trend_analysis']
        support_resistance = indicator_data['support_resistance']
        current_price = indicator_data['current_price']
        
        signal = 'HOLD'
        strength = 0.0
        reasoning = []
        
        # Check price position relative to support/resistance
        support = support_resistance['support']
        resistance = support_resistance['resistance']
        
        if current_price <= support * 1.01:  # Within 1% of support
            signal = 'BUY'
            strength = 2.0
            reasoning.append(f"Price near support level (${support:.2f})")
        elif current_price >= resistance * 0.99:  # Within 1% of resistance
            signal = 'SELL'
            strength = 2.0
            reasoning.append(f"Price near resistance level (${resistance:.2f})")
        else:
            reasoning.append(f"Price between support (${support:.2f}) and resistance (${resistance:.2f})")
        
        # Add trend context
        if trend_data['strength'] > 3.0:
            reasoning.append(f"Strong {trend_data['direction'].lower()} trend")
        
        return {
            'signal': signal,
            'strength': strength,
            'reasoning': reasoning,
            'support_level': support,
            'resistance_level': resistance,
            'trend_direction': trend_data['direction']
        }
    
    def _calculate_composite_signal(self, ema_signal: Dict, rsi_signal: Dict, 
                                  volume_signal: Dict, trend_signal: Dict) -> Dict[str, Any]:
        """Calculate weighted composite signal"""
        
        # Signal scoring
        signal_scores = {'BUY': 0, 'SELL': 0, 'HOLD': 0}
        total_strength = 0
        
        # Weight and score each component
        components = [
            (ema_signal, self.config.SIGNAL_WEIGHTS['ema_crossover']),
            (rsi_signal, self.config.SIGNAL_WEIGHTS['rsi_confirmation']),
            (volume_signal, self.config.SIGNAL_WEIGHTS['volume_confirmation']),
            (trend_signal, self.config.SIGNAL_WEIGHTS['trend_strength'])
        ]
        
        for component, weight in components:
            if component['signal'] in signal_scores:
                weighted_strength = component['strength'] * weight
                signal_scores[component['signal']] += weighted_strength
                total_strength += abs(weighted_strength)
        
        # Determine final signal
        max_signal = max(signal_scores, key=signal_scores.get)
        max_score = signal_scores[max_signal]
        
        # Require minimum threshold for non-HOLD signals
        min_threshold = 1.0
        if max_signal != 'HOLD' and max_score < min_threshold:
            final_signal = 'HOLD'
            signal_strength = max_score
        else:
            final_signal = max_signal
            signal_strength = max_score
        
        # Calculate confidence based on signal consensus
        signal_consensus = self._calculate_signal_consensus(ema_signal, rsi_signal, trend_signal)
        confidence = min(signal_strength * signal_consensus, 10.0)
        
        return {
            'signal': final_signal,
            'strength': signal_strength,
            'confidence': confidence,
            'scores': signal_scores,
            'consensus': signal_consensus
        }
    
    def _calculate_signal_consensus(self, ema_signal: Dict, rsi_signal: Dict, trend_signal: Dict) -> float:
        """Calculate how much the signals agree with each other"""
        signals = [ema_signal['signal'], rsi_signal['signal'], trend_signal['signal']]
        
        # Count signal agreement
        buy_count = signals.count('BUY')
        sell_count = signals.count('SELL')
        hold_count = signals.count('HOLD')
        
        # Calculate consensus score
        max_count = max(buy_count, sell_count, hold_count)
        consensus = max_count / len(signals)
        
        return consensus
    
    def _calculate_risk_levels(self, df: pd.DataFrame, indicator_data: Dict, 
                             composite_signal: Dict) -> Dict[str, Any]:
        """Calculate stop loss and take profit levels"""
        current_price = indicator_data['current_price']
        atr = indicator_data['atr'].iloc[-1]
        support_resistance = indicator_data['support_resistance']
        
        # ATR-based stop loss
        atr_stop_distance = atr * self.config.STOP_LOSS_ATR_MULTIPLIER
        
        if composite_signal['signal'] == 'BUY':
            # For buy signals
            stop_loss = max(
                current_price - atr_stop_distance,
                support_resistance['support'] * 0.99  # Just below support
            )
            take_profit = current_price + (atr_stop_distance * self.config.TAKE_PROFIT_RATIO)
            
        elif composite_signal['signal'] == 'SELL':
            # For sell signals
            stop_loss = min(
                current_price + atr_stop_distance,
                support_resistance['resistance'] * 1.01  # Just above resistance
            )
            take_profit = current_price - (atr_stop_distance * self.config.TAKE_PROFIT_RATIO)
            
        else:
            # For hold signals
            stop_loss = current_price - atr_stop_distance
            take_profit = current_price + atr_stop_distance
        
        # Calculate risk metrics
        risk_amount = abs(current_price - stop_loss)
        reward_amount = abs(take_profit - current_price)
        risk_reward_ratio = reward_amount / risk_amount if risk_amount > 0 else 0
        
        return {
            'stop_loss': round(stop_loss, 2),
            'take_profit': round(take_profit, 2),
            'risk_amount': round(risk_amount, 2),
            'reward_amount': round(reward_amount, 2),
            'risk_reward_ratio': round(risk_reward_ratio, 2),
            'atr_value': round(atr, 2)
        }
    
    def _get_market_context(self, indicator_data: Dict) -> Dict[str, Any]:
        """Get additional market context information"""
        return {
            'trend_direction': indicator_data['trend_analysis']['direction'],
            'trend_strength': indicator_data['trend_analysis']['strength'],
            'rsi_condition': indicator_data['rsi_analysis']['condition'],
            'volume_status': 'HIGH' if indicator_data['volume_profile']['is_high_volume'] else 'NORMAL',
            'support_level': indicator_data['support_resistance']['support'],
            'resistance_level': indicator_data['support_resistance']['resistance']
        }
    
    def _generate_recommendation(self, composite_signal: Dict, risk_levels: Dict) -> str:
        """Generate human-readable trading recommendation"""
        signal = composite_signal['signal']
        strength = composite_signal['strength']
        confidence = composite_signal['confidence']
        
        if signal == 'BUY':
            if confidence >= 7.0:
                return f"STRONG BUY - High confidence signal (Score: {confidence:.1f}/10)"
            elif confidence >= 5.0:
                return f"BUY - Moderate confidence signal (Score: {confidence:.1f}/10)"
            else:
                return f"WEAK BUY - Low confidence signal (Score: {confidence:.1f}/10)"
        
        elif signal == 'SELL':
            if confidence >= 7.0:
                return f"STRONG SELL - High confidence signal (Score: {confidence:.1f}/10)"
            elif confidence >= 5.0:
                return f"SELL - Moderate confidence signal (Score: {confidence:.1f}/10)"
            else:
                return f"WEAK SELL - Low confidence signal (Score: {confidence:.1f}/10)"
        
        else:
            return f"HOLD - No clear trading opportunity (Score: {confidence:.1f}/10)"
    
    def _create_error_signal(self, error_message: str) -> Dict[str, Any]:
        """Create error signal when analysis fails"""
        return {
            'signal': 'ERROR',
            'error': error_message,
            'timestamp': pd.Timestamp.now(),
            'recommendation': 'Unable to generate signal due to data issues'
        }
