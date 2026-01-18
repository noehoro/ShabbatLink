"""
Default matching engine implementation.

This is a greedy assignment algorithm that:
1. Scores all eligible guest-host pairs
2. Assigns guests to their highest-scoring eligible host
3. Updates capacity and continues until all guests are processed

CRITICAL INVARIANTS:
- No guest is ever assigned to multiple hosts
- No host capacity ever goes negative
- party_size is correctly subtracted from capacity
"""
from typing import List, Dict, Tuple
from app.matching.interface import MatchingEngineInterface
from app.matching.data_types import (
    GuestData, HostData, MatchingConfig, 
    ProposedMatch, MatchingResult
)
from app.matching.eligibility import is_eligible
from app.matching.scoring import calculate_total_score
from app.matching.explainer import generate_explanation


class DefaultMatchingEngine(MatchingEngineInterface):
    """
    Default greedy matching engine.
    
    Algorithm:
    1. For each guest, calculate scores for all eligible hosts
    2. Sort guests by "difficulty" (fewer eligible hosts = higher priority)
    3. Assign each guest to their best available host
    4. Track capacity to ensure no overbooking
    """
    
    def generate_matches(
        self,
        guests: List[GuestData],
        hosts: List[HostData],
        config: MatchingConfig
    ) -> MatchingResult:
        """Generate matches between guests and hosts."""
        
        # Track remaining capacity per host
        remaining_capacity: Dict[str, int] = {
            host.id: host.seats_available for host in hosts
        }
        
        # Track total initial capacity for scoring
        total_capacity = sum(h.seats_available for h in hosts)
        
        # Build host lookup
        host_lookup: Dict[str, HostData] = {h.id: h for h in hosts}
        
        # Track assigned guests to ensure no double-assignment
        assigned_guests: set = set()
        
        matches: List[ProposedMatch] = []
        unmatched: List[str] = []
        
        # Calculate scores and eligible hosts for each guest
        guest_options: List[Tuple[GuestData, List[Tuple[str, float]]]] = []
        
        for guest in guests:
            # Skip flagged guests with too many no-shows
            if guest.is_flagged and guest.no_show_count >= 2:
                unmatched.append(guest.id)
                continue
            
            # Find all eligible hosts and their scores
            eligible_hosts = []
            for host in hosts:
                capacity = remaining_capacity[host.id]
                if is_eligible(guest, host, capacity):
                    score = calculate_total_score(
                        guest, host, capacity, total_capacity, config
                    )
                    if score >= config.min_score_threshold:
                        eligible_hosts.append((host.id, score))
            
            # Sort by score descending
            eligible_hosts.sort(key=lambda x: x[1], reverse=True)
            guest_options.append((guest, eligible_hosts))
        
        # Sort guests by number of options (fewest first = hardest to place)
        guest_options.sort(key=lambda x: len(x[1]))
        
        # Assign guests
        for guest, options in guest_options:
            if guest.id in assigned_guests:
                # Should never happen, but safety check
                continue
            
            # Find first available host with sufficient capacity
            matched_host_id = None
            alternatives = []
            
            for host_id, score in options:
                current_capacity = remaining_capacity[host_id]
                
                # Check capacity again (may have changed since initial scoring)
                if current_capacity >= guest.party_size:
                    if matched_host_id is None:
                        matched_host_id = host_id
                    else:
                        # Track as alternative (up to max)
                        if len(alternatives) < config.max_alternatives_per_guest:
                            alternatives.append(host_id)
            
            if matched_host_id:
                host = host_lookup[matched_host_id]
                
                # Create match
                match = ProposedMatch(
                    guest_id=guest.id,
                    host_id=matched_host_id,
                    score=next(s for h, s in options if h == matched_host_id),
                    why_fit=generate_explanation(guest, host),
                    alternatives=alternatives
                )
                matches.append(match)
                
                # Update capacity (CRITICAL: subtract party_size, not 1)
                remaining_capacity[matched_host_id] -= guest.party_size
                
                # Mark guest as assigned
                assigned_guests.add(guest.id)
                
                # INVARIANT CHECK: capacity should never go negative
                assert remaining_capacity[matched_host_id] >= 0, \
                    f"Host {matched_host_id} capacity went negative!"
            else:
                unmatched.append(guest.id)
        
        # Verify invariants
        self._verify_invariants(matches, guests, hosts, remaining_capacity)
        
        return MatchingResult(
            matches=matches,
            unmatched_guests=unmatched,
            stats={
                'total_guests': len(guests),
                'matched_guests': len(matches),
                'unmatched_guests': len(unmatched),
                'hosts_used': len(set(m.host_id for m in matches)),
                'total_hosts': len(hosts)
            }
        )
    
    def _verify_invariants(
        self,
        matches: List[ProposedMatch],
        guests: List[GuestData],
        hosts: List[HostData],
        remaining_capacity: Dict[str, int]
    ) -> None:
        """Verify critical matching invariants."""
        # Check no guest is assigned twice
        assigned_guest_ids = [m.guest_id for m in matches]
        assert len(assigned_guest_ids) == len(set(assigned_guest_ids)), \
            "INVARIANT VIOLATION: A guest was assigned to multiple hosts!"
        
        # Check no host has negative capacity
        for host_id, capacity in remaining_capacity.items():
            assert capacity >= 0, \
                f"INVARIANT VIOLATION: Host {host_id} has negative capacity ({capacity})!"
        
        # Verify capacity math
        guest_lookup = {g.id: g for g in guests}
        for host in hosts:
            matches_for_host = [m for m in matches if m.host_id == host.id]
            seats_used = sum(guest_lookup[m.guest_id].party_size for m in matches_for_host)
            expected_remaining = host.seats_available - seats_used
            actual_remaining = remaining_capacity[host.id]
            assert expected_remaining == actual_remaining, \
                f"INVARIANT VIOLATION: Capacity mismatch for host {host.id}!"
