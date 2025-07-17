from openai import OpenAI
from knowledge_graph import RiskKnowledgeGraph

client = OpenAI(api_key=config.OPENAI_API_KEY)

class AlertEnricher:
    def enrich_alert(self, alert: dict) -> str:
        """Add contextual knowledge to raw alerts"""
        context = self._retrieve_context(alert)
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a risk analyst at Rothschild. Explain alerts with context."},
                {"role": "user", "content": f"""
                Alert: {alert['message']}
                Context: {context}
                Generate 2-sentence insight with historical precedents and recommended actions.
                """}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content

    def _retrieve_context(self, alert: dict) -> str:
        """Query knowledge graph for related events"""
        with self.driver.session() as session:
            result = session.run("""
            MATCH (a:Alert {id: $alert_id})-[:RELATED_TO*..3]-(e:Event)
            RETURN e.description, e.impact, e.date
            """, alert_id=alert['id'])
            return "\n".join([str(record) for record in result])