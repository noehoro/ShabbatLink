"""
Seed script to populate database with realistic mock data.
Run from backend directory: python seed_data.py
"""
import requests
import random

API_URL = "http://localhost:5001/api"

# Realistic data pools
FIRST_NAMES_MALE = ["David", "Michael", "Daniel", "Jonathan", "Benjamin", "Aaron", "Joshua", "Samuel", "Nathan", "Adam", "Eli", "Jacob", "Isaac", "Gabriel", "Noah", "Ethan", "Lucas", "Mateo", "Sebastian", "Diego"]
FIRST_NAMES_FEMALE = ["Sarah", "Rebecca", "Rachel", "Miriam", "Hannah", "Leah", "Esther", "Naomi", "Ruth", "Maya", "Sofia", "Isabella", "Valentina", "Camila", "Lucia", "Elena", "Ana", "Maria", "Gabriela", "Carolina"]
LAST_NAMES = ["Cohen", "Levy", "Goldstein", "Friedman", "Rosenberg", "Shapiro", "Katz", "Weiss", "Klein", "Schwartz", "Rubin", "Stern", "Rosen", "Kaplan", "Berger", "Hoffman", "Meyer", "Wolf", "Stein", "Green", "Rodriguez", "Garcia", "Martinez", "Lopez", "Gonzalez", "Fernandez", "Alvarez", "Morales", "Vargas", "Castro"]

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

LANGUAGES = ["English", "Spanish", "Portuguese"]

GUEST_KOSHER_OPTIONS = [
    "Kosher House",
    "Kosher Take out",
    "Not a Kosher home (Staff member will reach out to you)"
]

HOST_KOSHER_OPTIONS = [
    "Full kosher",
    "Mixed dairy and meat dishes",
    "Vegetarian kosher home"
]

CONTRIBUTION_AMOUNTS = ["$15", "$20", "$25", "$30", "$35", "$40", "$50"]

HOST_CONTRIBUTION_PREFERENCES = [
    "No contribution needed",
    "$10 to $25",
    "$25 to $50",
    "$50+"
]

def random_phone():
    return f"555-{random.randint(100,999)}-{random.randint(1000,9999)}"

def random_email(name):
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
    clean_name = name.lower().replace(" ", ".").replace("'", "")
    return f"{clean_name}{random.randint(1,99)}@{random.choice(domains)}"

def random_facebook(name):
    clean_name = name.lower().replace(" ", "").replace("'", "")
    return f"https://facebook.com/{clean_name}{random.randint(10,999)}"

def random_instagram(name):
    clean_name = name.lower().replace(" ", "_").replace("'", "")
    return f"@{clean_name}{random.randint(10,99)}"

