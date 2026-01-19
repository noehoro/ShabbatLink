// Match statuses as defined in PRD
export const MATCH_STATUSES = {
  proposed: { label: 'Proposed', color: 'gray' },
  requested: { label: 'Requested', color: 'blue' },
  accepted: { label: 'Accepted', color: 'yellow' },
  declined: { label: 'Declined', color: 'red' },
  confirmed: { label: 'Confirmed', color: 'green' },
} as const;

export type MatchStatus = keyof typeof MATCH_STATUSES;

// Neighborhoods (Manhattan)
export const NEIGHBORHOODS = [
  'Upper West Side',
  'Upper East Side',
  'Midtown West',
  'Midtown East',
  'Murray Hill',
  'Gramercy / Flatiron',
  'Chelsea',
  'Greenwich Village / West Village',
  'East Village / NoHo',
  'SoHo / Tribeca',
  'Lower East Side',
  'Financial District',
  'Washington Heights',
  'Harlem',
] as const;

export type Neighborhood = typeof NEIGHBORHOODS[number];

// Languages
export const LANGUAGES = ['English', 'Spanish', 'Portuguese'] as const;
export type Language = typeof LANGUAGES[number];

// Kosher requirements (guest)
export const KOSHER_REQUIREMENTS = [
  'Full kosher only',
  'Mixed dairy and meat dishes ok',
  'Vegetarian kosher home ok',
] as const;

// Kosher levels (host)
export const KOSHER_LEVELS = [
  'Full kosher',
  'Mixed dairy and meat dishes',
  'Vegetarian kosher home',
] as const;

// Contribution ranges
export const CONTRIBUTION_RANGES = [
  'Prefer not to say',
  '$0 to $10',
  '$10 to $25',
  '$25 to $50',
  '$50+',
] as const;

// Host contribution preferences
export const HOST_CONTRIBUTION_PREFERENCES = [
  'No contribution needed',
  'Prefer not to say',
  '$0 to $10',
  '$10 to $25',
  '$25 to $50',
  '$50+',
] as const;

// Travel time options
export const TRAVEL_TIMES = [
  { value: 15, label: '15 minutes' },
  { value: 30, label: '30 minutes' },
  { value: 45, label: '45 minutes' },
  { value: 60, label: '60 minutes' },
] as const;

// Gender options (for Select dropdown)
export const GENDER_OPTIONS = [
  { value: 'male', label: 'Male' },
  { value: 'female', label: 'Female' },
  { value: 'other', label: 'Other' },
  { value: 'prefer_not_to_say', label: 'Prefer not to say' },
];

// Guest kosher options (for RadioGroup - simple strings)
export const GUEST_KOSHER_OPTIONS = [
  'Full kosher only',
  'Mixed dairy and meat dishes ok',
  'Vegetarian kosher home ok',
];

// Host kosher options (for RadioGroup - simple strings)
export const HOST_KOSHER_OPTIONS = [
  'Full kosher',
  'Mixed dairy and meat dishes',
  'Vegetarian kosher home',
];

// Host contribution options (for Select dropdown)
export const HOST_CONTRIBUTION_OPTIONS = [
  { value: 'none', label: 'No contribution needed' },
  { value: 'prefer_not_to_say', label: 'Prefer not to say' },
  { value: '0_10', label: '$0 to $10' },
  { value: '10_25', label: '$10 to $25' },
  { value: '25_50', label: '$25 to $50' },
  { value: '50_plus', label: '$50+' },
];

// Vibe slider labels
export const VIBE_LABELS = {
  chabad: {
    label: 'Chabad Energy',
    low: 'Chill',
    high: 'Full on',
  },
  social: {
    label: 'Social Intensity',
    low: 'Intimate',
    high: 'Big group',
  },
  formality: {
    label: 'Formality',
    low: 'Casual',
    high: 'Formal',
  },
};
