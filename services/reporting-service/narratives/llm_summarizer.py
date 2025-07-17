from openai import OpenAI
from lib_utils.config import get_config
import json

config = get_config()
client = OpenAI(api_key=config.OPENAI_API_KEY)

class RiskReportGenerator:
    SYSTEM_PROMPT = """
    You are a senior risk analyst at Rothschild & Co. Generate insightful risk assessment 
    reports in JSON format with the following structure:
    {
        "market_commentary": "2-3 sentence summary of market conditions",
        "key_risks": ["list", "of", "top 3 risks"],
        "portfolio_strengths": ["list", "of", "positive aspects"],
        "recommended_actions": ["actionable", "recommendations"]
    }
    Use professional finance terminology suitable for institutional clients.
    """

    def generate_report(self, risk_metrics: dict, portfolio: dict) -> dict:
        """Generate risk narrative using GPT-4"""
        user_prompt = f"""
        Portfolio Overview:
        - Value: {portfolio['value']:,.2f} {portfolio['currency']}
        - Positions: {len(portfolio['positions'])} assets
        
        Risk Metrics:
        - 1-Day 99% VaR: {risk_metrics['var_99']:,.2f}
        - Expected Shortfall: {risk_metrics['es_99']:,.2f}
        - Max Drawdown: {risk_metrics['max_drawdown']:.2%}
        - Volatility: {risk_metrics['volatility']:.2%}
        
        Generate comprehensive risk assessment.
        """
        
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        return json.loads(response.choices[0].message.content)