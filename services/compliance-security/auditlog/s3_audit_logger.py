import boto3
import json
from hashlib import sha256
from lib_utils.config import get_config

config = get_config()

class AuditLogger:
    def __init__(self):
        self.s3 = boto3.client('s3',
            endpoint_url=config.S3_ENDPOINT,
            aws_access_key_id=config.S3_ACCESS_KEY,
            aws_secret_access_key=config.S3_SECRET_KEY
        )
        self.bucket = "risk-audit-logs"
        
    def log_event(self, event_type: str, payload: dict, user: str):
        """Write immutable log entry to WORM S3 bucket"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,
            "user": user,
            "payload": payload
        }
        log_json = json.dumps(log_entry).encode()
        object_key = f"{datetime.utcnow().date()}/{sha256(log_json).hexdigest()}.json"
        
        self.s3.put_object(
            Bucket=self.bucket,
            Key=object_key,
            Body=log_json,
            ObjectLockMode="GOVERNANCE",
            ObjectLockRetainUntilDate=datetime.utcnow() + timedelta(days=365*7)
        )
        return object_key