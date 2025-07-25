import json
from openai import OpenAI
from lib_utils.config import get_config
from lib_utils.logger import get_logger

logger = get_logger(__name__)
config = get_config()
client = OpenAI(api_key=config.OPENAI_API_KEY)

#class AnomalyExplainer:
#    SYSTEM_PROMPT = """
#    You are a senior risk quant at top-tier Hedge fund. Explain model residual anomalies using:
#    - Statistical properties
#    - Market context
#    - Historical precedents
#    Output in JSON format: {"severity": "high/medium/low", "root_cause": "...", "action_items": ["..."]}
#    """
#   
#    def generate_insight(self, residual_analysis: dict, market_context: str) -> dict:
#       user_prompt = f"""
#        Residual Analysis:
#        {json.dumps(residual_analysis, indent=2)}
#        
#        Market Context:
#        {market_context}
#        """
#        
#        response = client.chat.completions.create(
#            model="gpt-4-turbo",
#            messages=[
#                {"role": "system", "content": self.SYSTEM_PROMPT},
#                {"role": "user", "content": user_prompt}
#            ],
#            response_format={"type": "json_object"},
#            temperature=0.2
#        )
#        return json.loads(response.choices[0].message.content)
        
        
class InsightGenerator:
    SYSTEM_PROMPT = """
    As Rothschild's Chief Risk AI, explain model anomalies with:
    1. Statistical significance
    2. Market context connections
    3. Historical precedents
    4. Actionable recommendations
    
    Output JSON format:
    {
        "severity": "high/medium/low",
        "probable_cause": "1-2 sentence summary",
        "historical_precedent": "Relevant historical event",
        "recommended_actions": ["list", "of", "actions"],
        "quant_metrics": {"key_metric": value}
    }
    """
    
    def __init__(self, model: str = "gpt-4-turbo"):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = model
        
    def generate_insight(self, analysis: dict, market_context: str) -> dict:
        """Create business-focused explanation from technical analysis"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": self._build_prompt(analysis, market_context)}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Insight generation failed: {e}")
            return self._fallback_response()
    
    def _build_prompt(self, analysis: dict, market_context: str) -> str:
        """Structure input for LLM"""
        return f"""
        [Residual Analysis Results]
        {json.dumps(analysis, indent=2)}
        
        [Current Market Context]
        {market_context}
        
        Generate risk management insight using the template above.
        """
    
    def _fallback_response(self) -> dict:
        """Safety net for API failures"""
        return {
            "severity": "high",
            "probable_cause": "Technical failure in analysis system",
            "recommended_actions": ["Contact AI engineering team"],
            "quant_metrics": {}
        }
