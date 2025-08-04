import os
import sys
from datetime import datetime
from typing import Dict, Any
from config import Config
from data_fetcher import DataFetcher
from signal_generator import SignalGenerator

class TradingBotCLI:
    """Command Line Interface for the Gold Trading Bot"""
    
    def __init__(self, demo_mode: bool = False):
        self.config = Config()
        self.data_fetcher = DataFetcher(demo_mode=demo_mode)
        self.signal_generator = SignalGenerator()
        self.demo_mode = demo_mode
    
    def display_banner(self):
        """Display welcome banner"""
        banner = f"""
{self.config.COLORS['INFO']}
╔══════════════════════════════════════════════════════════════╗
║                    🏆 GOLD TRADING BOT AI 🏆                 ║
║                                                              ║
║           Advanced Technical Analysis for Gold Futures       ║
║                        (GC=F Analysis)                       ║
╚══════════════════════════════════════════════════════════════╝
{self.config.COLORS['RESET']}
"""
        print(banner)
    
    def display_menu(self):
        """Display main menu options"""
        menu = f"""
{self.config.COLORS['INFO']}📊 SELECT CHART TIMEFRAME:{self.config.COLORS['RESET']}

1️⃣  1-Day Chart    (5-minute candles)   - Short-term analysis
2️⃣  2-Day Chart    (15-minute candles)  - Medium-term analysis  
3️⃣  5-Day Chart    (30-minute candles)  - Weekly analysis
4️⃣  Custom Analysis
5️⃣  View Configuration
6️⃣  Exit

"""
        print(menu)
    
    def get_user_choice(self) -> str:
        """Get user menu selection"""
        while True:
            try:
                choice = input(f"{self.config.COLORS['INFO']}Enter your choice (1-6): {self.config.COLORS['RESET']}").strip()
                if choice in ['1', '2', '3', '4', '5', '6']:
                    return choice
                else:
                    print(f"{self.config.COLORS['SELL']}❌ Invalid choice. Please enter 1-6.{self.config.COLORS['RESET']}")
            except KeyboardInterrupt:
                print(f"\n{self.config.COLORS['INFO']}👋 Goodbye!{self.config.COLORS['RESET']}")
                sys.exit(0)
    
    def get_timeframe_from_choice(self, choice: str) -> str:
        """Convert menu choice to timeframe"""
        timeframe_map = {
            '1': '1d',
            '2': '2d', 
            '3': '5d'
        }
        return timeframe_map.get(choice, '1d')
    
    def display_signal_analysis(self, signal_data: Dict[str, Any]):
        """Display comprehensive signal analysis"""
        if signal_data.get('signal') == 'ERROR':
            self.display_error(signal_data.get('error', 'Unknown error'))
            return
        
        # Header
        print(f"\n{self.config.COLORS['INFO']}{'='*80}")
        print(f"🔍 GOLD TRADING ANALYSIS - {signal_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}{self.config.COLORS['RESET']}")
        
        # Current Market Info
        self.display_market_info(signal_data)
        
        # Main Signal
        self.display_main_signal(signal_data)
        
        # Technical Analysis Breakdown
        self.display_technical_breakdown(signal_data)
        
        # Risk Management
        self.display_risk_management(signal_data)
        
        # Market Context
        self.display_market_context(signal_data)
        
        print(f"{self.config.COLORS['INFO']}{'='*80}{self.config.COLORS['RESET']}\n")
    
    def display_market_info(self, signal_data: Dict[str, Any]):
        """Display current market information"""
        current_price = signal_data['current_price']
        
        print(f"\n{self.config.COLORS['INFO']}📈 CURRENT MARKET STATUS:{self.config.COLORS['RESET']}")
        print(f"   Gold Price (GC=F): ${current_price:.2f}")
        print(f"   Analysis Time: {signal_data['timestamp'].strftime('%H:%M:%S UTC')}")
    
    def display_main_signal(self, signal_data: Dict[str, Any]):
        """Display main trading signal"""
        signal = signal_data['signal']
        strength = signal_data['signal_strength']
        confidence = signal_data['confidence']
        recommendation = signal_data['recommendation']
        
        # Choose color based on signal
        if signal == 'BUY':
            color = self.config.COLORS['BUY']
            emoji = "🟢"
        elif signal == 'SELL':
            color = self.config.COLORS['SELL']
            emoji = "🔴"
        else:
            color = self.config.COLORS['HOLD']
            emoji = "🟡"
        
        print(f"\n{color}🎯 TRADING SIGNAL:{self.config.COLORS['RESET']}")
        print(f"   {emoji} Signal: {color}{signal}{self.config.COLORS['RESET']}")
        print(f"   📊 Strength: {strength:.1f}/10")
        print(f"   🎯 Confidence: {confidence:.1f}/10")
        print(f"   💡 Recommendation: {recommendation}")
    
    def display_technical_breakdown(self, signal_data: Dict[str, Any]):
        """Display detailed technical analysis"""
        components = signal_data['components']
        
        print(f"\n{self.config.COLORS['INFO']}🔧 TECHNICAL ANALYSIS BREAKDOWN:{self.config.COLORS['RESET']}")
        
        # EMA Analysis
        ema = components['ema']
        print(f"   📈 EMA Analysis:")
        print(f"      • Signal: {self._format_component_signal(ema['signal'])} (Strength: {ema['strength']:.1f})")
        print(f"      • Trend: {ema['trend_direction']} (Strength: {ema['trend_strength']:.1f})")
        for reason in ema['reasoning']:
            print(f"      • {reason}")
        
        # RSI Analysis
        rsi = components['rsi']
        print(f"   📊 RSI Analysis:")
        print(f"      • Signal: {self._format_component_signal(rsi['signal'])} (Strength: {rsi['strength']:.1f})")
        print(f"      • Current RSI: {rsi['current_rsi']:.1f} ({rsi['condition']})")
        print(f"      • Momentum: {rsi['momentum']:+.1f}")
        for reason in rsi['reasoning']:
            print(f"      • {reason}")
        
        # Volume Analysis
        volume = components['volume']
        print(f"   📦 Volume Analysis:")
        print(f"      • Volume Ratio: {volume['volume_ratio']:.1f}x average")
        print(f"      • Status: {'HIGH VOLUME' if volume['is_high_volume'] else 'NORMAL VOLUME'}")
        for reason in volume['reasoning']:
            print(f"      • {reason}")
        
        # Trend Analysis
        trend = components['trend']
        print(f"   📉 Support/Resistance:")
        print(f"      • Support Level: ${trend['support_level']:.2f}")
        print(f"      • Resistance Level: ${trend['resistance_level']:.2f}")
        print(f"      • Trend Direction: {trend['trend_direction']}")
        for reason in trend['reasoning']:
            print(f"      • {reason}")
    
    def display_risk_management(self, signal_data: Dict[str, Any]):
        """Display risk management information"""
        risk = signal_data['risk_management']
        current_price = signal_data['current_price']
        
        print(f"\n{self.config.COLORS['SELL']}⚠️  RISK MANAGEMENT:{self.config.COLORS['RESET']}")
        print(f"   🛑 Stop Loss: ${risk['stop_loss']:.2f} ({((risk['stop_loss'] - current_price) / current_price * 100):+.1f}%)")
        print(f"   🎯 Take Profit: ${risk['take_profit']:.2f} ({((risk['take_profit'] - current_price) / current_price * 100):+.1f}%)")
        print(f"   💰 Risk Amount: ${risk['risk_amount']:.2f}")
        print(f"   🏆 Reward Amount: ${risk['reward_amount']:.2f}")
        print(f"   ⚖️  Risk/Reward Ratio: 1:{risk['risk_reward_ratio']:.1f}")
        print(f"   📏 ATR (Volatility): ${risk['atr_value']:.2f}")
    
    def display_market_context(self, signal_data: Dict[str, Any]):
        """Display additional market context"""
        context = signal_data['market_context']
        
        print(f"\n{self.config.COLORS['INFO']}🌍 MARKET CONTEXT:{self.config.COLORS['RESET']}")
        print(f"   📈 Overall Trend: {context['trend_direction']} (Strength: {context['trend_strength']:.1f})")
        print(f"   📊 RSI Condition: {context['rsi_condition']}")
        print(f"   📦 Volume Status: {context['volume_status']}")
        print(f"   🔻 Key Support: ${context['support_level']:.2f}")
        print(f"   🔺 Key Resistance: ${context['resistance_level']:.2f}")
    
    def display_configuration(self):
        """Display current bot configuration"""
        print(f"\n{self.config.COLORS['INFO']}⚙️  CURRENT CONFIGURATION:{self.config.COLORS['RESET']}")
        print(f"   📊 Symbol: {self.config.DEFAULT_SYMBOL}")
        print(f"   🔑 Alpha Vantage API: {'✅ Configured' if self.config.ALPHA_VANTAGE_API_KEY else '❌ Not configured'}")
        print(f"   📈 EMA Periods: {self.config.EMA_SHORT_PERIOD}, {self.config.EMA_LONG_PERIOD}")
        print(f"   📊 RSI Period: {self.config.RSI_PERIOD}")
        print(f"   📊 RSI Levels: Oversold {self.config.RSI_OVERSOLD}, Overbought {self.config.RSI_OVERBOUGHT}")
        print(f"   💰 Risk Percentage: {self.config.DEFAULT_RISK_PERCENT}%")
        print(f"   🛑 Stop Loss Multiplier: {self.config.STOP_LOSS_ATR_MULTIPLIER}x ATR")
        print(f"   🎯 Take Profit Ratio: 1:{self.config.TAKE_PROFIT_RATIO}")
        print(f"   🔄 Trading Mode: {self.config.TRADING_MODE}")
    
    def display_custom_analysis_menu(self):
        """Display custom analysis options"""
        print(f"\n{self.config.COLORS['INFO']}🔧 CUSTOM ANALYSIS OPTIONS:{self.config.COLORS['RESET']}")
        print("1️⃣  Multi-timeframe Analysis")
        print("2️⃣  Historical Backtest")
        print("3️⃣  Real-time Monitoring")
        print("4️⃣  Back to Main Menu")
    
    def display_error(self, error_message: str):
        """Display error message"""
        print(f"\n{self.config.COLORS['SELL']}❌ ERROR: {error_message}{self.config.COLORS['RESET']}")
    
    def display_loading(self, message: str):
        """Display loading message"""
        print(f"{self.config.COLORS['INFO']}⏳ {message}...{self.config.COLORS['RESET']}")
    
    def _format_component_signal(self, signal: str) -> str:
        """Format component signal with color"""
        if signal == 'BUY':
            return f"{self.config.COLORS['BUY']}{signal}{self.config.COLORS['RESET']}"
        elif signal == 'SELL':
            return f"{self.config.COLORS['SELL']}{signal}{self.config.COLORS['RESET']}"
        else:
            return f"{self.config.COLORS['HOLD']}{signal}{self.config.COLORS['RESET']}"
    
    def run_analysis(self, timeframe: str):
        """Run complete trading analysis"""
        try:
            # Display loading message
            timeframe_desc = self.config.TIMEFRAME_MAPPING[timeframe]['description']
            self.display_loading(f"Analyzing {timeframe_desc}")
            
            # Fetch market data
            market_data = self.data_fetcher.get_market_data(timeframe)
            
            if market_data is None:
                self.display_error("Failed to fetch market data")
                return
            
            # Validate data
            if not self.data_fetcher.validate_data(market_data):
                self.display_error("Invalid or insufficient market data")
                return
            
            # Generate trading signal
            signal_data = self.signal_generator.generate_signal(market_data)
            
            # Display results
            self.display_signal_analysis(signal_data)
            
        except Exception as e:
            self.display_error(f"Analysis failed: {str(e)}")
    
    def run(self):
        """Main CLI loop"""
        self.display_banner()
        
        # Check API configuration
        if not self.config.ALPHA_VANTAGE_API_KEY:
            print(f"{self.config.COLORS['HOLD']}⚠️  Alpha Vantage API key not configured. Using Yahoo Finance only.{self.config.COLORS['RESET']}")
            print(f"   To get better data quality, add your API key to .env file")
            print(f"   Get free API key at: https://www.alphavantage.co/support/#api-key\n")
        
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            
            if choice in ['1', '2', '3']:
                timeframe = self.get_timeframe_from_choice(choice)
                self.run_analysis(timeframe)
                
                # Ask if user wants to continue
                print(f"\n{self.config.COLORS['INFO']}Press Enter to continue...{self.config.COLORS['RESET']}")
                input()
                
            elif choice == '4':
                self.display_custom_analysis_menu()
                custom_choice = input(f"{self.config.COLORS['INFO']}Enter choice (1-4): {self.config.COLORS['RESET']}")
                if custom_choice == '1':
                    # Multi-timeframe analysis
                    for tf in ['1d', '2d', '5d']:
                        print(f"\n{self.config.COLORS['INFO']}--- {self.config.TIMEFRAME_MAPPING[tf]['description']} ---{self.config.COLORS['RESET']}")
                        self.run_analysis(tf)
                elif custom_choice == '2':
                    print(f"{self.config.COLORS['HOLD']}📊 Historical backtesting feature coming soon!{self.config.COLORS['RESET']}")
                elif custom_choice == '3':
                    print(f"{self.config.COLORS['HOLD']}🔄 Real-time monitoring feature coming soon!{self.config.COLORS['RESET']}")
                
                print(f"\n{self.config.COLORS['INFO']}Press Enter to continue...{self.config.COLORS['RESET']}")
                input()
                
            elif choice == '5':
                self.display_configuration()
                print(f"\n{self.config.COLORS['INFO']}Press Enter to continue...{self.config.COLORS['RESET']}")
                input()
                
            elif choice == '6':
                print(f"\n{self.config.COLORS['BUY']}🏆 Thank you for using Gold Trading Bot AI!{self.config.COLORS['RESET']}")
                print(f"{self.config.COLORS['INFO']}💡 Remember: This is for educational purposes. Always do your own research!{self.config.COLORS['RESET']}")
                break
