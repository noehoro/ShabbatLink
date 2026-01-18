"""
Plain Python data structures for the matching engine.

These are COMPLETELY DECOUPLED from SQLAlchemy/Flask.
The adapter layer converts between ORM models and these dataclasses.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class GuestData:
    """Guest data for matching - plain Python, no ORM."""
    id: str
    full_name: str
    party_size: int
    neighborhood: str
    max_travel_time: int  # 15, 30, 45, 60
    languages: List[str]
    kosher_requirement: str
    contribution_range: str
    vibe_chabad: int
    vibe_social: int
    vibe_formality: int
    is_flagged: bool = False
    no_show_count: int = 0


@dataclass
class HostData:
    """Host data for matching - plain Python, no ORM."""
    id: str
    full_name: str
    seats_available: int
    neighborhood: str
    languages: List[str]
    kosher_level: str
    contribution_preference: str
    vibe_chabad: int
    vibe_social: int
    vibe_formality: int


@dataclass
class MatchingConfig:
    """Configuration for the matching algorithm."""
    # Scoring weights (must sum to 1.0)
    weight_distance: float = 0.25
    weight_vibe: float = 0.35
    weight_contribution: float = 0.15
    weight_capacity: float = 0.25
    
    # Thresholds
    min_score_threshold: float = 0.3  # Minimum score to consider a match
    
    # Options
    max_alternatives_per_guest: int = 3


@dataclass
class ProposedMatch:
    """A single proposed match."""
    guest_id: str
    host_id: str
    score: float
    why_fit: str
    alternatives: List[str] = field(default_factory=list)  # List of alternative host IDs


@dataclass
class MatchingResult:
    """Result of the matching algorithm."""
    matches: List[ProposedMatch]
    unmatched_guests: List[str]  # List of guest IDs that couldn't be matched
    stats: dict = field(default_factory=dict)
