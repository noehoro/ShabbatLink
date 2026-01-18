"""
Abstract interface for matching engines.

Any matching algorithm implementation must implement this interface.
This enables swapping algorithms without changing any other code.
"""
from abc import ABC, abstractmethod
from typing import List
from app.matching.data_types import GuestData, HostData, MatchingConfig, MatchingResult


class MatchingEngineInterface(ABC):
    """
    Abstract interface for matching engines.
    
    To create a new matching algorithm:
    1. Create a class that inherits from this interface
    2. Implement the generate_matches method
    3. Update matching_adapter.py to use your new engine
    """
    
    @abstractmethod
    def generate_matches(
        self,
        guests: List[GuestData],
        hosts: List[HostData],
        config: MatchingConfig
    ) -> MatchingResult:
        """
        Generate matches between guests and hosts.
        
        Args:
            guests: List of guest data objects
            hosts: List of host data objects
            config: Matching configuration with weights and options
        
        Returns:
            MatchingResult with proposed matches and unmatched guests
        
        Guarantees:
            - No guest is assigned to multiple hosts
            - No host capacity goes negative
            - All guests are either matched or in unmatched list
        """
        pass