def create_hosts():
    """Create 5 diverse hosts."""
    hosts = [
        {
            "full_name": "Rabbi David Goldstein",
            "email": "rabbi.goldstein@example.com",
            "phone": "555-100-1001",
            "neighborhood": "Upper West Side",
            "address": "245 West 86th Street, Apt 12B",
            "seats_available": 8,
            "languages": ["English", "Spanish"],
            "kosher_level": "Full kosher",
            "contribution_preference": "$25 to $50",
            "vibe_chabad": 4,
            "vibe_social": 4,
            "vibe_formality": 4,
            "host_notes": "Traditional Shabbat dinner with zemiros and divrei Torah. All are welcome!",
            "dinner_time": "7:00 PM",
            "no_show_acknowledged": True
        },
        {
            "full_name": "Sofia & Miguel Rodriguez",
            "email": "sofia.miguel@example.com",
            "phone": "555-200-2002",
            "neighborhood": "Washington Heights",
            "address": "180 Fort Washington Ave, Apt 5C",
            "seats_available": 6,
            "languages": ["English", "Spanish", "Portuguese"],
            "kosher_level": "Vegetarian kosher home",
            "contribution_preference": "No contribution needed",
            "vibe_chabad": 2,
            "vibe_social": 5,
            "vibe_formality": 2,
            "host_notes": "Casual Latino-Jewish fusion dinner! Great music and food. Vegetarian menu.",
            "dinner_time": "7:30 PM",
            "no_show_acknowledged": True
        },
        {
            "full_name": "Hannah & Jonathan Levy",
            "email": "hannah.levy@example.com",
            "phone": "555-300-3003",
            "neighborhood": "Upper East Side",
            "address": "340 East 72nd Street, Apt 8A",
            "seats_available": 4,
            "languages": ["English"],
            "kosher_level": "Full kosher",
            "contribution_preference": "$25 to $50",
            "vibe_chabad": 3,
            "vibe_social": 3,
            "vibe_formality": 4,
            "host_notes": "Intimate dinner with meaningful conversation. We love meeting new people!",
            "dinner_time": "6:45 PM",
            "no_show_acknowledged": True
        },
        {
            "full_name": "The Fernandez Family",
            "email": "fernandez.family@example.com",
            "phone": "555-400-4004",
            "neighborhood": "Murray Hill",
            "address": "225 East 34th Street, Apt 15D",
            "seats_available": 10,
            "languages": ["English", "Spanish"],
            "kosher_level": "Mixed dairy and meat dishes",
            "contribution_preference": "$10 to $25",
            "vibe_chabad": 3,
            "vibe_social": 5,
            "vibe_formality": 2,
            "host_notes": "Big family dinner! Kids welcome. Lots of food and fun.",
            "dinner_time": "7:00 PM",
            "no_show_acknowledged": True
        },
        {
            "full_name": "Elena Schwartz",
            "email": "elena.schwartz@example.com",
            "phone": "555-500-5005",
            "neighborhood": "Greenwich Village / West Village",
            "address": "78 Christopher Street, Apt 3B",
            "seats_available": 5,
            "languages": ["English", "Spanish"],
            "kosher_level": "Vegetarian kosher home",
            "contribution_preference": "$10 to $25",
            "vibe_chabad": 1,
            "vibe_social": 4,
            "vibe_formality": 1,
            "host_notes": "Chill Friday night. Good wine, good food, good vibes. Very laid back.",
            "dinner_time": "8:00 PM",
            "no_show_acknowledged": True
        }
    ]
    
    created = []
    for host in hosts:
        try:
            resp = requests.post(f"{API_URL}/hosts", json=host)
            if resp.status_code == 201:
                print(f"✓ Created host: {host['full_name']}")
                created.append(resp.json())
            else:
                print(f"✗ Failed to create host {host['full_name']}: {resp.text}")
        except Exception as e:
            print(f"✗ Error creating host {host['full_name']}: {e}")
    
    return created

