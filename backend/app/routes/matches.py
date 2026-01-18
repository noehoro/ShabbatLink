"""Match response API endpoints (uses signed action tokens)."""
from datetime import datetime
from flask import Blueprint, request
from app import db
from app.models import Match, ActivityLog
from app.utils.responses import success_response, error_response
from app.utils.tokens import verify_action_token
from app.config import MatchStatus, ActivityType

matches_bp = Blueprint('matches', __name__)


@matches_bp.route('/respond', methods=['POST'])
def respond_to_match():
    """
    Accept or decline a match using signed action token.
    
    This is used by hosts when they click the accept/decline link in their email.
    No login required - the signed token authenticates the action.
    """
    data = request.get_json()
    token = data.get('token', '').strip()
    
    if not token:
        return error_response("Token is required")
    
    # Verify the action token
    token_data = verify_action_token(token)
    if not token_data:
        return error_response("Invalid or expired link", status_code=401)
    
    action = token_data['action']
    match_id = token_data['target_id']
    
    # Validate action type
    if action not in ['match_accept', 'match_decline']:
        return error_response("Invalid action", status_code=400)
    
    # Find the match
    match = Match.query.get(match_id)
    if not match:
        return error_response("Match not found", status_code=404)
    
    # Verify match is in correct state
    if match.status != MatchStatus.REQUESTED.value:
        if match.status == MatchStatus.ACCEPTED.value:
            return success_response(
                message="You've already accepted this guest request.",
                data={'status': 'already_accepted'}
            )
        elif match.status == MatchStatus.DECLINED.value:
            return success_response(
                message="You've already declined this guest request.",
                data={'status': 'already_declined'}
            )
        elif match.status == MatchStatus.CONFIRMED.value:
            return success_response(
                message="This match has already been finalized.",
                data={'status': 'already_confirmed'}
            )
        else:
            return error_response("This request is no longer available", status_code=400)
    
    # Process the response
    if action == 'match_accept':
        match.status = MatchStatus.ACCEPTED.value
        match.responded_at = datetime.utcnow()
        db.session.commit()
        
        # Log activity
        ActivityLog.log(
            ActivityType.MATCH_ACCEPTED.value,
            actor='host',
            target_type='match',
            target_id=match.id,
            details={'host_id': match.host_id, 'guest_id': match.guest_id}
        )
        db.session.commit()
        
        # Note: We do NOT notify the guest here. Admin must finalize first.
        
        return success_response(
            message="Thank you! You've accepted this guest. We'll finalize and send you the details soon.",
            data={
                'status': 'accepted',
                'guest_name': match.guest.full_name,
                'party_size': match.guest.party_size
            }
        )
    
    else:  # match_decline
        match.status = MatchStatus.DECLINED.value
        match.responded_at = datetime.utcnow()
        db.session.commit()
        
        # Log activity
        ActivityLog.log(
            ActivityType.MATCH_DECLINED.value,
            actor='host',
            target_type='match',
            target_id=match.id,
            details={'host_id': match.host_id, 'guest_id': match.guest_id}
        )
        db.session.commit()
        
        return success_response(
            message="No problem! We'll find another host for this guest.",
            data={'status': 'declined'}
        )


@matches_bp.route('/details/<match_id>', methods=['GET'])
def get_match_details_for_response(match_id):
    """
    Get match details for the response page.
    Uses signed token for authentication.
    """
    token = request.args.get('token', '').strip()
    
    if not token:
        return error_response("Token is required", status_code=401)
    
    # Verify the action token
    token_data = verify_action_token(token)
    if not token_data:
        return error_response("Invalid or expired link", status_code=401)
    
    # Verify token is for this match
    if token_data['target_id'] != match_id:
        return error_response("Invalid token for this match", status_code=401)
    
    # Find the match
    match = Match.query.get(match_id)
    if not match:
        return error_response("Match not found", status_code=404)
    
    # Return match details (guest summary only, no contact info)
    return success_response(data={
        'match': match.to_dict(include_guest_details=True),
        'status': match.status
    })
