#!/usr/bin/env python3
"""
Gold Trading Bot AI - Main Application
Advanced Technical Analysis for Gold Futures Trading

This bot analyzes live and historical market data to generate trading signals
for Gold Futures (GC=F) using technical indicators like EMA and RSI.
"""

import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from data_fetcher import DataFetcher
from signal_generator import SignalGenerator
from cli import TradingBotCLI

class GoldTradingBot:
    """Main Gold Trading Bot class"""
    
    def __init__(self, demo_mode: bool = False):
        """Initialize the trading bot"""
        self.config = Config()
        self.data_fetcher = DataFetcher(demo_mode=demo_mode)
        self.signal_generator = SignalGenerator()
        self.cli = TradingBotCLI(demo_mode=demo_mode)
        self.demo_mode = demo_mode
        
        # Initialize session data
        self.session_data = {
            'start_time': datetime.now(),
            'analyses_performed': 0,
            'signals_generated': [],
            'last_analysis': None
        }
    
    def run_single_analysis(self, timeframe: str = '1d', display_results: bool = True) -> Optional[Dict[str, Any]]:
        """
        Run a single trading analysis
        
        Args:
            timeframe: Chart timeframe ('1d', '2d', '5d')
            display_results: Whether to display results via CLI
            
        Returns:
            Signal data dictionary or None if failed
        """
        try:
            print(f"🚀 Starting Gold Trading Analysis...")
            print(f"📊 Timeframe: {self.config.TIMEFRAME_MAPPING[timeframe]['description']}")
            print(f"⏰ Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Fetch market data
            market_data = self.data_fetcher.get_market_data(timeframe)
            
            if market_data is None:
                print("❌ Failed to fetch market data")
                return None
            
            # Validate data quality
            if not self.data_fetcher.validate_data(market_data):
                print("❌ Data validation failed")
                return None
            
            print(f"✅ Successfully fetched {len(market_data)} data points")
            
            # Generate trading signal
            signal_data = self.signal_generator.generate_signal(market_data)
            
            if signal_data.get('signal') == 'ERROR':
                print(f"❌ Signal generation failed: {signal_data.get('error')}")
                return None
            
            # Update session data
            self.session_data['analyses_performed'] += 1
            self.session_data['signals_generated'].append({
                'timestamp': signal_data['timestamp'],
                'signal': signal_data['signal'],
                'strength': signal_data['signal_strength'],
                'confidence': signal_data['confidence']
            })
            self.session_data['last_analysis'] = signal_data
            
            # Display results if requested
            if display_results:
                self.cli.display_signal_analysis(signal_data)
            
            return signal_data
            
        except Exception as e:
            print(f"❌ Analysis failed: {str(e)}")
            return None
    
    def run_multi_timeframe_analysis(self) -> Dict[str, Any]:
        """
        Run analysis across multiple timeframes
        
        Returns:
            Dictionary with results from all timeframes
        """
        print(f"\n🔍 Running Multi-Timeframe Analysis...")
        print(f"{'='*60}")
        
        results = {}
        timeframes = ['1d', '2d', '5d']
        
        for timeframe in timeframes:
            print(f"\n📊 Analyzing {self.config.TIMEFRAME_MAPPING[timeframe]['description']}...")
            result = self.run_single_analysis(timeframe, display_results=False)
            results[timeframe] = result
        
        # Display consolidated results
        self._display_multi_timeframe_results(results)
        
        return results
    
    def run_backtest_mode(self, timeframe: str = '5d') -> Dict[str, Any]:
        """
        Run in backtest mode using historical data
        
        Args:
            timeframe: Timeframe for backtesting
            
        Returns:
            Backtest results
        """
        print(f"\n📈 Running Backtest Mode...")
        print(f"⏰ Timeframe: {self.config.TIMEFRAME_MAPPING[timeframe]['description']}")
        
        # For now, run single analysis
        # TODO: Implement proper backtesting with historical signal tracking
        result = self.run_single_analysis(timeframe)
        
        if result:
            print(f"\n✅ Backtest completed successfully")
            return {
                'mode': 'BACKTEST',
                'timeframe': timeframe,
                'result': result,
                'performance_metrics': self._calculate_basic_metrics(result)
            }
        else:
            return {'mode': 'BACKTEST', 'status': 'FAILED'}
    
    def run_realtime_mode(self, timeframe: str = '1d', iterations: int = 1) -> None:
        """
        Run in real-time mode (for future live trading integration)
        
        Args:
            timeframe: Timeframe for analysis
            iterations: Number of analysis iterations
        """
        print(f"\n🔄 Running Real-time Mode...")
        print(f"📊 Timeframe: {timeframe}")
        print(f"🔁 Iterations: {iterations}")
        
        for i in range(iterations):
            if iterations > 1:
                print(f"\n--- Iteration {i+1}/{iterations} ---")
            
            result = self.run_single_analysis(timeframe)
            
            if result and iterations > 1:
                # In real implementation, this would wait for next interval
                print(f"⏳ Waiting for next analysis cycle...")
                # time.sleep(300)  # Wait 5 minutes (disabled for demo)
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of current session"""
        runtime = datetime.now() - self.session_data['start_time']
        
        return {
            'session_start': self.session_data['start_time'],
            'runtime_minutes': runtime.total_seconds() / 60,
            'analyses_performed': self.session_data['analyses_performed'],
            'total_signals': len(self.session_data['signals_generated']),
            'last_analysis': self.session_data['last_analysis'],
            'signal_distribution': self._get_signal_distribution()
        }
    
    def _display_multi_timeframe_results(self, results: Dict[str, Any]) -> None:
        """Display consolidated multi-timeframe results"""
        print(f"\n{self.config.COLORS['INFO']}📊 MULTI-TIMEFRAME ANALYSIS SUMMARY{self.config.COLORS['RESET']}")
        print(f"{'='*60}")
        
        # Create summary table
        summary_data = []
        for timeframe, result in results.items():
            if result and result.get('signal') != 'ERROR':
                summary_data.append({
                    'Timeframe': self.config.TIMEFRAME_MAPPING[timeframe]['description'],
                    'Signal': result['signal'],
                    'Strength': f"{result['signal_strength']:.1f}/10",
                    'Confidence': f"{result['confidence']:.1f}/10",
                    'Price': f"${result['current_price']:.2f}"
                })
        
        if summary_data:
            # Display table
            print(f"\n{'Timeframe':<25} {'Signal':<8} {'Strength':<10} {'Confidence':<12} {'Price':<10}")
            print(f"{'-'*70}")
            
            for row in summary_data:
                signal_color = self.config.COLORS['BUY'] if row['Signal'] == 'BUY' else \
                              self.config.COLORS['SELL'] if row['Signal'] == 'SELL' else \
                              self.config.COLORS['HOLD']
                
                print(f"{row['Timeframe']:<25} {signal_color}{row['Signal']:<8}{self.config.COLORS['RESET']} "
                      f"{row['Strength']:<10} {row['Confidence']:<12} {row['Price']:<10}")
            
            # Consensus analysis
            signals = [row['Signal'] for row in summary_data]
            consensus = self._calculate_consensus(signals)
            print(f"\n🎯 Consensus Signal: {consensus}")
        else:
            print("❌ No valid results to display")
    
    def _calculate_basic_metrics(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate basic performance metrics"""
        risk_mgmt = result.get('risk_management', {})
        
        return {
            'signal_strength': result.get('signal_strength', 0),
            'confidence_score': result.get('confidence', 0),
            'risk_reward_ratio': risk_mgmt.get('risk_reward_ratio', 0),
            'potential_risk': risk_mgmt.get('risk_amount', 0),
            'potential_reward': risk_mgmt.get('reward_amount', 0)
        }
    
    def _get_signal_distribution(self) -> Dict[str, int]:
        """Get distribution of signals generated in this session"""
        distribution = {'BUY': 0, 'SELL': 0, 'HOLD': 0}
        
        for signal_record in self.session_data['signals_generated']:
            signal = signal_record['signal']
            if signal in distribution:
                distribution[signal] += 1
        
        return distribution
    
    def _calculate_consensus(self, signals: list) -> str:
        """Calculate consensus from multiple signals"""
        if not signals:
            return "NO DATA"
        
        buy_count = signals.count('BUY')
        sell_count = signals.count('SELL')
        hold_count = signals.count('HOLD')
        
        if buy_count > sell_count and buy_count > hold_count:
            return f"{self.config.COLORS['BUY']}BUY CONSENSUS{self.config.COLORS['RESET']} ({buy_count}/{len(signals)})"
        elif sell_count > buy_count and sell_count > hold_count:
            return f"{self.config.COLORS['SELL']}SELL CONSENSUS{self.config.COLORS['RESET']} ({sell_count}/{len(signals)})"
        else:
            return f"{self.config.COLORS['HOLD']}MIXED/HOLD{self.config.COLORS['RESET']}"
    
    def display_system_info(self) -> None:
        """Display system information and configuration"""
        print(f"\n{self.config.COLORS['INFO']}🔧 SYSTEM INFORMATION{self.config.COLORS['RESET']}")
        print(f"{'='*50}")
        print(f"📊 Default Symbol: {self.config.DEFAULT_SYMBOL}")
        print(f"🔑 Alpha Vantage API: {'✅ Active' if self.config.ALPHA_VANTAGE_API_KEY else '❌ Not configured'}")
        print(f"📈 EMA Periods: {self.config.EMA_SHORT_PERIOD}, {self.config.EMA_LONG_PERIOD}")
        print(f"📊 RSI Settings: {self.config.RSI_PERIOD} period, {self.config.RSI_OVERSOLD}-{self.config.RSI_OVERBOUGHT} levels")
        print(f"🎯 Risk Management: {self.config.DEFAULT_RISK_PERCENT}% risk, {self.config.STOP_LOSS_ATR_MULTIPLIER}x ATR stop")
        print(f"🔄 Trading Mode: {self.config.TRADING_MODE}")
        
        # Session info
        session = self.get_session_summary()
        print(f"\n📊 Session Statistics:")
        print(f"   ⏰ Runtime: {session['runtime_minutes']:.1f} minutes")
        print(f"   🔍 Analyses: {session['analyses_performed']}")
        print(f"   📈 Signals: {session['total_signals']}")
    
    def run_interactive_mode(self) -> None:
        """Run the bot in interactive CLI mode"""
        try:
            self.cli.run()
        except KeyboardInterrupt:
            print(f"\n{self.config.COLORS['INFO']}👋 Session ended by user{self.config.COLORS['RESET']}")
        except Exception as e:
            print(f"\n{self.config.COLORS['SELL']}❌ Unexpected error: {str(e)}{self.config.COLORS['RESET']}")
        finally:
            # Display session summary
            session = self.get_session_summary()
            if session['analyses_performed'] > 0:
                print(f"\n{self.config.COLORS['INFO']}📊 SESSION SUMMARY{self.config.COLORS['RESET']}")
                print(f"   Runtime: {session['runtime_minutes']:.1f} minutes")
                print(f"   Analyses performed: {session['analyses_performed']}")
                print(f"   Signals generated: {session['total_signals']}")
                
                if session['signal_distribution']:
                    dist = session['signal_distribution']
                    print(f"   Signal distribution: BUY({dist['BUY']}) SELL({dist['SELL']}) HOLD({dist['HOLD']})")

def main():
    """Main entry point"""
    try:
        # Create bot instance
        bot = GoldTradingBot()
        
        # Check command line arguments
        if len(sys.argv) > 1:
            command = sys.argv[1].lower()
            
            if command == 'quick':
                # Quick analysis mode
                timeframe = sys.argv[2] if len(sys.argv) > 2 else '1d'
                bot.run_single_analysis(timeframe)
                
            elif command == 'multi':
                # Multi-timeframe analysis
                bot.run_multi_timeframe_analysis()
                
            elif command == 'backtest':
                # Backtest mode
                timeframe = sys.argv[2] if len(sys.argv) > 2 else '5d'
                bot.run_backtest_mode(timeframe)
                
            elif command == 'info':
                # System information
                bot.display_system_info()
                
            else:
                print(f"❌ Unknown command: {command}")
                print("Available commands: quick, multi, backtest, info")
                
        else:
            # Interactive mode (default)
            bot.run_interactive_mode()
            
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
