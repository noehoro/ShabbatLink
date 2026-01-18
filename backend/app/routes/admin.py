"""Admin API endpoints."""
from datetime import datetime
from functools import wraps
from flask import Blueprint, request, current_app
from app import db
from app.models import Guest, Host, Match, Email, ActivityLog
from app.services.email_service import EmailService
from app.utils.responses import success_response, error_response
from app.utils.tokens import generate_session_token, verify_session_token, generate_action_token
from app.config import MatchStatus, ActivityType

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """Decorator to require admin authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return error_response("Authorization required", status_code=401)
        
        token = auth_header.split(' ')[1]
        session = verify_session_token(token, expected_type='admin')
        
        if not session:
            return error_response("Invalid or expired session", status_code=401)
        
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/auth', methods=['POST'])
def admin_login():
    """Admin login with password."""
    data = request.get_json()
    password = data.get('password', '')
    
    if password != current_app.config['ADMIN_PASSWORD']:
        return error_response("Invalid password", status_code=401)
    
    # Generate admin session token
    token = generate_session_token('admin', 'admin', expires_hours=24)
    
    return success_response(data={'token': token}, message="Login successful")


@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard():
    """Get dashboard statistics and alerts."""
    # Count totals
    total_guests = Guest.query.count()
    total_hosts = Host.query.count()
    total_seats = db.session.query(db.func.sum(Host.seats_available)).scalar() or 0
    
    # Count by match status
    guests_with_match = db.session.query(Match.guest_id).filter(
        Match.status.in_([
            MatchStatus.PROPOSED.value,
            MatchStatus.REQUESTED.value,
            MatchStatus.ACCEPTED.value,
            MatchStatus.CONFIRMED.value
        ])
    ).distinct().count()
    
    pending_decisions = Match.query.filter(
        Match.status == MatchStatus.REQUESTED.value
    ).count()
    
    confirmed_matches = Match.query.filter(
        Match.status == MatchStatus.CONFIRMED.value
    ).count()
    
    accepted_awaiting = Match.query.filter(
        Match.status == MatchStatus.ACCEPTED.value
    ).count()
    
    # Calculate alerts
    alerts = []
    
    # Unmatched guests
    matched_guest_ids = db.session.query(Match.guest_id).filter(
        Match.status.in_([
            MatchStatus.PROPOSED.value,
            MatchStatus.REQUESTED.value,
            MatchStatus.ACCEPTED.value,
            MatchStatus.CONFIRMED.value
        ])
    ).distinct()
    
    unmatched_guests = Guest.query.filter(
        ~Guest.id.in_(matched_guest_ids)
    ).count()
    
    if unmatched_guests > 0:
        alerts.append({
            'type': 'warning',
            'message': f"{unmatched_guests} guest(s) not yet matched"
        })
    
    # Strict kosher unmatched
    strict_kosher_unmatched = Guest.query.filter(
        Guest.kosher_requirement == 'Full kosher only',
        ~Guest.id.in_(matched_guest_ids)
    ).count()
    
    if strict_kosher_unmatched > 0:
        alerts.append({
            'type': 'error',
            'message': f"{strict_kosher_unmatched} strict kosher guest(s) unmatched"
        })
    
    # Hosts with unused capacity
    hosts_with_capacity = []
    for host in Host.query.all():
        remaining = host.get_remaining_capacity()
        if remaining > 0:
            hosts_with_capacity.append(host.full_name)
    
    if hosts_with_capacity:
        alerts.append({
            'type': 'info',
            'message': f"{len(hosts_with_capacity)} host(s) have unused capacity"
        })
    
    # Accepted matches awaiting finalization
    if accepted_awaiting > 0:
        alerts.append({
            'type': 'info',
            'message': f"{accepted_awaiting} match(es) accepted, awaiting finalization"
        })
    
    return success_response(data={
        'stats': {
            'total_guests': total_guests,
            'total_hosts': total_hosts,
            'total_seats': total_seats,
            'guests_placed': guests_with_match,
            'pending_decisions': pending_decisions,
            'confirmed_matches': confirmed_matches,
            'accepted_awaiting': accepted_awaiting
        },
        'alerts': alerts
    })


@admin_bp.route('/guests', methods=['GET'])
@admin_required
def list_guests():
    """List all guests with optional filtering."""
    status_filter = request.args.get('status')
    
    guests = Guest.query.order_by(Guest.created_at.desc()).all()
    
    result = []
    for guest in guests:
        guest_data = guest.to_dict(include_private=True)
        
        # Get current match status
        current_match = Match.query.filter(
            Match.guest_id == guest.id,
            Match.status.in_([
                MatchStatus.PROPOSED.value,
                MatchStatus.REQUESTED.value,
                MatchStatus.ACCEPTED.value,
                MatchStatus.CONFIRMED.value
            ])
        ).first()
        
        guest_data['match_status'] = current_match.status if current_match else 'unmatched'
        guest_data['match_id'] = current_match.id if current_match else None
        
        # Filter by status if requested
        if status_filter:
            if status_filter == 'unmatched' and current_match:
                continue
            elif status_filter != 'unmatched' and (not current_match or current_match.status != status_filter):
                continue
        
        result.append(guest_data)
    
    return success_response(data=result)


@admin_bp.route('/guests/<guest_id>', methods=['GET'])
@admin_required
def get_guest_detail(guest_id):
    """Get detailed guest information."""
    guest = Guest.query.get(guest_id)
    if not guest:
        return error_response("Guest not found", status_code=404)
    
    guest_data = guest.to_dict(include_private=True)
    
    # Get match history
    matches = Match.query.filter_by(guest_id=guest_id).order_by(Match.created_at.desc()).all()
    guest_data['matches'] = [m.to_dict(include_host_details=True) for m in matches]
    
    return success_response(data=guest_data)


@admin_bp.route('/guests/<guest_id>/flag', methods=['POST'])
@admin_required
def flag_guest(guest_id):
    """Flag a guest for no-show or other issues."""
    guest = Guest.query.get(guest_id)
    if not guest:
        return error_response("Guest not found", status_code=404)
    
    data = request.get_json() or {}
    
    guest.is_flagged = True
    if data.get('increment_noshow', False):
        guest.no_show_count += 1
    
    db.session.commit()
    
    ActivityLog.log(
        ActivityType.GUEST_FLAGGED.value,
        actor='admin',
        target_type='guest',
        target_id=guest.id,
        details={'reason': data.get('reason', 'Manual flag by admin')}
    )
    db.session.commit()
    
    return success_response(
        message="Guest flagged successfully",
        data=guest.to_dict(include_private=True)
    )


@admin_bp.route('/hosts', methods=['GET'])
@admin_required
def list_hosts():
    """List all hosts with capacity info."""
    hosts = Host.query.order_by(Host.created_at.desc()).all()
    
    result = []
    for host in hosts:
        host_data = host.to_dict(include_private=True, include_address=True)
        host_data['remaining_capacity'] = host.get_remaining_capacity()
        
        # Count matches by status
        host_data['match_counts'] = {
            'proposed': Match.query.filter_by(host_id=host.id, status=MatchStatus.PROPOSED.value).count(),
            'requested': Match.query.filter_by(host_id=host.id, status=MatchStatus.REQUESTED.value).count(),
            'accepted': Match.query.filter_by(host_id=host.id, status=MatchStatus.ACCEPTED.value).count(),
            'confirmed': Match.query.filter_by(host_id=host.id, status=MatchStatus.CONFIRMED.value).count()
        }
        
        result.append(host_data)
    
    return success_response(data=result)


@admin_bp.route('/hosts/<host_id>', methods=['GET'])
@admin_required
def get_host_detail(host_id):
    """Get detailed host information."""
    host = Host.query.get(host_id)
    if not host:
        return error_response("Host not found", status_code=404)
    
    host_data = host.to_dict(include_private=True, include_address=True)
    host_data['remaining_capacity'] = host.get_remaining_capacity()
    
    # Get all matches for this host
    matches = Match.query.filter_by(host_id=host_id).order_by(Match.created_at.desc()).all()
    host_data['matches'] = [m.to_dict(include_guest_details=True, reveal_contact=True) for m in matches]
    
    return success_response(data=host_data)


@admin_bp.route('/matches', methods=['GET'])
@admin_required
def list_matches():
    """List all matches with optional status filter."""
    status_filter = request.args.get('status')
    
    query = Match.query.order_by(Match.created_at.desc())
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    matches = query.all()
    
    result = [m.to_dict(include_guest_details=True, include_host_details=True, reveal_contact=True) for m in matches]
    
    return success_response(data=result)


@admin_bp.route('/matches/generate', methods=['POST'])
@admin_required
def generate_matches():
    """Run the matching algorithm to generate proposed matches."""
    from app.services.matching_adapter import run_matching
    
    # Clear existing proposed matches
    Match.query.filter_by(status=MatchStatus.PROPOSED.value).delete()
    db.session.commit()
    
    # Run matching
    result = run_matching()
    
    # Log activity
    ActivityLog.log(
        ActivityType.MATCHES_GENERATED.value,
        actor='admin',
        target_type=None,
        target_id=None,
        details={
            'matches_created': result['matches_created'],
            'unmatched_guests': len(result['unmatched_guests'])
        }
    )
    db.session.commit()
    
    return success_response(
        message=f"Generated {result['matches_created']} matches",
        data=result
    )


@admin_bp.route('/matches/<match_id>', methods=['PUT'])
@admin_required
def edit_match(match_id):
    """Edit a match (reassign host)."""
    match = Match.query.get(match_id)
    if not match:
        return error_response("Match not found", status_code=404)
    
    # Only allow editing proposed matches
    if match.status != MatchStatus.PROPOSED.value:
        return error_response("Can only edit proposed matches", status_code=400)
    
    data = request.get_json()
    new_host_id = data.get('host_id')
    
    if not new_host_id:
        return error_response("New host_id is required")
    
    new_host = Host.query.get(new_host_id)
    if not new_host:
        return error_response("Host not found", status_code=404)
    
    # Check capacity
    if new_host.get_remaining_capacity() < match.guest.party_size:
        return error_response("Host doesn't have enough capacity")
    
    old_host_id = match.host_id
    match.host_id = new_host_id
    
    # Regenerate "why it's a fit"
    from app.services.matching_adapter import generate_why_fit
    match.why_its_a_fit = generate_why_fit(match.guest, new_host)
    
    db.session.commit()
    
    ActivityLog.log(
        ActivityType.MATCH_EDITED.value,
        actor='admin',
        target_type='match',
        target_id=match.id,
        details={'old_host_id': old_host_id, 'new_host_id': new_host_id}
    )
    db.session.commit()
    
    return success_response(
        message="Match updated",
        data=match.to_dict(include_guest_details=True, include_host_details=True)
    )


@admin_bp.route('/matches/<match_id>', methods=['DELETE'])
@admin_required
def delete_match(match_id):
    """Delete a proposed match."""
    match = Match.query.get(match_id)
    if not match:
        return error_response("Match not found", status_code=404)
    
    if match.status != MatchStatus.PROPOSED.value:
        return error_response("Can only delete proposed matches", status_code=400)
    
    ActivityLog.log(
        ActivityType.MATCH_REMOVED.value,
        actor='admin',
        target_type='match',
        target_id=match.id,
        details={'guest_id': match.guest_id, 'host_id': match.host_id}
    )
    
    db.session.delete(match)
    db.session.commit()
    
    return success_response(message="Match deleted")


@admin_bp.route('/matches/<match_id>/send', methods=['POST'])
@admin_required
def send_match_request(match_id):
    """Send match request to host."""
    match = Match.query.get(match_id)
    if not match:
        return error_response("Match not found", status_code=404)
    
    if match.status != MatchStatus.PROPOSED.value:
        return error_response("Match must be in proposed status", status_code=400)
    
    # Generate action tokens for accept/decline
    frontend_url = current_app.config['FRONTEND_URL']
    accept_token = generate_action_token('match_accept', match.id, expires_hours=168)  # 7 days
    decline_token = generate_action_token('match_decline', match.id, expires_hours=168)
    
    accept_link = f"{frontend_url}/match/respond?token={accept_token}&action=accept"
    decline_link = f"{frontend_url}/match/respond?token={decline_token}&action=decline"
    
    # Update status
    match.status = MatchStatus.REQUESTED.value
    match.requested_at = datetime.utcnow()
    db.session.commit()
    
    # Send email to host
    EmailService.send_match_request_to_host(match, accept_link, decline_link)
    
    ActivityLog.log(
        ActivityType.MATCH_REQUEST_SENT.value,
        actor='admin',
        target_type='match',
        target_id=match.id,
        details={'host_id': match.host_id, 'guest_id': match.guest_id}
    )
    db.session.commit()
    
    return success_response(
        message="Match request sent to host",
        data=match.to_dict()
    )


@admin_bp.route('/matches/<match_id>/finalize', methods=['POST'])
@admin_required
def finalize_match(match_id):
    """Finalize an accepted match and send confirmations to both parties."""
    match = Match.query.get(match_id)
    if not match:
        return error_response("Match not found", status_code=404)
    
    if match.status != MatchStatus.ACCEPTED.value:
        return error_response("Match must be in accepted status", status_code=400)
    
    # Update status
    match.status = MatchStatus.CONFIRMED.value
    match.finalized_at = datetime.utcnow()
    db.session.commit()
    
    # Send confirmation emails to BOTH parties (this is when guest learns about match)
    EmailService.send_match_confirmed_to_guest(match)
    EmailService.send_match_confirmed_to_host(match)
    
    ActivityLog.log(
        ActivityType.MATCH_FINALIZED.value,
        actor='admin',
        target_type='match',
        target_id=match.id,
        details={'host_id': match.host_id, 'guest_id': match.guest_id}
    )
    db.session.commit()
    
    return success_response(
        message="Match finalized and confirmations sent",
        data=match.to_dict(include_guest_details=True, include_host_details=True, reveal_contact=True)
    )


@admin_bp.route('/matches/<match_id>/send-reminder', methods=['POST'])
@admin_required
def send_day_of_reminder(match_id):
    """Send day-of reminder to guest with attendance confirmation link."""
    match = Match.query.get(match_id)
    if not match:
        return error_response("Match not found", status_code=404)
    
    if match.status != MatchStatus.CONFIRMED.value:
        return error_response("Match must be confirmed", status_code=400)
    
    # Generate attendance confirmation token
    frontend_url = current_app.config['FRONTEND_URL']
    confirm_token = generate_action_token('confirm_attendance', match.id, expires_hours=24)
    confirm_link = f"{frontend_url}/attendance/confirm?token={confirm_token}"
    
    # Send reminder email
    EmailService.send_day_of_reminder_to_guest(match, confirm_link)
    
    return success_response(message="Day-of reminder sent")


@admin_bp.route('/hosts/<host_id>/send-summary', methods=['POST'])
@admin_required
def send_host_summary(host_id):
    """Send day-of summary to host with guest list."""
    host = Host.query.get(host_id)
    if not host:
        return error_response("Host not found", status_code=404)
    
    # Get all confirmed matches for this host
    confirmed_matches = Match.query.filter(
        Match.host_id == host_id,
        Match.status == MatchStatus.CONFIRMED.value
    ).all()
    
    if not confirmed_matches:
        return error_response("No confirmed guests for this host")
    
    # Send summary email
    EmailService.send_day_of_summary_to_host(host, confirmed_matches)
    
    return success_response(message="Host summary sent")


@admin_bp.route('/hosts/<host_id>/send-noshow-request', methods=['POST'])
@admin_required
def send_noshow_report_request(host_id):
    """Send post-event email asking host to report no-shows."""
    host = Host.query.get(host_id)
    if not host:
        return error_response("Host not found", status_code=404)
    
    # Generate no-show report token
    frontend_url = current_app.config['FRONTEND_URL']
    report_token = generate_action_token('noshow_report', host.id, expires_hours=168)  # 7 days
    report_link = f"{frontend_url}/noshow/report?token={report_token}"
    
    # Send email
    EmailService.send_noshow_report_request(host, report_link)
    
    return success_response(message="No-show report request sent")


@admin_bp.route('/emails', methods=['GET'])
@admin_required
def list_emails():
    """List all emails (for debugging/viewing simulated sends)."""
    emails = Email.query.order_by(Email.created_at.desc()).limit(100).all()
    return success_response(data=[e.to_dict() for e in emails])


@admin_bp.route('/activity', methods=['GET'])
@admin_required
def list_activity():
    """List recent activity log entries."""
    logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(100).all()
    return success_response(data=[l.to_dict() for l in logs])
