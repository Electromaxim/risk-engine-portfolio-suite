from lib_data.fx import FXConverter
from lib_utils.logger import get_logger
import hashlib
import json

logger = get_logger(__name__)

class SAPAccountingAdapter:
    def __init__(self, system="SAP"):
        self.fx = FXConverter()
        self.mappers = {
            "SAP": self._map_sap,
            "Oracle": self._map_oracle
        }
        self.mapper = self.mappers[system]
        self.portfolio_metadata = self._load_portfolio_metadata()
    
    def _load_portfolio_metadata(self) -> dict:
        """Cache portfolio metadata (base currency, fund type)"""
        # Implementation would query portfolio service DB
        return {
            101: {"base_currency": "CHF", "fund_type": "EQUITY"},
            102: {"base_currency": "EUR", "fund_type": "FIXED_INCOME"}
        }
    
    def _map_sap(self, raw_record: dict) -> dict:
        """Hybrid mapping with currency conversion and derivatives handling"""
        portfolio_id = raw_record["PORTFOLIO"]
        metadata = self.portfolio_metadata.get(portfolio_id, {})
        base_ccy = metadata.get("base_currency", "CHF")
        
        # Currency conversion
        pnl_local = raw_record["DAILY_PNL_LC"]
        local_ccy = raw_record["CURRENCY_CD"]
        pnl_base = self.fx.convert(
            amount=pnl_local,
            from_currency=local_ccy,
            to_currency=base_ccy,
            date=raw_record["VALUATION_DATE"]
        )
        
        # Derivatives normalization
        deriv_adjusted = None
        if raw_record["ASSET_CLASS"] == "DERIV":
            deriv_adjusted = self._normalize_derivative(raw_record)
        
        return {
            "portfolio_id": portfolio_id,
            "date": pd.to_datetime(raw_record["VALUATION_DATE"]),
            "pnl_local": pnl_local,
            "currency_local": local_ccy,
            "pnl_base": pnl_base,
            "currency_base": base_ccy,
            "derivatives_adjusted": deriv_adjusted,
            "source_hash": hashlib.sha256(json.dumps(raw_record).encode()).hexdigest()
        }
    
    def _normalize_derivative(self, record: dict) -> float:
        """Apply ISDA SIMM logic for derivatives P&L"""
        # Implementation would use external SIMM library
        notional = record["NOTIONAL"]
        dv01 = record["DV01"]
        return notional * dv01 * 0.01  # Simplified placeholder