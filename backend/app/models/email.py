"""Email model for simulated email queue."""
import uuid
from datetime import datetime
from app import db
from app.config import EmailStatus


class Email(db.Model):
    """Email model for simulated email sending."""
    __tablename__ = 'emails'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    to_email = db.Column(db.String(255), nullable=False)
    to_name = db.Column(db.String(255), nullable=True)
    email_type = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=False)
    
    status = db.Column(db.String(20), nullable=False, default=EmailStatus.QUEUED.value)
    sent_at = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def mark_sent(self):
        """Mark the email as sent (simulated)."""
        self.status = EmailStatus.SENT.value
        self.sent_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'to_email': self.to_email,
            'to_name': self.to_name,
            'email_type': self.email_type,
            'subject': self.subject,
            'body': self.body,
            'status': self.status,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'created_at': self.created_at.isoformat()
        }
