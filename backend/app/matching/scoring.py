"""
Scoring functions for ranking matches.

Each function returns a score between 0 and 1, where 1 is the best match.
"""
import math
from app.matching.data_types import GuestData, HostData, MatchingConfig
from app.matching.distance import get_travel_time


def calculate_distance_score(guest: GuestData, host: HostData) -> float:
    """
    Calculate distance score based on travel time.
    
    Score is higher when travel time is lower relative to guest's max preference.
    Returns 0-1, where 1 = same neighborhood, 0 = at max travel time.
    """
    travel_time = get_travel_time(guest.neighborhood, host.neighborhood)
    max_travel = guest.max_travel_time
    
    if travel_time >= max_travel:
        return 0.0
    
    # Linear decay from 1 (0 min) to 0 (max_travel min)
    return 1.0 - (travel_time / max_travel)


def calculate_vibe_score(guest: GuestData, host: HostData) -> float:
    """
    Calculate vibe similarity score using Euclidean distance on 3D vibe space.
    
    Each vibe slider is 1-5, so max distance = sqrt(4^2 + 4^2 + 4^2) = ~6.93
    Returns 0-1, where 1 = perfect match, 0 = maximum difference.
    """
    diff_chabad = guest.vibe_chabad - host.vibe_chabad
    diff_social = guest.vibe_social - host.vibe_social
    diff_formality = guest.vibe_formality - host.vibe_formality
    
    distance = math.sqrt(diff_chabad**2 + diff_social**2 + diff_formality**2)
    max_distance = math.sqrt(4**2 + 4**2 + 4**2)  # ~6.93
    
    return 1.0 - (distance / max_distance)


def calculate_contribution_score(guest: GuestData, host: HostData) -> float:
    """
    Calculate contribution alignment score.
    
    This is a soft preference - we try to match contribution expectations.
    Returns 0-1, where 1 = good alignment, 0 = poor alignment.
    """
    # Define contribution levels in order
    contribution_order = [
        "No contribution needed",
        "Prefer not to say",
        "$0 to $10",
        "$10 to $25",
        "$25 to $50",
        "$50+"
    ]
    
    def get_level(value):
        if value in contribution_order:
            return contribution_order.index(value)
        return 1  # Default to "Prefer not to say"
    
    guest_level = get_level(guest.contribution_range)
    host_level = get_level(host.contribution_preference)
    
    # "Prefer not to say" matches with anything (score 0.7)
    if guest_level == 1 or host_level == 1:
        return 0.7
    
    # "No contribution needed" from host is always good
    if host_level == 0:
        return 1.0
    
    # Calculate difference in levels
    diff = abs(guest_level - host_level)
    max_diff = len(contribution_order) - 1
    
    return 1.0 - (diff / max_diff)


def calculate_capacity_score(host: HostData, remaining_capacity: int, total_capacity: int) -> float:
    """
    Calculate capacity utilization score.
    
    Prefers distributing guests across hosts rather than overloading one host.
    Returns 0-1, where 1 = host has most available capacity.
    """
    if total_capacity == 0:
        return 0.5
    
    return remaining_capacity / total_capacity


def calculate_total_score(
    guest: GuestData,
    host: HostData,
    remaining_capacity: int,
    total_capacity: int,
    config: MatchingConfig
) -> float:
    """
    Calculate total weighted score for a guest-host pairing.
    
    Returns 0-1, where higher is better.
    """
    distance_score = calculate_distance_score(guest, host)
    vibe_score = calculate_vibe_score(guest, host)
    contribution_score = calculate_contribution_score(guest, host)
    capacity_score = calculate_capacity_score(host, remaining_capacity, total_capacity)
    
    total = (
        config.weight_distance * distance_score +
        config.weight_vibe * vibe_score +
        config.weight_contribution * contribution_score +
        config.weight_capacity * capacity_score
    )
    
    return total


def get_score_breakdown(
    guest: GuestData,
    host: HostData,
    remaining_capacity: int,
    total_capacity: int,
    config: MatchingConfig
) -> dict:
    """Get detailed breakdown of score components."""
    return {
        'distance': calculate_distance_score(guest, host),
        'vibe': calculate_vibe_score(guest, host),
        'contribution': calculate_contribution_score(guest, host),
        'capacity': calculate_capacity_score(host, remaining_capacity, total_capacity),
        'total': calculate_total_score(guest, host, remaining_capacity, total_capacity, config)
    }
