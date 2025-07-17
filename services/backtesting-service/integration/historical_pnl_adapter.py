class AccountingSystemAdapter:
    def __init__(self, system="SAP"):
        self.mappers = {
            "SAP": self._map_sap_to_risk,
            "Oracle": self._map_oracle_to_risk
        }
        self.mapper = self.mappers[system]
    
    def _map_sap_to_risk(self, raw_record: dict) -> dict:
        """Transform SAP P&L format to risk engine schema"""
        return {
            "portfolio_id": raw_record["PORTFOLIO"],
            "date": pd.to_datetime(raw_record["VALUATION_DATE"]),
            "pnl": raw_record["DAILY_PNL_LC"],
            "currency": raw_record["CURRENCY_CD"],
            "source_hash": sha256(json.dumps(raw_record).encode()).hexdigest()
        }
    
    def stream_realized_pnl(self, start_date: str) -> Generator:
        """Real-time P&L stream from accounting system"""
        # Implementation using Apache NiFi or Kafka Connect