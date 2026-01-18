"""Authentication API endpoints."""
from flask import Blueprint, request, current_app
from app import db
from app.models import Guest, Host, MagicLink
from app.services.email_service import EmailService
from app.utils.responses import success_response, error_response
from app.utils.tokens import generate_session_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/request-link', methods=['POST'])
def request_magic_link():
    """Request a magic link for profile editing."""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if not email:
        return error_response("Email is required")
    
    # Look up user (check both guests and hosts)
    guest = Guest.query.filter_by(email=email).first()
    host = Host.query.filter_by(email=email).first()
    
    if not guest and not host:
        # Don't reveal if email exists or not for security
        return success_response(
            message="If an account exists with this email, a login link will be sent."
        )
    
    # Determine user type and create magic link
    if guest:
        user_type = 'guest'
        user_id = guest.id
        user_name = guest.full_name
    else:
        user_type = 'host'
        user_id = host.id
        user_name = host.full_name
    
    # Create magic link
    magic_link = MagicLink.create_for_user(email, user_type, user_id)
    db.session.add(magic_link)
    db.session.commit()
    
    # Build link URL
    frontend_url = current_app.config['FRONTEND_URL']
    link_url = f"{frontend_url}/auth/verify?token={magic_link.token}"
    
    # Send email
    EmailService.send_magic_link(email, user_name, user_type, link_url)
    
    return success_response(
        message="If an account exists with this email, a login link will be sent."
    )


@auth_bp.route('/verify', methods=['POST'])
def verify_magic_link():
    """Verify a magic link token and return a session."""
    data = request.get_json()
    token = data.get('token', '').strip()
    
    if not token:
        return error_response("Token is required")
    
    # Find magic link
    magic_link = MagicLink.query.filter_by(token=token).first()
    
    if not magic_link:
        return error_response("Invalid or expired link", status_code=401)
    
    if not magic_link.is_valid():
        return error_response("This link has expired. Please request a new one.", status_code=401)
    
    # Mark as used
    magic_link.mark_used()
    db.session.commit()
    
    # Generate session token
    session_token = generate_session_token(magic_link.user_type, magic_link.user_id)
    
    # Get user info
    if magic_link.user_type == 'guest':
        user = Guest.query.get(magic_link.user_id)
        user_data = user.to_dict(include_private=True)
    else:
        user = Host.query.get(magic_link.user_id)
        user_data = user.to_dict(include_private=True, include_address=True)
    
    return success_response(data={
        'token': session_token,
        'user_type': magic_link.user_type,
        'user': user_data
    })
