# services/portfolio-service/access/dual_control.py
class DualControl:
    def authorize_change(self, change_request: dict, approver: str) -> bool:
        """Requires 2 distinct approvers for critical changes"""
        approvers = set(self.change_db.get_approvers(change_request["id"]))
        approvers.add(approver)
        return len(approvers) >= 2