"""MagicLink model for profile editing authentication."""
import uuid
import secrets
from datetime import datetime, timedelta
from app import db


class MagicLink(db.Model):
    """Magic link for profile editing authentication (NOT for match actions)."""
    __tablename__ = 'magic_links'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    email = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(64), unique=True, nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'guest' or 'host'
    user_id = db.Column(db.String(36), nullable=False)
    
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    @classmethod
    def create_for_user(cls, email, user_type, user_id, expires_minutes=15):
        """Create a new magic link for a user."""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(minutes=expires_minutes)
        
        magic_link = cls(
            email=email,
            token=token,
            user_type=user_type,
            user_id=user_id,
            expires_at=expires_at
        )
        
        return magic_link
    
    def is_valid(self):
        """Check if the magic link is still valid."""
        return self.used_at is None and datetime.utcnow() < self.expires_at
    
    def mark_used(self):
        """Mark the magic link as used."""
        self.used_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'user_type': self.user_type,
            'user_id': self.user_id,
            'expires_at': self.expires_at.isoformat(),
            'used_at': self.used_at.isoformat() if self.used_at else None,
            'created_at': self.created_at.isoformat()
        }
