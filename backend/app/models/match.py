"""Match model for guest-host pairings."""
import uuid
from datetime import datetime
from app import db
from app.config import MatchStatus


class Match(db.Model):
    """Match model - a pairing between a guest and host."""
    __tablename__ = 'matches'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign keys
    guest_id = db.Column(db.String(36), db.ForeignKey('guests.id'), nullable=False)
    host_id = db.Column(db.String(36), db.ForeignKey('hosts.id'), nullable=False)
    
    # Match details
    status = db.Column(db.String(20), nullable=False, default=MatchStatus.PROPOSED.value)
    match_score = db.Column(db.Float, nullable=True)
    why_its_a_fit = db.Column(db.Text, nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)
    
    # Status timestamps
    requested_at = db.Column(db.DateTime, nullable=True)  # When sent to host
    responded_at = db.Column(db.DateTime, nullable=True)  # When host accepted/declined
    finalized_at = db.Column(db.DateTime, nullable=True)  # When admin confirmed
    
    # Attendance tracking (per match, not on guest)
    guest_confirmed_at = db.Column(db.DateTime, nullable=True)  # Day-of confirmation
    guest_no_show = db.Column(db.Boolean, nullable=False, default=False)
    no_show_reported_at = db.Column(db.DateTime, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self, include_guest_details=False, include_host_details=False, reveal_contact=False):
        """Convert to dictionary for API responses."""
        data = {
            'id': self.id,
            'guest_id': self.guest_id,
            'host_id': self.host_id,
            'status': self.status,
            'match_score': self.match_score,
            'why_its_a_fit': self.why_its_a_fit,
            'admin_notes': self.admin_notes,
            'requested_at': self.requested_at.isoformat() if self.requested_at else None,
            'responded_at': self.responded_at.isoformat() if self.responded_at else None,
            'finalized_at': self.finalized_at.isoformat() if self.finalized_at else None,
            'guest_confirmed_at': self.guest_confirmed_at.isoformat() if self.guest_confirmed_at else None,
            'guest_no_show': self.guest_no_show,
            'no_show_reported_at': self.no_show_reported_at.isoformat() if self.no_show_reported_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_guest_details:
            if reveal_contact:
                data['guest'] = self.guest.to_dict(include_private=True)
            else:
                data['guest'] = self.guest.to_summary()
        
        if include_host_details:
            if reveal_contact:
                data['host'] = self.host.to_dict(include_private=True, include_address=True)
            else:
                data['host'] = self.host.to_summary()
        
        return data
