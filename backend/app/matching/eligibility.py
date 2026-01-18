"""
Eligibility checking for guest-host matching.

A host is eligible for a guest if ALL of:
1. Host has enough seats for the guest party
2. Kosher compatibility is satisfied
3. At least one language overlaps
4. Travel preference is within reason
"""
from typing import List
from app.matching.data_types import GuestData, HostData
from app.matching.distance import is_within_travel_preference


# Kosher compatibility matrix
# Key: Guest requirement, Value: List of compatible host levels
KOSHER_COMPATIBILITY = {
    # New guest requirement values
    "Kosher House": ["Full kosher"],
    "Kosher Take out": ["Full kosher", "Mixed dairy and meat dishes", "Vegetarian kosher home"],
    "Not a Kosher home (Staff member will reach out to you)": ["Full kosher", "Mixed dairy and meat dishes", "Vegetarian kosher home"],
    # Legacy values (for backwards compatibility)
    "Full kosher only": ["Full kosher"],
    "Mixed dairy and meat dishes ok": ["Full kosher", "Mixed dairy and meat dishes"],
    "Vegetarian kosher home ok": ["Full kosher", "Mixed dairy and meat dishes", "Vegetarian kosher home"]
}


def check_capacity(guest: GuestData, host: HostData, remaining_capacity: int) -> bool:
    """Check if host has enough remaining capacity for guest party."""
    return remaining_capacity >= guest.party_size


def check_kosher_compatibility(guest: GuestData, host: HostData) -> bool:
    """Check if guest's kosher requirement is compatible with host's kitchen."""
    compatible_levels = KOSHER_COMPATIBILITY.get(guest.kosher_requirement, [])
    return host.kosher_level in compatible_levels


def check_language_overlap(guest: GuestData, host: HostData) -> bool:
    """Check if there's at least one shared language."""
    guest_languages = set(guest.languages)
    host_languages = set(host.languages)
    return len(guest_languages & host_languages) > 0


def check_travel_preference(guest: GuestData, host: HostData) -> bool:
    """Check if travel distance is within guest's preference."""
    return is_within_travel_preference(
        guest.neighborhood,
        host.neighborhood,
        guest.max_travel_time
    )


def is_eligible(guest: GuestData, host: HostData, remaining_capacity: int) -> bool:
    """
    Check if a host is eligible for a guest.
    
    ALL conditions must be met:
    - Capacity available
    - Kosher compatible
    - Language overlap
    - Travel within preference
    """
    return (
        check_capacity(guest, host, remaining_capacity) and
        check_kosher_compatibility(guest, host) and
        check_language_overlap(guest, host) and
        check_travel_preference(guest, host)
    )


def get_ineligibility_reasons(guest: GuestData, host: HostData, remaining_capacity: int) -> List[str]:
    """Get list of reasons why a host is not eligible for a guest."""
    reasons = []
    
    if not check_capacity(guest, host, remaining_capacity):
        reasons.append(f"Insufficient capacity (needs {guest.party_size}, has {remaining_capacity})")
    
    if not check_kosher_compatibility(guest, host):
        reasons.append(f"Kosher incompatible ({guest.kosher_requirement} vs {host.kosher_level})")
    
    if not check_language_overlap(guest, host):
        reasons.append(f"No shared language ({guest.languages} vs {host.languages})")
    
    if not check_travel_preference(guest, host):
        reasons.append(f"Travel too far ({guest.neighborhood} to {host.neighborhood})")
    
    return reasons
