"""
Matching Adapter - Bridges ORM models and the matching engine.

This is the ONLY place where SQLAlchemy models and matching engine meet.
To swap matching algorithms, change which engine is instantiated here.
"""
from typing import List
from app import db
from app.models import Guest, Host, Match
from app.matching import (
    GuestData, HostData, MatchingConfig,
    DefaultMatchingEngine
)
from app.matching.explainer import generate_explanation
from app.config import MatchStatus


def guest_to_data(guest: Guest) -> GuestData:
    """Convert ORM Guest to plain GuestData."""
    return GuestData(
        id=guest.id,
        full_name=guest.full_name,
        party_size=guest.party_size,
        neighborhood=guest.neighborhood,
        max_travel_time=guest.max_travel_time,
        languages=guest.languages or [],
        kosher_requirement=guest.kosher_requirement,
        contribution_range=guest.contribution_range,
        vibe_chabad=guest.vibe_chabad,
        vibe_social=guest.vibe_social,
        vibe_formality=guest.vibe_formality,
        is_flagged=guest.is_flagged,
        no_show_count=guest.no_show_count
    )


def host_to_data(host: Host) -> HostData:
    """Convert ORM Host to plain HostData."""
    return HostData(
        id=host.id,
        full_name=host.full_name,
        seats_available=host.seats_available,
        neighborhood=host.neighborhood,
        languages=host.languages or [],
        kosher_level=host.kosher_level,
        contribution_preference=host.contribution_preference,
        vibe_chabad=host.vibe_chabad,
        vibe_social=host.vibe_social,
        vibe_formality=host.vibe_formality
    )


def run_matching() -> dict:
    """
    Run the matching algorithm and create Match records.
    
    This function:
    1. Loads all unmatched guests and available hosts
    2. Converts them to plain data structures
    3. Calls the matching engine
    4. Creates Match ORM records from the results
    
    Returns:
        dict with matching statistics
    """
    # Get guests who don't have an active match
    active_match_guest_ids = db.session.query(Match.guest_id).filter(
        Match.status.in_([
            MatchStatus.PROPOSED.value,
            MatchStatus.REQUESTED.value,
            MatchStatus.ACCEPTED.value,
            MatchStatus.CONFIRMED.value
        ])
    ).distinct()
    
    guests = Guest.query.filter(
        ~Guest.id.in_(active_match_guest_ids)
    ).all()
    
    # Get all hosts (we'll track capacity during matching)
    hosts = Host.query.all()
    
    if not guests or not hosts:
        return {
            'matches_created': 0,
            'unmatched_guests': [g.id for g in guests] if guests else [],
            'error': 'No guests or hosts available for matching'
        }
    
    # Convert to plain data structures
    guest_data_list = [guest_to_data(g) for g in guests]
    host_data_list = [host_to_data(h) for h in hosts]
    
    # Adjust host capacity for existing matches
    for host_data in host_data_list:
        existing_matches = Match.query.filter(
            Match.host_id == host_data.id,
            Match.status.in_([
                MatchStatus.REQUESTED.value,
                MatchStatus.ACCEPTED.value,
                MatchStatus.CONFIRMED.value
            ])
        ).all()
        
        # Get guest lookup for party size
        for match in existing_matches:
            guest = Guest.query.get(match.guest_id)
            if guest:
                host_data.seats_available -= guest.party_size
    
    # Filter out hosts with no remaining capacity
    host_data_list = [h for h in host_data_list if h.seats_available > 0]
    
    if not host_data_list:
        return {
            'matches_created': 0,
            'unmatched_guests': [g.id for g in guest_data_list],
            'error': 'No hosts with available capacity'
        }
    
    # Create matching engine and run
    # *** TO SWAP ALGORITHMS: Change this line ***
    engine = DefaultMatchingEngine()
    config = MatchingConfig()
    
    result = engine.generate_matches(guest_data_list, host_data_list, config)
    
    # Create Match records from results
    matches_created = 0
    for proposed in result.matches:
        match = Match(
            guest_id=proposed.guest_id,
            host_id=proposed.host_id,
            status=MatchStatus.PROPOSED.value,
            match_score=proposed.score,
            why_its_a_fit=proposed.why_fit
        )
        db.session.add(match)
        matches_created += 1
    
    db.session.commit()
    
    return {
        'matches_created': matches_created,
        'unmatched_guests': result.unmatched_guests,
        'stats': result.stats
    }


def generate_why_fit(guest: Guest, host: Host) -> str:
    """
    Generate "why it's a fit" explanation for a guest-host pair.
    
    Used when admin manually reassigns a match.
    """
    guest_data = guest_to_data(guest)
    host_data = host_to_data(host)
    return generate_explanation(guest_data, host_data)
