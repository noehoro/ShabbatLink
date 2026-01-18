"""Host model for dinner hosts."""
import uuid
from datetime import datetime
from app import db


class Host(db.Model):
    """Host model - a person offering seats for Friday night dinner."""
    __tablename__ = 'hosts'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Profile data (reusable)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    neighborhood = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)  # Hidden until match accepted
    languages = db.Column(db.JSON, nullable=False, default=list)  # ["English", "Spanish", "Portuguese"]
    kosher_level = db.Column(db.String(100), nullable=False)
    contribution_preference = db.Column(db.String(50), nullable=False)
    
    # Vibe sliders (1-5)
    vibe_chabad = db.Column(db.Integer, nullable=False, default=3)
    vibe_social = db.Column(db.Integer, nullable=False, default=3)
    vibe_formality = db.Column(db.Integer, nullable=False, default=3)
    
    # Event-specific data
    seats_available = db.Column(db.Integer, nullable=False, default=2)
    
    # Optional fields
    tagline = db.Column(db.Text, nullable=True)  # "What to expect"
    private_notes = db.Column(db.Text, nullable=True)  # Admin only
    
    # Policy
    no_show_acknowledged = db.Column(db.Boolean, nullable=False, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    matches = db.relationship('Match', backref='host', lazy='dynamic')
    
    def to_dict(self, include_private=False, include_address=False):
        """Convert to dictionary for API responses."""
        data = {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'neighborhood': self.neighborhood,
            'languages': self.languages,
            'kosher_level': self.kosher_level,
            'contribution_preference': self.contribution_preference,
            'vibe_chabad': self.vibe_chabad,
            'vibe_social': self.vibe_social,
            'vibe_formality': self.vibe_formality,
            'seats_available': self.seats_available,
            'tagline': self.tagline,
            'no_show_acknowledged': self.no_show_acknowledged,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_private:
            data['phone'] = self.phone
            data['private_notes'] = self.private_notes
        
        if include_address:
            data['address'] = self.address
        
        return data
    
    def to_summary(self, include_phone=False, include_address=False):
        """Return a summary for match previews (limited info)."""
        data = {
            'id': self.id,
            'full_name': self.full_name,
            'neighborhood': self.neighborhood,
            'languages': self.languages,
            'kosher_level': self.kosher_level,
            'contribution_preference': self.contribution_preference,
            'vibe_chabad': self.vibe_chabad,
            'vibe_social': self.vibe_social,
            'vibe_formality': self.vibe_formality,
            'tagline': self.tagline
        }
        
        if include_phone:
            data['phone'] = self.phone
        
        if include_address:
            data['address'] = self.address
        
        return data
    
    def get_remaining_capacity(self):
        """Calculate remaining seat capacity based on confirmed matches."""
        from app.models.match import Match
        from app.config import MatchStatus
        
        # Count seats taken by accepted/confirmed matches
        active_matches = Match.query.filter(
            Match.host_id == self.id,
            Match.status.in_([MatchStatus.ACCEPTED.value, MatchStatus.CONFIRMED.value, MatchStatus.REQUESTED.value, MatchStatus.PROPOSED.value])
        ).all()
        
        seats_taken = sum(m.guest.party_size for m in active_matches)
        return self.seats_available - seats_taken