def create_guests():
    """Create 30 diverse guests."""
    guests = []
    
    # Generate 30 guests with varied profiles
    guest_profiles = [
        # Young professionals - solo
        {"gender": "Male", "party_size": 1, "vibe": (2, 4, 2), "kosher": "Kosher Take out", "contribution": "$25", "travel": 30, "langs": ["English", "Spanish"]},
        {"gender": "Female", "party_size": 1, "vibe": (1, 5, 1), "kosher": "Not a Kosher home (Staff member will reach out to you)", "contribution": "$30", "travel": 45, "langs": ["English"]},
        {"gender": "Male", "party_size": 1, "vibe": (3, 3, 3), "kosher": "Kosher House", "contribution": "$35", "travel": 30, "langs": ["English", "Spanish"]},
        {"gender": "Female", "party_size": 1, "vibe": (4, 4, 4), "kosher": "Kosher House", "contribution": "$25", "travel": 60, "langs": ["English"]},
        {"gender": "Male", "party_size": 1, "vibe": (2, 5, 2), "kosher": "Kosher Take out", "contribution": "$20", "travel": 30, "langs": ["English", "Spanish", "Portuguese"]},
        
        # Couples
        {"gender": "Female", "party_size": 2, "vibe": (3, 4, 3), "kosher": "Kosher Take out", "contribution": "$30", "travel": 45, "langs": ["English", "Spanish"]},
        {"gender": "Male", "party_size": 2, "vibe": (4, 3, 4), "kosher": "Kosher House", "contribution": "$40", "travel": 30, "langs": ["English"]},
        {"gender": "Female", "party_size": 2, "vibe": (2, 5, 2), "kosher": "Not a Kosher home (Staff member will reach out to you)", "contribution": "$25", "travel": 60, "langs": ["English", "Spanish"]},
        {"gender": "Male", "party_size": 2, "vibe": (1, 4, 1), "kosher": "Kosher Take out", "contribution": "$35", "travel": 45, "langs": ["English", "Portuguese"]},
        {"gender": "Female", "party_size": 2, "vibe": (5, 5, 4), "kosher": "Kosher House", "contribution": "$30", "travel": 30, "langs": ["English", "Spanish"]},
        
        # More solo guests
        {"gender": "Male", "party_size": 1, "vibe": (3, 2, 3), "kosher": "Kosher House", "contribution": "$25", "travel": 15, "langs": ["English"]},
        {"gender": "Female", "party_size": 1, "vibe": (4, 4, 5), "kosher": "Kosher House", "contribution": "$40", "travel": 30, "langs": ["English", "Spanish"]},
        {"gender": "Male", "party_size": 1, "vibe": (1, 3, 1), "kosher": "Not a Kosher home (Staff member will reach out to you)", "contribution": "$15", "travel": 999, "langs": ["English", "Spanish", "Portuguese"]},
        {"gender": "Female", "party_size": 1, "vibe": (2, 4, 2), "kosher": "Kosher Take out", "contribution": "$30", "travel": 45, "langs": ["English"]},
        {"gender": "Male", "party_size": 1, "vibe": (5, 5, 5), "kosher": "Kosher House", "contribution": "$50", "travel": 60, "langs": ["English"]},
        
        # More varied profiles
        {"gender": "Female", "party_size": 1, "vibe": (3, 3, 2), "kosher": "Kosher Take out", "contribution": "$25", "travel": 30, "langs": ["Spanish"]},
        {"gender": "Male", "party_size": 2, "vibe": (2, 4, 3), "kosher": "Not a Kosher home (Staff member will reach out to you)", "contribution": "$35", "travel": 45, "langs": ["English", "Spanish"]},
        {"gender": "Female", "party_size": 1, "vibe": (4, 2, 4), "kosher": "Kosher House", "contribution": "$30", "travel": 30, "langs": ["English"]},
        {"gender": "Male", "party_size": 1, "vibe": (1, 5, 1), "kosher": "Kosher Take out", "contribution": "$20", "travel": 999, "langs": ["English", "Portuguese"]},
        {"gender": "Female", "party_size": 2, "vibe": (3, 4, 3), "kosher": "Kosher House", "contribution": "$40", "travel": 60, "langs": ["English", "Spanish"]},
        
        # Final batch
        {"gender": "Male", "party_size": 1, "vibe": (2, 3, 2), "kosher": "Not a Kosher home (Staff member will reach out to you)", "contribution": "$25", "travel": 30, "langs": ["English"]},
        {"gender": "Female", "party_size": 1, "vibe": (4, 5, 3), "kosher": "Kosher Take out", "contribution": "$30", "travel": 45, "langs": ["English", "Spanish"]},
        {"gender": "Male", "party_size": 2, "vibe": (3, 3, 4), "kosher": "Kosher House", "contribution": "$35", "travel": 30, "langs": ["English"]},
        {"gender": "Female", "party_size": 1, "vibe": (1, 4, 1), "kosher": "Kosher Take out", "contribution": "$25", "travel": 60, "langs": ["English", "Spanish", "Portuguese"]},
        {"gender": "Male", "party_size": 1, "vibe": (5, 4, 5), "kosher": "Kosher House", "contribution": "$50", "travel": 15, "langs": ["English"]},
        {"gender": "Female", "party_size": 2, "vibe": (2, 5, 2), "kosher": "Not a Kosher home (Staff member will reach out to you)", "contribution": "$30", "travel": 45, "langs": ["Spanish"]},
        {"gender": "Male", "party_size": 1, "vibe": (3, 2, 3), "kosher": "Kosher Take out", "contribution": "$25", "travel": 30, "langs": ["English", "Spanish"]},
        {"gender": "Female", "party_size": 1, "vibe": (4, 4, 4), "kosher": "Kosher House", "contribution": "$40", "travel": 999, "langs": ["English"]},
        {"gender": "Male", "party_size": 1, "vibe": (2, 3, 2), "kosher": "Kosher Take out", "contribution": "$20", "travel": 45, "langs": ["English", "Portuguese"]},
        {"gender": "Female", "party_size": 1, "vibe": (1, 5, 1), "kosher": "Not a Kosher home (Staff member will reach out to you)", "contribution": "$30", "travel": 60, "langs": ["English", "Spanish"]},
    ]
    
    used_names = set()
    
    for i, profile in enumerate(guest_profiles):
        # Generate unique name
        while True:
            if profile["gender"] == "Male":
                first = random.choice(FIRST_NAMES_MALE)
            else:
                first = random.choice(FIRST_NAMES_FEMALE)
            last = random.choice(LAST_NAMES)
            full_name = f"{first} {last}"
            if full_name not in used_names:
                used_names.add(full_name)
                break
        
        neighborhood = random.choice(NEIGHBORHOODS)
        
        guest = {
            "full_name": full_name,
            "email": random_email(full_name),
            "phone": random_phone(),
            "gender": profile["gender"],
            "party_size": profile["party_size"],
            "neighborhood": neighborhood,
            "max_travel_time": profile["travel"],
            "languages": profile["langs"],
            "kosher_requirement": profile["kosher"],
            "contribution_range": profile["contribution"],
            "vibe_chabad": profile["vibe"][0],
            "vibe_social": profile["vibe"][1],
            "vibe_formality": profile["vibe"][2],
            "attended_jlc_before": random.choice([True, False]),
            "facebook_url": random_facebook(full_name) if random.random() > 0.3 else None,
            "instagram_handle": random_instagram(full_name) if random.random() > 0.5 else None,
            "notes_to_admin": random.choice([
                None, 
                None,
                None,
                "First time at a Shabbat dinner!",
                "Looking forward to meeting new people",
                "Vegetarian preference if possible",
                "Can bring wine!",
                "Coming with a friend who might be late"
            ]),
            "no_show_acknowledged": True
        }
        guests.append(guest)
    
    created = []
    for guest in guests:
        try:
            resp = requests.post(f"{API_URL}/guests", json=guest)
            if resp.status_code == 201:
                print(f"✓ Created guest: {guest['full_name']} ({guest['gender']}, party of {guest['party_size']}, {guest['neighborhood']})")
                created.append(resp.json())
            else:
                print(f"✗ Failed to create guest {guest['full_name']}: {resp.text}")
        except Exception as e:
            print(f"✗ Error creating guest {guest['full_name']}: {e}")
    
    return created


def main():
    print("=" * 60)
    print("ShabbatLink Seed Data Script")
    print("=" * 60)
    print()
    
    print("Creating 5 hosts...")
    print("-" * 40)
    hosts = create_hosts()
    print()
    
    print("Creating 30 guests...")
    print("-" * 40)
    guests = create_guests()
    print()
    
    print("=" * 60)
    print(f"Summary: Created {len(hosts)} hosts and {len(guests)} guests")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Go to http://localhost:3000/admin")
    print("2. Login with password: shabbatlink2024")
    print("3. Click 'Generate Matches' to run the matching algorithm")
    print("4. Review and send match proposals!")


if __name__ == "__main__":
    main()
