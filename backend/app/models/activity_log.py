"""ActivityLog model for audit trail."""
import uuid
from datetime import datetime
from app import db


class ActivityLog(db.Model):
    """Activity log for tracking all actions."""
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    action_type = db.Column(db.String(100), nullable=False)
    actor = db.Column(db.String(50), nullable=False)  # 'admin', 'system', 'guest', 'host'
    target_type = db.Column(db.String(50), nullable=True)  # 'guest', 'host', 'match'
    target_id = db.Column(db.String(36), nullable=True)
    details = db.Column(db.JSON, nullable=True)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    @classmethod
    def log(cls, action_type, actor='system', target_type=None, target_id=None, details=None):
        """Create and save an activity log entry."""
        log_entry = cls(
            action_type=action_type,
            actor=actor,
            target_type=target_type,
            target_id=target_id,
            details=details
        )
        db.session.add(log_entry)
        return log_entry
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'action_type': self.action_type,
            'actor': self.actor,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'details': self.details,
            'created_at': self.created_at.isoformat()
        }
