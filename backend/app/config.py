"""Configuration constants and enums."""
from enum import Enum


class Neighborhood(str, Enum):
    """Manhattan neighborhoods."""
    UPPER_WEST_SIDE = "Upper West Side"
    UPPER_EAST_SIDE = "Upper East Side"
    MIDTOWN_WEST = "Midtown West"
    MIDTOWN_EAST = "Midtown East"
    MURRAY_HILL = "Murray Hill"
    GRAMERCY_FLATIRON = "Gramercy / Flatiron"
    CHELSEA = "Chelsea"
    GREENWICH_VILLAGE = "Greenwich Village / West Village"
    EAST_VILLAGE = "East Village / NoHo"
    SOHO_TRIBECA = "SoHo / Tribeca"
    LOWER_EAST_SIDE = "Lower East Side"
    FINANCIAL_DISTRICT = "Financial District"
    WASHINGTON_HEIGHTS = "Washington Heights"
    HARLEM = "Harlem"


class TravelTime(int, Enum):
    """Max travel time preferences in minutes."""
    FIFTEEN = 15
    THIRTY = 30
    FORTY_FIVE = 45
    SIXTY = 60
    NO_LIMIT = 999  # Distance doesn't matter


class Language(str, Enum):
    """Supported languages."""
    ENGLISH = "English"
    SPANISH = "Spanish"
    PORTUGUESE = "Portuguese"


class Gender(str, Enum):
    """Gender options."""
    MALE = "Male"
    FEMALE = "Female"


class GuestKosherRequirement(str, Enum):
    """Guest kosher requirements."""
    KOSHER_HOUSE = "Kosher House"
    KOSHER_TAKEOUT = "Kosher Take out"
    NOT_KOSHER = "Not a Kosher home (Staff member will reach out to you)"


class HostKosherLevel(str, Enum):
    """Host kosher levels."""
    FULL_KOSHER = "Full kosher"
    MIXED = "Mixed dairy and meat dishes"
    VEGETARIAN = "Vegetarian kosher home"


class ContributionRange(str, Enum):
    """Guest contribution comfort ranges."""
    PREFER_NOT_TO_SAY = "Prefer not to say"
    ZERO_TO_TEN = "$0 to $10"
    TEN_TO_TWENTY_FIVE = "$10 to $25"
    TWENTY_FIVE_TO_FIFTY = "$25 to $50"
    FIFTY_PLUS = "$50+"


class HostContributionPreference(str, Enum):
    """Host contribution preferences."""
    NO_CONTRIBUTION = "No contribution needed"
    PREFER_NOT_TO_SAY = "Prefer not to say"
    ZERO_TO_TEN = "$0 to $10"
    TEN_TO_TWENTY_FIVE = "$10 to $25"
    TWENTY_FIVE_TO_FIFTY = "$25 to $50"
    FIFTY_PLUS = "$50+"


class MatchStatus(str, Enum):
    """Match status states (5 states only)."""
    PROPOSED = "proposed"
    REQUESTED = "requested"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    CONFIRMED = "confirmed"


class EmailType(str, Enum):
    """Email types for simulated emails."""
    GUEST_SUBMISSION_CONFIRMATION = "guest_submission_confirmation"
    HOST_SUBMISSION_CONFIRMATION = "host_submission_confirmation"
    MAGIC_LINK = "magic_link"
    MATCH_REQUEST_TO_HOST = "match_request_to_host"
    MATCH_CONFIRMED_GUEST = "match_confirmed_guest"
    MATCH_CONFIRMED_HOST = "match_confirmed_host"
    MATCH_DECLINED_ADMIN = "match_declined_admin"
    DAY_OF_REMINDER_GUEST = "day_of_reminder_guest"
    DAY_OF_SUMMARY_HOST = "day_of_summary_host"
    NOSHOW_REPORT_REQUEST = "noshow_report_request"


class EmailStatus(str, Enum):
    """Email sending status."""
    QUEUED = "queued"
    SENT = "sent"
    FAILED = "failed"


class ActivityType(str, Enum):
    """Activity log action types."""
    GUEST_REGISTERED = "guest_registered"
    GUEST_UPDATED = "guest_updated"
    GUEST_FLAGGED = "guest_flagged"
    HOST_REGISTERED = "host_registered"
    HOST_UPDATED = "host_updated"
    MATCHES_GENERATED = "matches_generated"
    MATCH_EDITED = "match_edited"
    MATCH_REMOVED = "match_removed"
    MATCH_REQUEST_SENT = "match_request_sent"
    MATCH_ACCEPTED = "match_accepted"
    MATCH_DECLINED = "match_declined"
    MATCH_FINALIZED = "match_finalized"
    GUEST_CONFIRMED_ATTENDANCE = "guest_confirmed_attendance"
    NOSHOW_REPORTED = "noshow_reported"
