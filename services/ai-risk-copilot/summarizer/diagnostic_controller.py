"""
Diagnostic Orchestration Module
Coordinates analysis → insight → alerting workflow
"""
from .log_parser.residual_forensics import ResidualAnalyzer
from .assistant.anomaly_explainer import InsightGenerator
from monitoring_telemetry.alerts import send_alert
from lib_data.market_context import get_market_context
from lib_utils.logger import get_logger

logger = get_logger(__name__)

class DiagnosticController:
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.analyzer = ResidualAnalyzer(window=90)
        self.insight_gen = InsightGenerator()
        
    def run_daily_diagnostic(self):
        """Full diagnostic workflow"""
        # 1. Load residuals from risk engine output
        residuals = self._load_residuals()
        
        if residuals.empty:
            logger.warning(f"No residuals found for {self.model_id}")
            return
        
        # 2. Perform statistical analysis
        analysis = self.analyzer.full_analysis(residuals)
        
        # 3. Generate business insight
        market_context = get_market_context()
        insight = self.insight_gen.generate_insight(analysis, market_context)
        
        # 4. Trigger alerts if needed
        if insight['severity'] in ['high', 'medium']:
            self._trigger_alert(insight)
        
        return insight
    
    def _load_residuals(self) -> pd.Series:
        """Load model residuals from risk engine output"""
        # Implementation would query risk engine database
        return pd.Series(np.random.randn(250),  # Placeholder
                         index=pd.date_range(end=pd.Timestamp.today(), periods=250, freq='B'))
    
    def _trigger_alert(self, insight: dict):
        """Send alert via configured channels"""
        message = f"""
        🚨 Risk Model Anomaly - {self.model_id}
        Severity: {insight['severity'].upper()}
        Probable Cause: {insight['probable_cause']}
        Recommended Actions: {', '.join(insight['recommended_actions'])}
        """
        send_alert(
            title=f"Model Risk Alert: {self.model_id}",
            message=message,
            severity=insight['severity']
        )