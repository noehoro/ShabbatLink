"""Attendance confirmation and no-show reporting endpoints."""
from datetime import datetime
from flask import Blueprint, request
from app import db
from app.models import Match, Guest, Host, ActivityLog
from app.utils.responses import success_response, error_response
from app.utils.tokens import verify_action_token
from app.config import MatchStatus, ActivityType

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/confirm', methods=['POST'])
def confirm_attendance():
    """
    Guest confirms attendance using signed token from day-of reminder email.
    No login required.
    """
    data = request.get_json()
    token = data.get('token', '').strip()
    
    if not token:
        return error_response("Token is required")
    
    # Verify the action token
    token_data = verify_action_token(token)
    if not token_data:
        return error_response("Invalid or expired link", status_code=401)
    
    if token_data['action'] != 'confirm_attendance':
        return error_response("Invalid token type", status_code=400)
    
    match_id = token_data['target_id']
    
    # Find the match
    match = Match.query.get(match_id)
    if not match:
        return error_response("Match not found", status_code=404)
    
    # Verify match is confirmed
    if match.status != MatchStatus.CONFIRMED.value:
        return error_response("This match is not in confirmed status", status_code=400)
    
    # Check if already confirmed
    if match.guest_confirmed_at:
        return success_response(
            message="You've already confirmed your attendance. See you tonight!",
            data={'already_confirmed': True}
        )
    
    # Mark attendance confirmed
    match.guest_confirmed_at = datetime.utcnow()
    db.session.commit()
    
    # Log activity
    ActivityLog.log(
        ActivityType.GUEST_CONFIRMED_ATTENDANCE.value,
        actor='guest',
        target_type='match',
        target_id=match.id,
        details={'guest_id': match.guest_id, 'host_id': match.host_id}
    )
    db.session.commit()
    
    # Return host details for the confirmation page
    host = match.host
    return success_response(
        message="Thank you for confirming! Have a wonderful Shabbat dinner!",
        data={
            'confirmed': True,
            'host_name': host.full_name,
            'host_address': host.address,
            'host_phone': host.phone
        }
    )


@attendance_bp.route('/noshow/report', methods=['GET'])
def get_noshow_report_form():
    """
    Get the list of guests that a host can report as no-shows.
    Uses signed token to identify the host.
    """
    token = request.args.get('token', '').strip()
    
    if not token:
        return error_response("Token is required", status_code=401)
    
    # Verify the action token
    token_data = verify_action_token(token)
    if not token_data:
        return error_response("Invalid or expired link", status_code=401)
    
    if token_data['action'] != 'noshow_report':
        return error_response("Invalid token type", status_code=400)
    
    host_id = token_data['target_id']
    
    # Find the host
    host = Host.query.get(host_id)
    if not host:
        return error_response("Host not found", status_code=404)
    
    # Get all confirmed matches for this host (only those who confirmed attendance)
    confirmed_matches = Match.query.filter(
        Match.host_id == host_id,
        Match.status == MatchStatus.CONFIRMED.value,
        Match.guest_confirmed_at.isnot(None),
        Match.guest_no_show == False
    ).all()
    
    # Return list of guests that can be reported
    guests = []
    for match in confirmed_matches:
        guests.append({
            'match_id': match.id,
            'guest_name': match.guest.full_name,
            'party_size': match.guest.party_size
        })
    
    return success_response(data={
        'host_name': host.full_name,
        'guests': guests
    })


@attendance_bp.route('/noshow/report', methods=['POST'])
def submit_noshow_report():
    """
    Host submits no-show report for guests who didn't show up.
    Uses signed token to identify the host.
    """
    data = request.get_json()
    token = data.get('token', '').strip()
    no_show_match_ids = data.get('no_show_match_ids', [])
    
    if not token:
        return error_response("Token is required")
    
    # Verify the action token
    token_data = verify_action_token(token)
    if not token_data:
        return error_response("Invalid or expired link", status_code=401)
    
    if token_data['action'] != 'noshow_report':
        return error_response("Invalid token type", status_code=400)
    
    host_id = token_data['target_id']
    
    # Find the host
    host = Host.query.get(host_id)
    if not host:
        return error_response("Host not found", status_code=404)
    
    # Process each reported no-show
    reported_count = 0
    for match_id in no_show_match_ids:
        match = Match.query.get(match_id)
        
        # Security: Verify this match belongs to this host
        if not match or match.host_id != host_id:
            continue
        
        # Only process confirmed matches
        if match.status != MatchStatus.CONFIRMED.value:
            continue
        
        # Skip if already reported
        if match.guest_no_show:
            continue
        
        # Mark as no-show
        match.guest_no_show = True
        match.no_show_reported_at = datetime.utcnow()
        
        # Increment guest's no-show count
        guest = match.guest
        guest.no_show_count += 1
        
        # Log activity
        ActivityLog.log(
            ActivityType.NOSHOW_REPORTED.value,
            actor='host',
            target_type='match',
            target_id=match.id,
            details={
                'host_id': host_id,
                'guest_id': guest.id,
                'guest_name': guest.full_name,
                'new_no_show_count': guest.no_show_count
            }
        )
        
        reported_count += 1
    
    db.session.commit()
    
    if reported_count > 0:
        return success_response(
            message=f"Thank you for reporting. {reported_count} no-show(s) recorded.",
            data={'reported_count': reported_count}
        )
    else:
        return success_response(
            message="No new no-shows to report.",
            data={'reported_count': 0}
        )
