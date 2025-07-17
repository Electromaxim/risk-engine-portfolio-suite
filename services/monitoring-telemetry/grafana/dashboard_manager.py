import requests
import json
from lib_utils.config import get_config

config = get_config()

class GrafanaDashboardManager:
    DASHBOARD_TEMPLATE = {
        "title": "Risk Engine Monitoring",
        "panels": [
            {
                "title": "VaR Coverage",
                "type": "graph",
                "targets": [{
                    "expr": 'sum(rate(var_backtest_breaches_total[5m])) / sum(rate(var_predictions_total[5m]))',
                    "legendFormat": "Breach Rate"
                }],
                "thresholds": [{"value": 0.025, "color": "red"}]
            },
            {
                "title": "Model Calibration Status",
                "type": "stat",
                "targets": [{
                    "expr": 'risk_model_calibration_status',
                    "format": "table"
                }],
                "colorMode": "background",
                "mapping": [
                    {"0": "CRITICAL", "color": "red"},
                    {"1": "WARNING", "color": "yellow"},
                    {"2": "OK", "color": "green"}
                ]
            }
        ]
    }

    def create_production_dashboard(self):
        """Deploy standard monitoring dashboard to Grafana"""
        headers = {"Authorization": f"Bearer {config.GRAFANA_API_KEY}"}
        response = requests.post(
            f"{config.GRAFANA_URL}/api/dashboards/db",
            headers=headers,
            json={"dashboard": self.DASHBOARD_TEMPLATE}
        )
        if response.status_code != 200:
            raise RuntimeError(f"Dashboard creation failed: {response.text}")
        return response.json()["uid"]