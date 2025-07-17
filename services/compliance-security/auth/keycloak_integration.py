from keycloak import KeycloakOpenID

class KeycloakAuth:
    def __init__(self):
        self.client = KeycloakOpenID(
            server_url=config.KEYCLOAK_URL,
            client_id="risk-engine",
            realm_name="rothschild",
            client_secret_key=config.KEYCLOAK_SECRET
        )
    
    def authenticate(self, token: str) -> dict:
        """Validate token and map Keycloak roles to internal permissions"""
        userinfo = self.client.userinfo(token)
        return {
            "user_id": userinfo["sub"],
            "roles": self._map_roles(userinfo["realm_access"]["roles"]),
            "portfolio_access": self._get_portfolio_scope(userinfo)
        }
    
    def _map_roles(self, keycloak_roles: list) -> list:
        role_map = {
            "risk-analyst": ["READ_PORTFOLIO", "RUN_VAR"],
            "risk-manager": ["OVERRIDE_CHECKS", "APPROVE_SCENARIOS"],
            "compliance": ["VIEW_AUDIT_LOGS", "EXPORT_REPORTS"]
        }
        return [perm for role in keycloak_roles for perm in role_map.get(role, [])]