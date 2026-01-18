"""
Neighborhood distance matrix for Manhattan.

Travel times are rough estimates based on subway/walking distances.
"""

# Manhattan neighborhoods with approximate travel times in minutes
# This is a simplified heuristic - actual travel times vary

NEIGHBORHOODS = [
    "Upper West Side",
    "Upper East Side",
    "Midtown West",
    "Midtown East",
    "Murray Hill",
    "Gramercy / Flatiron",
    "Chelsea",
    "Greenwich Village / West Village",
    "East Village / NoHo",
    "SoHo / Tribeca",
    "Lower East Side",
    "Financial District",
    "Washington Heights",
    "Harlem"
]

# Distance matrix: approximate travel time in minutes between neighborhoods
# Index corresponds to NEIGHBORHOODS list order
DISTANCE_MATRIX = {
    "Upper West Side": {
        "Upper West Side": 5,
        "Upper East Side": 20,
        "Midtown West": 15,
        "Midtown East": 20,
        "Murray Hill": 25,
        "Gramercy / Flatiron": 25,
        "Chelsea": 20,
        "Greenwich Village / West Village": 25,
        "East Village / NoHo": 30,
        "SoHo / Tribeca": 30,
        "Lower East Side": 35,
        "Financial District": 35,
        "Washington Heights": 20,
        "Harlem": 15
    },
    "Upper East Side": {
        "Upper West Side": 20,
        "Upper East Side": 5,
        "Midtown West": 20,
        "Midtown East": 10,
        "Murray Hill": 15,
        "Gramercy / Flatiron": 20,
        "Chelsea": 25,
        "Greenwich Village / West Village": 25,
        "East Village / NoHo": 20,
        "SoHo / Tribeca": 30,
        "Lower East Side": 25,
        "Financial District": 35,
        "Washington Heights": 35,
        "Harlem": 20
    },
    "Midtown West": {
        "Upper West Side": 15,
        "Upper East Side": 20,
        "Midtown West": 5,
        "Midtown East": 15,
        "Murray Hill": 15,
        "Gramercy / Flatiron": 15,
        "Chelsea": 10,
        "Greenwich Village / West Village": 15,
        "East Village / NoHo": 20,
        "SoHo / Tribeca": 20,
        "Lower East Side": 25,
        "Financial District": 25,
        "Washington Heights": 30,
        "Harlem": 25
    },
    "Midtown East": {
        "Upper West Side": 20,
        "Upper East Side": 10,
        "Midtown West": 15,
        "Midtown East": 5,
        "Murray Hill": 10,
        "Gramercy / Flatiron": 15,
        "Chelsea": 20,
        "Greenwich Village / West Village": 20,
        "East Village / NoHo": 15,
        "SoHo / Tribeca": 25,
        "Lower East Side": 20,
        "Financial District": 30,
        "Washington Heights": 35,
        "Harlem": 25
    },
    "Murray Hill": {
        "Upper West Side": 25,
        "Upper East Side": 15,
        "Midtown West": 15,
        "Midtown East": 10,
        "Murray Hill": 5,
        "Gramercy / Flatiron": 10,
        "Chelsea": 15,
        "Greenwich Village / West Village": 15,
        "East Village / NoHo": 15,
        "SoHo / Tribeca": 20,
        "Lower East Side": 15,
        "Financial District": 25,
        "Washington Heights": 40,
        "Harlem": 30
    },
    "Gramercy / Flatiron": {
        "Upper West Side": 25,
        "Upper East Side": 20,
        "Midtown West": 15,
        "Midtown East": 15,
        "Murray Hill": 10,
        "Gramercy / Flatiron": 5,
        "Chelsea": 10,
        "Greenwich Village / West Village": 10,
        "East Village / NoHo": 10,
        "SoHo / Tribeca": 15,
        "Lower East Side": 15,
        "Financial District": 25,
        "Washington Heights": 40,
        "Harlem": 35
    },
    "Chelsea": {
        "Upper West Side": 20,
        "Upper East Side": 25,
        "Midtown West": 10,
        "Midtown East": 20,
        "Murray Hill": 15,
        "Gramercy / Flatiron": 10,
        "Chelsea": 5,
        "Greenwich Village / West Village": 10,
        "East Village / NoHo": 15,
        "SoHo / Tribeca": 15,
        "Lower East Side": 20,
        "Financial District": 25,
        "Washington Heights": 35,
        "Harlem": 30
    },
    "Greenwich Village / West Village": {
        "Upper West Side": 25,
        "Upper East Side": 25,
        "Midtown West": 15,
        "Midtown East": 20,
        "Murray Hill": 15,
        "Gramercy / Flatiron": 10,
        "Chelsea": 10,
        "Greenwich Village / West Village": 5,
        "East Village / NoHo": 10,
        "SoHo / Tribeca": 10,
        "Lower East Side": 15,
        "Financial District": 20,
        "Washington Heights": 40,
        "Harlem": 35
    },
    "East Village / NoHo": {
        "Upper West Side": 30,
        "Upper East Side": 20,
        "Midtown West": 20,
        "Midtown East": 15,
        "Murray Hill": 15,
        "Gramercy / Flatiron": 10,
        "Chelsea": 15,
        "Greenwich Village / West Village": 10,
        "East Village / NoHo": 5,
        "SoHo / Tribeca": 10,
        "Lower East Side": 10,
        "Financial District": 20,
        "Washington Heights": 45,
        "Harlem": 35
    },
    "SoHo / Tribeca": {
        "Upper West Side": 30,
        "Upper East Side": 30,
        "Midtown West": 20,
        "Midtown East": 25,
        "Murray Hill": 20,
        "Gramercy / Flatiron": 15,
        "Chelsea": 15,
        "Greenwich Village / West Village": 10,
        "East Village / NoHo": 10,
        "SoHo / Tribeca": 5,
        "Lower East Side": 15,
        "Financial District": 15,
        "Washington Heights": 45,
        "Harlem": 40
    },
    "Lower East Side": {
        "Upper West Side": 35,
        "Upper East Side": 25,
        "Midtown West": 25,
        "Midtown East": 20,
        "Murray Hill": 15,
        "Gramercy / Flatiron": 15,
        "Chelsea": 20,
        "Greenwich Village / West Village": 15,
        "East Village / NoHo": 10,
        "SoHo / Tribeca": 15,
        "Lower East Side": 5,
        "Financial District": 15,
        "Washington Heights": 50,
        "Harlem": 40
    },
    "Financial District": {
        "Upper West Side": 35,
        "Upper East Side": 35,
        "Midtown West": 25,
        "Midtown East": 30,
        "Murray Hill": 25,
        "Gramercy / Flatiron": 25,
        "Chelsea": 25,
        "Greenwich Village / West Village": 20,
        "East Village / NoHo": 20,
        "SoHo / Tribeca": 15,
        "Lower East Side": 15,
        "Financial District": 5,
        "Washington Heights": 50,
        "Harlem": 45
    },
    "Washington Heights": {
        "Upper West Side": 20,
        "Upper East Side": 35,
        "Midtown West": 30,
        "Midtown East": 35,
        "Murray Hill": 40,
        "Gramercy / Flatiron": 40,
        "Chelsea": 35,
        "Greenwich Village / West Village": 40,
        "East Village / NoHo": 45,
        "SoHo / Tribeca": 45,
        "Lower East Side": 50,
        "Financial District": 50,
        "Washington Heights": 5,
        "Harlem": 15
    },
    "Harlem": {
        "Upper West Side": 15,
        "Upper East Side": 20,
        "Midtown West": 25,
        "Midtown East": 25,
        "Murray Hill": 30,
        "Gramercy / Flatiron": 35,
        "Chelsea": 30,
        "Greenwich Village / West Village": 35,
        "East Village / NoHo": 35,
        "SoHo / Tribeca": 40,
        "Lower East Side": 40,
        "Financial District": 45,
        "Washington Heights": 15,
        "Harlem": 5
    }
}


def get_travel_time(neighborhood_a: str, neighborhood_b: str) -> int:
    """
    Get estimated travel time between two neighborhoods.
    
    Returns travel time in minutes, or 60 if neighborhood not found.
    """
    if neighborhood_a not in DISTANCE_MATRIX:
        return 60  # Unknown neighborhood, assume far
    
    distances = DISTANCE_MATRIX[neighborhood_a]
    return distances.get(neighborhood_b, 60)


def is_within_travel_preference(guest_neighborhood: str, host_neighborhood: str, max_travel_time: int) -> bool:
    """
    Check if travel between neighborhoods is within guest's preference.
    """
    travel_time = get_travel_time(guest_neighborhood, host_neighborhood)
    return travel_time <= max_travel_time
