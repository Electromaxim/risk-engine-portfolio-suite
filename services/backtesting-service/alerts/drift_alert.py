import smtplib
from email.mime.text import MIMEText
from lib_utils.config import get_config
from lib_utils.logger import get_logger
from drift import DriftDetector

config = get_config()
logger = get_logger(__name__)

class DriftAlertSystem:
    def __init__(self, threshold: float = 0.25):
        self.detector = DriftDetector(threshold)
        self.slack_webhook = config.SLACK_RISK_ALERTS

    def check_and_alert(self, current_distribution, historical_distribution):
        drift_detected, kl_div = self.detector.detect_drift(
            historical_distribution, current_distribution
        )
        
        if drift_detected:
            self._send_slack_alert(kl_div)
            self._send_email_alert(kl_div)
            return True
        return False

    def _send_slack_alert(self, kl_div: float):
        import requests
        message = {
            "text": f"🚨 Risk Model Drift Alert",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*KL Divergence Alert*: Significant distribution drift detected"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Metric*: KL Divergence"},
                        {"type": "mrkdwn", "text": f"*Value*: {kl_div:.4f}"},
                        {"type": "mrkdwn", "text": f"*Threshold*: {self.detector.threshold}"},
                        {"type": "mrkdwn", "text": f"*Action*: Investigate model calibration"}
                    ]
                }
            ]
        }
        requests.post(self.slack_webhook, json=message)

    def _send_email_alert(self, kl_div: float):
        msg = MIMEText(f"""
        Risk Model Drift Alert
        
        KL Divergence: {kl_div:.4f}
        Threshold: {self.detector.threshold}
        
        Required Actions:
        1. Validate current market data pipeline
        2. Recalibrate risk models
        3. Review recent VaR backtest results
        """)
        msg["Subject"] = "URGENT: Risk Model Drift Detected"
        msg["From"] = config.EMAIL_FROM
        msg["To"] = config.EMAIL_RISK_TEAM
        
        with smtplib.SMTP(config.SMTP_SERVER) as server:
            server.send_message(msg)