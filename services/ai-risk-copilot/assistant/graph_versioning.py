class VersionedKnowledgeGraph(RiskKnowledgeGraph):  
    SCHEMA_VERSIONS = {  
        "2025.1": self._v1_schema,  
        "2025.2": self._v2_schema  
    }  

    def __init__(self, version="2025.2"):  
        self.schema = SCHEMA_VERSIONS[version]  

    def migrate(self, from_version: str, to_version: str):  
        """Execute schema migration path"""  
        migration_path = f"{from_version}-{to_version}"  
        if migration_path == "2025.1-2025.2":  
            self._run_cypher("ALTER GRAPH ADD CONSTRAINT risk_event_v2")  

    def _v2_schema(self):  
        return {  
            "nodes": ["Alert", "Event", "Portfolio"],  
            "relationships": ["TRIGGERED_BY", "SIMILAR_TO"],  
            "constraints": [  
                "CREATE CONSTRAINT risk_event_v2 IF NOT EXISTS FOR (e:Event) REQUIRE e.id IS UNIQUE"  
            ]  
        }  