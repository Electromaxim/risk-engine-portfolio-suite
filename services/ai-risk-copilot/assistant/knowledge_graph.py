import networkx as nx
from neo4j import GraphDatabase

class RiskKnowledgeGraph:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            config.NEO4J_URI, 
            auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
        )
        self.G = nx.DiGraph()

    def add_event(self, event_type: str, entities: dict, relationships: list):
        """Add risk event to knowledge graph"""
        with self.driver.session() as session:
            # Create entities
            for label, props in entities.items():
                session.execute_write(
                    self._create_node, label, props
                )
            
            # Create relationships
            for rel in relationships:
                session.execute_write(
                    self._create_relationship,
                    rel['source'], rel['target'], rel['type'], rel.get('props', {})
                )

    @staticmethod
    def _create_node(tx, label: str, properties: dict):
        props_str = ", ".join(f"{k}: ${k}" for k in properties)
        query = f"MERGE (n:{label} {{{props_str}}})"
        tx.run(query, **properties)

    @staticmethod
    def _create_relationship(tx, source: dict, target: dict, rel_type: str, props: dict):
        query = """
        MATCH (a), (b) 
        WHERE a.id = $source_id AND b.id = $target_id
        MERGE (a)-[r:{rel_type}]->(b)
        SET r += $props
        """.format(rel_type=rel_type)
        tx.run(query, 
            source_id=source['id'], 
            target_id=target['id'],
            props=props
        )