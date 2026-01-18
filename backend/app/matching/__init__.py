"""
Matching Engine Module - Isolated and Plug-and-Play

This module is intentionally isolated from Flask and SQLAlchemy.
It uses only plain Python dataclasses for input/output.

To swap algorithms:
1. Implement the MatchingEngineInterface
2. Change one line in matching_adapter.py to use the new engine
"""
from app.matching.interface import MatchingEngineInterface
from app.matching.data_types import GuestData, HostData, MatchingConfig, ProposedMatch, MatchingResult
from app.matching.engine import DefaultMatchingEngine

__all__ = [
    'MatchingEngineInterface',
    'GuestData',
    'HostData',
    'MatchingConfig',
    'ProposedMatch',
    'MatchingResult',
    'DefaultMatchingEngine'
]
