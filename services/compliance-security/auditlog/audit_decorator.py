from functools import wraps
from lib_utils.config import get_config
from .s3_audit_logger import AuditLogger

audit_logger = AuditLogger()
config = get_config()

def audit_event(event_type: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get('user', 'system')
            result = func(*args, **kwargs)
            
            # Log after successful execution
            audit_logger.log_event(
                event_type=event_type,
                payload={
                    "function": func.__name__,
                    "args": args,
                    "kwargs": {k: v for k, v in kwargs.items() if k != 'password'},
                    "result": result
                },
                user=user
            )
            return result
        return wrapper
    return decorator

# Usage in risk engine:
@audit_event("VAR_CALCULATION")
def calculate_var(portfolio: dict, user: str):
    # Risk calculation logic