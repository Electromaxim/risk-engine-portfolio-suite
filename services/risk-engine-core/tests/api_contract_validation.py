# tests/api_contract_validation.py
import requests
import jsonschema

class RiskAPIContractTest:
    API_ENDPOINTS = {
        "/calculate-var": {
            "method": "POST",
            "schema": {
                "type": "object",
                "properties": {
                    "portfolio_id": {"type": "integer"},
                    "confidence_level": {"type": "number", "minimum": 0.90, "maximum": 0.99}
                },
                "required": ["portfolio_id"]
            }
        },
        # Add all other endpoints...
    }
    
    BASE_URL = "http://localhost:8000"
    
    def test_endpoint_contracts(self):
        for endpoint, spec in self.API_ENDPOINTS.items():
            # Verify response schema
            response = self._call_endpoint(endpoint)
            self._validate_response(endpoint, response)
            
            # Verify error handling
            error_response = self._call_endpoint(endpoint, invalid=True)
            self._validate_error_format(error_response)
    
    def _call_endpoint(self, endpoint, invalid=False):
        if invalid:
            return requests.post(f"{self.BASE_URL}{endpoint}", json={"invalid": "data"})
        return requests.post(f"{self.BASE_URL}{endpoint}", json={"portfolio_id": 123})
    
    def _validate_response(self, endpoint, response):
        # Get response schema from OpenAPI spec
        schema = self._get_response_schema(endpoint)
        jsonschema.validate(response.json(), schema)
        
        # Verify standardized headers
        assert "X-Risk-Version" in response.headers
        assert "X-Attestation-Proof" in response.headers
    
    def _validate_error_format(self, response):
        error = response.json()
        assert "error_code" in error
        assert "message" in error
        assert "trace_id" in error
        assert response.status_code >= 400