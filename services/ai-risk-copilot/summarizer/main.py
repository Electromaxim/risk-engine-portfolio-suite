# services/ai-risk-copilot/summarizer/main.py
from .log_parser.residual_forensics import ResidualForensics
from .assistant.anomaly_explainer import AnomalyExplainer

def analyze_model_residuals(model_id: str):
    residuals = load_residuals(model_id)
    analysis = ResidualForensics().analyze(residuals)
    market_context = get_market_context()
    return AnomalyExplainer().generate_insight(analysis, market_context)