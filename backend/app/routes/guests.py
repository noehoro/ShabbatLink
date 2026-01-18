"""Guest API endpoints."""
from flask import Blueprint, request
from app import db
from app.models import Guest, ActivityLog
from app.services.email_service import EmailService
from app.utils.responses import success_response, error_response
from app.utils.tokens import verify_session_token
from app.config import ActivityType

guests_bp = Blueprint('guests', __name__)


def validate_guest_data(data, is_update=False):
    """Validate guest registration data."""
    errors = []
    
    if not is_update:
        required_fields = [
            'full_name', 'email', 'phone', 'gender', 'party_size', 'neighborhood',
            'max_travel_time', 'languages', 'kosher_requirement',
            'contribution_range', 'vibe_chabad', 'vibe_social', 'vibe_formality',
            'no_show_acknowledged'
        ]
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                errors.append(f"Missing required field: {field}")
    
    if 'party_size' in data and (data['party_size'] < 1 or data['party_size'] > 10):
        errors.append("Party size must be between 1 and 10")
    
    if 'max_travel_time' in data and data['max_travel_time'] not in [15, 30, 45, 60, 999]:
        errors.append("Max travel time must be 15, 30, 45, 60 minutes, or 999 for 'Distance doesn't matter'")
    
    if 'languages' in data and not isinstance(data['languages'], list):
        errors.append("Languages must be a list")
    
    for vibe in ['vibe_chabad', 'vibe_social', 'vibe_formality']:
        if vibe in data and (data[vibe] < 1 or data[vibe] > 5):
            errors.append(f"{vibe} must be between 1 and 5")
    
    if not is_update and 'no_show_acknowledged' in data and not data['no_show_acknowledged']:
        errors.append("You must acknowledge the no-show policy")
    
    return errors


@guests_bp.route('', methods=['POST'])
def create_guest():
    """Create a new guest registration."""
    data = request.get_json()
    
    # Validate data
    errors = validate_guest_data(data)
    if errors:
        return error_response("Validation failed", errors=errors)
    
    # Check for existing email
    existing = Guest.query.filter_by(email=data['email']).first()
    if existing:
        return error_response(
            "An account with this email already exists. Use the login link to edit your profile.",
            status_code=409
        )
    
    # Create guest
    guest = Guest(
        full_name=data['full_name'],
        email=data['email'],
        phone=data['phone'],
        gender=data['gender'],
        party_size=data['party_size'],
        neighborhood=data['neighborhood'],
        max_travel_time=data['max_travel_time'],
        languages=data['languages'],
        kosher_requirement=data['kosher_requirement'],
        contribution_range=data['contribution_range'],
        vibe_chabad=data['vibe_chabad'],
        vibe_social=data['vibe_social'],
        vibe_formality=data['vibe_formality'],
        attended_jlc_before=data.get('attended_jlc_before', False),
        facebook_url=data.get('facebook_url'),
        instagram_handle=data.get('instagram_handle'),
        notes_to_admin=data.get('notes_to_admin'),
        no_show_acknowledged=data['no_show_acknowledged']
    )
    
    db.session.add(guest)
    db.session.commit()
    
    # Log activity
    ActivityLog.log(
        ActivityType.GUEST_REGISTERED.value,
        actor='guest',
        target_type='guest',
        target_id=guest.id,
        details={'email': guest.email, 'name': guest.full_name}
    )
    db.session.commit()
    
    # Send confirmation email
    EmailService.send_guest_submission_confirmation(guest)
    
    return success_response(
        data={'id': guest.id},
        message="Registration successful! Check your email for confirmation.",
        status_code=201
    )


@guests_bp.route('/<guest_id>', methods=['GET'])
def get_guest(guest_id):
    """Get guest details (requires auth)."""
    # Check authorization
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return error_response("Authorization required", status_code=401)
    
    token = auth_header.split(' ')[1]
    session = verify_session_token(token, expected_type='guest')
    
    if not session or session['user_id'] != guest_id:
        return error_response("Unauthorized", status_code=401)
    
    guest = Guest.query.get(guest_id)
    if not guest:
        return error_response("Guest not found", status_code=404)
    
    return success_response(data=guest.to_dict(include_private=True))


@guests_bp.route('/<guest_id>', methods=['PUT'])
def update_guest(guest_id):
    """Update guest profile (requires auth)."""
    # Check authorization
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return error_response("Authorization required", status_code=401)
    
    token = auth_header.split(' ')[1]
    session = verify_session_token(token, expected_type='guest')
    
    if not session or session['user_id'] != guest_id:
        return error_response("Unauthorized", status_code=401)
    
    guest = Guest.query.get(guest_id)
    if not guest:
        return error_response("Guest not found", status_code=404)
    
    data = request.get_json()
    
    # Validate data
    errors = validate_guest_data(data, is_update=True)
    if errors:
        return error_response("Validation failed", errors=errors)
    
    # Update allowed fields
    updatable_fields = [
        'full_name', 'phone', 'gender', 'party_size', 'neighborhood', 'max_travel_time',
        'languages', 'kosher_requirement', 'contribution_range',
        'vibe_chabad', 'vibe_social', 'vibe_formality', 
        'attended_jlc_before', 'facebook_url', 'instagram_handle', 'notes_to_admin'
    ]
    
    for field in updatable_fields:
        if field in data:
            setattr(guest, field, data[field])
    
    db.session.commit()
    
    # Log activity
    ActivityLog.log(
        ActivityType.GUEST_UPDATED.value,
        actor='guest',
        target_type='guest',
        target_id=guest.id,
        details={'updated_fields': list(data.keys())}
    )
    db.session.commit()
    
    return success_response(
        data=guest.to_dict(include_private=True),
        message="Profile updated successfully"
    )
