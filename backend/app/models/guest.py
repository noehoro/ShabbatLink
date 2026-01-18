"""Guest model for dinner attendees."""
import uuid
from datetime import datetime
from app import db


class Guest(db.Model):
    """Guest model - a person looking to attend Friday night dinner."""
    __tablename__ = 'guests'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Profile data (reusable)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    neighborhood = db.Column(db.String(100), nullable=False)
    max_travel_time = db.Column(db.Integer, nullable=False)  # 15, 30, 45, 60
    languages = db.Column(db.JSON, nullable=False, default=list)  # ["English", "Spanish", "Portuguese"]
    kosher_requirement = db.Column(db.String(100), nullable=False)
    contribution_range = db.Column(db.String(50), nullable=False)
    
    # JLC History
    attended_jlc_before = db.Column(db.Boolean, nullable=False, default=False)
    
    # Social verification (at least one required for security)
    facebook_url = db.Column(db.String(500), nullable=True)
    instagram_handle = db.Column(db.String(100), nullable=True)
    
    # Vibe sliders (1-5)
    vibe_chabad = db.Column(db.Integer, nullable=False, default=3)
    vibe_social = db.Column(db.Integer, nullable=False, default=3)
    vibe_formality = db.Column(db.Integer, nullable=False, default=3)
    
    # Event-specific data
    party_size = db.Column(db.Integer, nullable=False, default=1)
    
    # Admin/notes
    notes_to_admin = db.Column(db.Text, nullable=True)
    
    # Policy
    no_show_acknowledged = db.Column(db.Boolean, nullable=False, default=False)
    
    # No-show tracking
    no_show_count = db.Column(db.Integer, nullable=False, default=0)
    is_flagged = db.Column(db.Boolean, nullable=False, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    matches = db.relationship('Match', backref='guest', lazy='dynamic')
    
    def to_dict(self, include_private=False):
        """Convert to dictionary for API responses."""
        data = {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'gender': self.gender,
            'neighborhood': self.neighborhood,
            'max_travel_time': self.max_travel_time,
            'languages': self.languages,
            'kosher_requirement': self.kosher_requirement,
            'contribution_range': self.contribution_range,
            'vibe_chabad': self.vibe_chabad,
            'vibe_social': self.vibe_social,
            'vibe_formality': self.vibe_formality,
            'party_size': self.party_size,
            'attended_jlc_before': self.attended_jlc_before,
            'no_show_acknowledged': self.no_show_acknowledged,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_private:
            data['phone'] = self.phone
            data['facebook_url'] = self.facebook_url
            data['instagram_handle'] = self.instagram_handle
            data['notes_to_admin'] = self.notes_to_admin
            data['no_show_count'] = self.no_show_count
            data['is_flagged'] = self.is_flagged
        
        return data
    
    def to_summary(self):
        """Return a summary for match previews (no sensitive info)."""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'neighborhood': self.neighborhood,
            'languages': self.languages,
            'kosher_requirement': self.kosher_requirement,
            'contribution_range': self.contribution_range,
            'vibe_chabad': self.vibe_chabad,
            'vibe_social': self.vibe_social,
            'vibe_formality': self.vibe_formality,
            'party_size': self.party_size
        }
