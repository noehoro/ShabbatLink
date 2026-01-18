"""Host API endpoints."""
from flask import Blueprint, request
from app import db
from app.models import Host, ActivityLog
from app.services.email_service import EmailService
from app.utils.responses import success_response, error_response
from app.utils.tokens import verify_session_token
from app.config import ActivityType

hosts_bp = Blueprint('hosts', __name__)


def validate_host_data(data, is_update=False):
    """Validate host registration data."""
    errors = []
    
    if not is_update:
        required_fields = [
            'full_name', 'email', 'phone', 'neighborhood', 'address',
            'seats_available', 'languages', 'kosher_level',
            'contribution_preference', 'vibe_chabad', 'vibe_social', 'vibe_formality',
            'no_show_acknowledged'
        ]
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(f"Missing required field: {field}")
    
    if 'seats_available' in data and (data['seats_available'] < 1 or data['seats_available'] > 50):
        errors.append("Seats available must be between 1 and 50")
    
    if 'languages' in data and not isinstance(data['languages'], list):
        errors.append("Languages must be a list")
    
    for vibe in ['vibe_chabad', 'vibe_social', 'vibe_formality']:
        if vibe in data and (data[vibe] < 1 or data[vibe] > 5):
            errors.append(f"{vibe} must be between 1 and 5")
    
    if not is_update and 'no_show_acknowledged' in data and not data['no_show_acknowledged']:
        errors.append("You must acknowledge the no-show policy")
    
    return errors


@hosts_bp.route('', methods=['POST'])
def create_host():
    """Create a new host registration."""
    data = request.get_json()
    
    # Validate data
    errors = validate_host_data(data)
    if errors:
        return error_response("Validation failed", errors=errors)
    
    # Check for existing email
    existing = Host.query.filter_by(email=data['email']).first()
    if existing:
        return error_response(
            "An account with this email already exists. Use the login link to edit your profile.",
            status_code=409
        )
    
    # Create host
    host = Host(
        full_name=data['full_name'],
        email=data['email'],
        phone=data['phone'],
        neighborhood=data['neighborhood'],
        address=data['address'],
        seats_available=data['seats_available'],
        languages=data['languages'],
        kosher_level=data['kosher_level'],
        contribution_preference=data['contribution_preference'],
        vibe_chabad=data['vibe_chabad'],
        vibe_social=data['vibe_social'],
        vibe_formality=data['vibe_formality'],
        tagline=data.get('tagline'),
        private_notes=data.get('private_notes'),
        no_show_acknowledged=data['no_show_acknowledged']
    )
    
    db.session.add(host)
    db.session.commit()
    
    # Log activity
    ActivityLog.log(
        ActivityType.HOST_REGISTERED.value,
        actor='host',
        target_type='host',
        target_id=host.id,
        details={'email': host.email, 'name': host.full_name}
    )
    db.session.commit()
    
    # Send confirmation email
    EmailService.send_host_submission_confirmation(host)
    
    return success_response(
        data={'id': host.id},
        message="Registration successful! Check your email for confirmation.",
        status_code=201
    )


@hosts_bp.route('/<host_id>', methods=['GET'])
def get_host(host_id):
    """Get host details (requires auth)."""
    # Check authorization
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return error_response("Authorization required", status_code=401)
    
    token = auth_header.split(' ')[1]
    session = verify_session_token(token, expected_type='host')
    
    if not session or session['user_id'] != host_id:
        return error_response("Unauthorized", status_code=401)
    
    host = Host.query.get(host_id)
    if not host:
        return error_response("Host not found", status_code=404)
    
    return success_response(data=host.to_dict(include_private=True, include_address=True))


@hosts_bp.route('/<host_id>', methods=['PUT'])
def update_host(host_id):
    """Update host profile (requires auth)."""
    # Check authorization
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return error_response("Authorization required", status_code=401)
    
    token = auth_header.split(' ')[1]
    session = verify_session_token(token, expected_type='host')
    
    if not session or session['user_id'] != host_id:
        return error_response("Unauthorized", status_code=401)
    
    host = Host.query.get(host_id)
    if not host:
        return error_response("Host not found", status_code=404)
    
    data = request.get_json()
    
    # Validate data
    errors = validate_host_data(data, is_update=True)
    if errors:
        return error_response("Validation failed", errors=errors)
    
    # Update allowed fields
    updatable_fields = [
        'full_name', 'phone', 'neighborhood', 'address', 'seats_available',
        'languages', 'kosher_level', 'contribution_preference',
        'vibe_chabad', 'vibe_social', 'vibe_formality', 'tagline'
    ]
    
    for field in updatable_fields:
        if field in data:
            setattr(host, field, data[field])
    
    db.session.commit()
    
    # Log activity
    ActivityLog.log(
        ActivityType.HOST_UPDATED.value,
        actor='host',
        target_type='host',
        target_id=host.id,
        details={'updated_fields': list(data.keys())}
    )
    db.session.commit()
    
    return success_response(
        data=host.to_dict(include_private=True, include_address=True),
        message="Profile updated successfully"
    )
