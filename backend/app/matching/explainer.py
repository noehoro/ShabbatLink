"""
"Why It's a Fit" explanation generator.

Generates friendly, 1-2 sentence explanations for matches based on structured fields.
"""
from app.matching.data_types import GuestData, HostData
from app.matching.distance import get_travel_time
from app.matching.scoring import calculate_vibe_score


def generate_explanation(guest: GuestData, host: HostData) -> str:
    """
    Generate a friendly explanation for why this match is a good fit.
    
    Uses only factual references to:
    - Shared language(s)
    - Kosher compatibility
    - Vibe similarity
    - Neighborhood proximity
    
    Returns 1-2 sentences.
    """
    points = []
    
    # Check shared languages
    shared_languages = set(guest.languages) & set(host.languages)
    if len(shared_languages) > 1:
        langs = list(shared_languages)
        points.append(f"You both speak {' and '.join(langs)}")
    elif len(shared_languages) == 1:
        lang = list(shared_languages)[0]
        if lang != "English":
            points.append(f"You both speak {lang}")
    
    # Check neighborhood proximity
    travel_time = get_travel_time(guest.neighborhood, host.neighborhood)
    if travel_time <= 15:
        if guest.neighborhood == host.neighborhood:
            points.append("you're in the same neighborhood")
        else:
            points.append("you're just a short trip apart")
    elif travel_time <= 25:
        points.append("you're conveniently located nearby")
    
    # Check vibe match
    vibe_score = calculate_vibe_score(guest, host)
    if vibe_score >= 0.85:
        points.append("you have very similar Shabbat vibes")
    elif vibe_score >= 0.7:
        points.append("your Shabbat styles align well")
    
    # Check specific vibe dimensions
    vibe_details = []
    
    # Check social intensity match
    if abs(guest.vibe_social - host.vibe_social) <= 1:
        if guest.vibe_social <= 2:
            vibe_details.append("you both prefer intimate gatherings")
        elif guest.vibe_social >= 4:
            vibe_details.append("you both enjoy larger groups")
    
    # Check formality match
    if abs(guest.vibe_formality - host.vibe_formality) <= 1:
        if guest.vibe_formality <= 2:
            vibe_details.append("you both enjoy a casual atmosphere")
        elif guest.vibe_formality >= 4:
            vibe_details.append("you both appreciate a traditional setting")
    
    # Add one vibe detail if we don't have enough points
    if len(points) < 2 and vibe_details:
        points.append(vibe_details[0])
    
    # Build the explanation
    if not points:
        return "Based on your preferences, this looks like a great match!"
    
    if len(points) == 1:
        return f"{points[0].capitalize()} - we think you'll have a wonderful time!"
    
    # Combine points into a sentence
    first = points[0]
    if not first[0].isupper():
        first = first.capitalize()
    
    rest = points[1:]
    combined = f"{first}, and {rest[0]}."
    
    return combined


def generate_explanation_for_host(guest: GuestData, host: HostData) -> str:
    """
    Generate explanation from host's perspective (used in match request email).
    """
    base_explanation = generate_explanation(guest, host)
    
    # Add party size info if relevant
    if guest.party_size > 1:
        return f"{guest.full_name} is bringing a party of {guest.party_size}. {base_explanation}"
    
    return base_explanation
