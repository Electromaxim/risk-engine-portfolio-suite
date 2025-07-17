from prometheus_client import Gauge, start_http_server

class RiskMetricsExporter:
    def __init__(self, port=9100):
        self.var_99 = Gauge('var_99', '99% Value-at-Risk', ['portfolio_id'])
        self.es_99 = Gauge('es_99', '99% Expected Shortfall', ['portfolio_id'])
        self.breach_status = Gauge('var_breach', 'VaR Breach Status (1=breach)', ['portfolio_id'])
        start_http_server(port)

    def update_metrics(self, portfolio_id: int, metrics: dict):
        """Update Prometheus metrics from risk calculation"""
        self.var_99.labels(portfolio_id=portfolio_id).set(metrics['var_99'])
        self.es_99.labels(portfolio_id=portfolio_id).set(metrics['es_99'])
        self.breach_status.labels(portfolio_id=portfolio_id).set(
            1 if metrics['breach_detected'] else 0
        )