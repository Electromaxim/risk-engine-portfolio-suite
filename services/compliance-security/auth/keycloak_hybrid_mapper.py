class KeycloakRoleMapper:
    ROLE_HIERARCHY = {
        "chief-risk-officer": ["risk-manager", "compliance"],
        "risk-manager": ["risk-analyst"],
        "compliance": ["auditor"]
    }
    
    ROLE_PERMISSIONS = {
        "risk-analyst": ["READ_PORTFOLIO", "RUN_VAR"],
        "risk-manager": ["OVERRIDE_CHECKS", "APPROVE_SCENARIOS"],
        "compliance": ["VIEW_AUDIT_LOGS"],
        "auditor": ["VIEW_AUDIT_LOGS"],
        "chief-risk-officer": ["OVERRIDE_ALL"]
    }
    
    def __init__(self, attributes: dict):
        self.user_attributes = attributes
    
    def expand_roles(self, roles: list) -> list:
        """Unroll role hierarchy"""
        expanded = set(roles)
        for role in roles:
            if role in self.ROLE_HIERARCHY:
                expanded.update(self.ROLE_HIERARCHY[role])
        return list(expanded)
    
    def get_permissions(self, expanded_roles: list) -> list:
        """Convert roles to permissions with ABAC attributes"""
        permissions = set()
        for role in expanded_roles:
            if role in self.ROLE_PERMISSIONS:
                permissions.update(self.ROLE_PERMISSIONS[role])
        
        # ABAC: Add portfolio region access
        if "portfolio_region:CH" in self.user_attributes:
            permissions.add("ACCESS_CH_PORTFOLIOS")
        
        # ABAC: Trading hour restrictions
        if "tier:2" in self.user_attributes:
            permissions.add("TRADE_AFTER_HOURS")
        
        return list(permissions)
    
    def resolve_portfolio_access(self, portfolio_id: int) -> bool:
        """ABAC portfolio accessibility check"""
        portfolio_region = self._get_portfolio_region(portfolio_id)
        user_regions = [attr.split(":")[1] for attr in self.user_attributes if "portfolio_region" in attr]
        return portfolio_region in user_regions
    
    def _get_portfolio_region(self, portfolio_id: int) -> str:
        """Get region from portfolio metadata service"""
        # Implementation would call portfolio service
        return "CH" if portfolio_id < 200 else "US"