"""
AI Risk Reasoning Engine
Core intelligence layer that connects anomalies to business actions
"""
from knowledge_graph import RiskKnowledgeGraph
from anomaly_explainer import InsightGenerator
from lib_data.market_context import MarketContextEngine
import networkx as nx

class RiskReasoner:
    def __init__(self):
        self.knowledge_graph = RiskKnowledgeGraph()
        self.insight_gen = InsightGenerator()
        self.market_ctx = MarketContextEngine()
        
    def diagnose_risk(self, portfolio_id: int, risk_metrics: dict) -> dict:
        """
        Full diagnostic workflow:
        1. Analyze risk metrics
        2. Retrieve contextual knowledge
        3. Generate actionable insights
        """
        # Step 1: Statistical anomaly detection
        residuals = self._get_model_residuals(portfolio_id)
        analysis = self.analyzer.full_analysis(residuals)
        
        # Step 2: Knowledge graph retrieval
        context = self._retrieve_historical_context(
            portfolio_id, 
            analysis["anomalies"]
        )
        
        # Step 3: Business insight generation
        market_ctx = self.market_ctx.get_context()
        insight = self.insight_gen.generate_insight(analysis, market_ctx)
        
        # Step 4: Recommended actions
        actions = self._generate_actions(insight, portfolio_id)
        
        return {
            "portfolio_id": portfolio_id,
            "analysis": analysis,
            "insight": insight,
            "actions": actions
        }
    
    def _retrieve_historical_context(self, portfolio_id: int, anomalies: list) -> str:
        """Query knowledge graph for similar historical events"""
        query = f"""
        MATCH (p:Portfolio {{id: {portfolio_id}})-[r:HAS_ANOMALY]->(a:Anomaly)
        WHERE a.date IN {anomalies}
        MATCH (a)-[c:SIMILAR_TO]->(e:Event)
        RETURN e.description, e.impact, e.recommended_response
        """
        results = self.knowledge_graph.query(query)
        return "\n".join([f"{r['e.description']} (Impact: {r['e.impact']})" for r in results])
    
    def _generate_actions(self, insight: dict, portfolio_id: int) -> list:
        """Convert insights into executable actions"""
        actions = []
        for recommendation in insight["recommended_actions"]:
            if "rebalance" in recommendation.lower():
                actions.append({
                    "type": "rebalance",
                    "portfolio": portfolio_id,
                    "intensity": 0.3 if "partial" in recommendation else 0.7
                })
            elif "hedge" in recommendation.lower():
                actions.append({
                    "type": "hedge",
                    "instrument": "EURUSD options",
                    "notional": self._calculate_hedge_size(portfolio_id)
                })
        return actions
    
    def _calculate_hedge_size(self, portfolio_id: int) -> float:
        """Determine hedge size based on portfolio exposure"""
        # Implementation would use portfolio service
        return 5000000  # Placeholder