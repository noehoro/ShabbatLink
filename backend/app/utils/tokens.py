"""Token generation and verification utilities.

THREE TOKEN TYPES:
1. Admin Session Token - for admin panel access
2. Magic Link Token - for profile editing (stored in DB)
3. Signed Action Token - for one-click actions (stateless, HMAC-signed)
"""
import hmac
import hashlib
import base64
import json
import secrets
from datetime import datetime, timedelta
from flask import current_app


def generate_action_token(action_type, target_id, expires_hours=72):
    """
    Generate a signed action token for one-click actions.
    
    Used for: match accept/decline, attendance confirm, no-show report
    These are stateless - no database storage needed.
    
    Args:
        action_type: Type of action (e.g., 'match_accept', 'match_decline', 'confirm_attendance')
        target_id: ID of the target entity (e.g., match_id, host_id)
        expires_hours: Hours until expiration (default 72 hours)
    
    Returns:
        Base64-encoded signed token string
    """
    expires_at = datetime.utcnow() + timedelta(hours=expires_hours)
    
    payload = {
        'action': action_type,
        'target_id': target_id,
        'exp': expires_at.isoformat()
    }
    
    payload_json = json.dumps(payload, sort_keys=True)
    payload_b64 = base64.urlsafe_b64encode(payload_json.encode()).decode()
    
    # Create signature using HMAC-SHA256
    secret_key = current_app.config['SECRET_KEY']
    signature = hmac.new(
        secret_key.encode(),
        payload_b64.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Combine payload and signature
    token = f"{payload_b64}.{signature}"
    return token


def verify_action_token(token):
    """
    Verify a signed action token.
    
    Args:
        token: The token string to verify
    
    Returns:
        dict with 'action' and 'target_id' if valid, None if invalid
    """
    try:
        parts = token.split('.')
        if len(parts) != 2:
            return None
        
        payload_b64, provided_signature = parts
        
        # Verify signature
        secret_key = current_app.config['SECRET_KEY']
        expected_signature = hmac.new(
            secret_key.encode(),
            payload_b64.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(provided_signature, expected_signature):
            return None
        
        # Decode payload
        payload_json = base64.urlsafe_b64decode(payload_b64.encode()).decode()
        payload = json.loads(payload_json)
        
        # Check expiration
        expires_at = datetime.fromisoformat(payload['exp'])
        if datetime.utcnow() > expires_at:
            return None
        
        return {
            'action': payload['action'],
            'target_id': payload['target_id']
        }
    except Exception:
        return None


def generate_session_token(user_type, user_id, expires_hours=24):
    """
    Generate a session token for authenticated users.
    
    Used for: Admin sessions, magic link sessions for profile editing.
    
    Args:
        user_type: Type of user ('admin', 'guest', 'host')
        user_id: ID of the user (or 'admin' for admin sessions)
        expires_hours: Hours until expiration
    
    Returns:
        Base64-encoded signed token string
    """
    expires_at = datetime.utcnow() + timedelta(hours=expires_hours)
    
    payload = {
        'type': user_type,
        'user_id': user_id,
        'exp': expires_at.isoformat(),
        'nonce': secrets.token_hex(8)  # Add randomness
    }
    
    payload_json = json.dumps(payload, sort_keys=True)
    payload_b64 = base64.urlsafe_b64encode(payload_json.encode()).decode()
    
    secret_key = current_app.config['SECRET_KEY']
    signature = hmac.new(
        secret_key.encode(),
        payload_b64.encode(),
        hashlib.sha256
    ).hexdigest()
    
    token = f"{payload_b64}.{signature}"
    return token


def verify_session_token(token, expected_type=None):
    """
    Verify a session token.
    
    Args:
        token: The token string to verify
        expected_type: If provided, verify the user type matches
    
    Returns:
        dict with 'type' and 'user_id' if valid, None if invalid
    """
    try:
        parts = token.split('.')
        if len(parts) != 2:
            return None
        
        payload_b64, provided_signature = parts
        
        secret_key = current_app.config['SECRET_KEY']
        expected_signature = hmac.new(
            secret_key.encode(),
            payload_b64.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(provided_signature, expected_signature):
            return None
        
        payload_json = base64.urlsafe_b64decode(payload_b64.encode()).decode()
        payload = json.loads(payload_json)
        
        expires_at = datetime.fromisoformat(payload['exp'])
        if datetime.utcnow() > expires_at:
            return None
        
        if expected_type and payload['type'] != expected_type:
            return None
        
        return {
            'type': payload['type'],
            'user_id': payload['user_id']
        }
    except Exception:
        return None
