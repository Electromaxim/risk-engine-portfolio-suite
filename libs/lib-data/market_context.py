"""
Market Context Provider
Aggregates real-time market signals for AI explanations
"""
import pandas as pd
from lib_data.calendar import TradingCalendar
from services.data-ingestion-service.connectors.bloomberg_connector import BloombergConnector

class MarketContextEngine:
    METRICS = [
        "VIX Index",  # Volatility
        "GCCITR Index",  # Commodities
        "GT10 Govt",  # Rates
        "EURUSD Curncy"  # FX
    ]
    def __init__(self, connector):  
        self.bloomberg = connector  
    
    def __init__(self):
        self.bloomberg = BloombergConnector()
        self.calendar = TradingCalendar()
        
    def get_context(self, lookback_days: int = 30) -> str:
        """Generate market summary for AI insights"""
        end_date = pd.Timestamp.today()
        start_date = self.calendar.get_trading_days(end_date - pd.Timedelta(days=lookback_days), end_date)[0]
        
        # Fetch Bloomberg data
        data = self.bloomberg.fetch_equity_data(
            tickers=self.METRICS,
            fields=["PX_LAST"],
            start_date=start_date.strftime("%Y%m%d"),
            end_date=end_date.strftime("%Y%m%d")
        )
        
        # Generate summary statistics
        summary = []
        for metric in self.METRICS:
            series = data[metric]['PX_LAST']
            summary.append(
                f"{metric}: {series.mean():.2f} avg, "
                f"{series.pct_change().std():.2%} vol, "
                f"Last: {series.iloc[-1]:.2f}"
            )
        
        return "\n".join(summary)