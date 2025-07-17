import pandas as pd
from sqlalchemy import create_engine
from lib_data.calendar import TradingCalendar
from lib_utils.config import get_config

config = get_config()

class HistoricalPnLLoader:
    def __init__(self):
        self.accounting_engine = create_engine(config.ACCOUNTING_DB_URI)
        self.calendar = TradingCalendar()

    def load_pnl_series(self, portfolio_id: int, start: str, end: str) -> pd.Series:
        """Load daily P&L from accounting system"""
        query = f"""
        SELECT date, pnl 
        FROM daily_pnl 
        WHERE portfolio_id = {portfolio_id}
          AND date BETWEEN '{start}' AND '{end}'
        ORDER BY date
        """
        df = pd.read_sql(query, self.accounting_engine, index_col='date')
        
        # Fill missing trading days with zero
        full_range = pd.date_range(start, end, freq='D')
        return df.reindex(full_range).fillna(0)['pnl']

    def align_with_var_predictions(self, pnl_series: pd.Series, var_predictions: pd.Series) -> tuple:
        """Align P&L and VaR on trading days"""
        trading_days = self.calendar.get_trading_days(pnl_series.index.min(), pnl_series.index.max())
        return pnl_series.loc[trading_days], var_predictions.loc[trading_days]