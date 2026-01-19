// API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

// Token storage keys
const AUTH_TOKEN_KEY = 'shabbatlink_auth_token';
const ADMIN_TOKEN_KEY = 'shabbatlink_admin_token';

// Custom error class for API errors
export class ApiError extends Error {
  status: number;
  
  constructor(message: string, status: number = 500) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

// Generic fetch wrapper with error handling
async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Add admin token if available
  const adminToken = getAdminToken();
  if (adminToken) {
    (headers as Record<string, string>)['Authorization'] = `Bearer ${adminToken}`;
  }

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new ApiError(
        data.error || data.message || `Request failed with status ${response.status}`,
        response.status
      );
    }

    return response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError('Network error. Please try again.');
  }
}

// Auth token management
export function setAuthToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem(AUTH_TOKEN_KEY, token);
  }
}

export function getAuthToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(AUTH_TOKEN_KEY);
  }
  return null;
}

export function clearAuthToken(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(AUTH_TOKEN_KEY);
  }
}

// Admin token management
export function setAdminToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem(ADMIN_TOKEN_KEY, token);
  }
}

export function getAdminToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(ADMIN_TOKEN_KEY);
  }
  return null;
}

export function clearAdminToken(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(ADMIN_TOKEN_KEY);
  }
}

// Types
export interface DashboardStats {
  stats: {
    total_guests: number;
    total_hosts: number;
    total_seats: number;
    guests_placed: number;
    pending_decisions: number;
    confirmed_matches: number;
    accepted_awaiting: number;
  };
  alerts: Array<{
    type: 'info' | 'warning' | 'error';
    message: string;
  }>;
}

export interface Guest {
  id: string;
  full_name: string;
  email: string;
  phone: string;
  party_size: number;
  neighborhood: string;
  max_travel_time: number;
  languages: string[];
  kosher_requirement: string;
  contribution_range: string;
  vibe_chabad: number;
  vibe_social: number;
  vibe_formality: number;
  notes_to_admin?: string;
  match_status?: string;
  is_flagged: boolean;
  no_show_count: number;
  created_at: string;
}

export interface Host {
  id: string;
  full_name: string;
  email: string;
  phone: string;
  neighborhood: string;
  seats_available: number;
  languages: string[];
  kosher_level: string;
  contribution_preference: string;
  vibe_chabad: number;
  vibe_social: number;
  vibe_formality: number;
  address?: string;
  tagline?: string;
  private_notes?: string;
  created_at: string;
}

export interface Match {
  id: string;
  guest_id: string;
  host_id: string;
  status: string;
  why_its_a_fit?: string;
  score?: number;
  guest?: Guest;
  host?: Host;
  created_at: string;
  updated_at: string;
}

// Auth APIs
export async function requestMagicLink(email: string): Promise<{ message: string }> {
  return apiFetch('/auth/request-link', {
    method: 'POST',
    body: JSON.stringify({ email }),
  });
}

export async function verifyMagicLink(token: string): Promise<{ 
  token: string; 
  user_type: string; 
  user: { id: string };
}> {
  return apiFetch(`/auth/verify?token=${token}`);
}

export async function adminLogin(password: string): Promise<{ token: string }> {
  return apiFetch('/admin/auth', {
    method: 'POST',
    body: JSON.stringify({ password }),
  });
}

// Guest APIs
export async function createGuest(data: Partial<Guest>): Promise<Guest> {
  return apiFetch('/guests', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function getGuest(id: string): Promise<Guest> {
  return apiFetch(`/guests/${id}`);
}

export async function updateGuest(id: string, data: Partial<Guest>): Promise<Guest> {
  return apiFetch(`/guests/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

// Host APIs
export async function createHost(data: Partial<Host>): Promise<Host> {
  return apiFetch('/hosts', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function getHost(id: string): Promise<Host> {
  return apiFetch(`/hosts/${id}`);
}

export async function updateHost(id: string, data: Partial<Host>): Promise<Host> {
  return apiFetch(`/hosts/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

// Admin - Dashboard
export async function getDashboard(): Promise<DashboardStats> {
  return apiFetch('/admin/dashboard');
}

// Admin - Guests
export async function getAdminGuests(): Promise<Guest[]> {
  return apiFetch('/admin/guests');
}

export async function getAdminGuestDetail(id: string): Promise<Guest> {
  return apiFetch(`/admin/guests/${id}`);
}

export async function flagGuest(id: string, reason: string, flagged: boolean): Promise<{ message: string }> {
  return apiFetch(`/admin/guests/${id}/flag`, {
    method: 'POST',
    body: JSON.stringify({ reason, is_flagged: flagged }),
  });
}

// Admin - Hosts
export async function getAdminHosts(): Promise<Host[]> {
  return apiFetch('/admin/hosts');
}

export async function getAdminHostDetail(id: string): Promise<Host> {
  return apiFetch(`/admin/hosts/${id}`);
}

export async function sendHostSummary(id: string): Promise<{ message: string }> {
  return apiFetch(`/admin/hosts/${id}/send-summary`, {
    method: 'POST',
  });
}

export async function sendNoShowReportRequest(id: string): Promise<{ message: string }> {
  return apiFetch(`/admin/hosts/${id}/send-noshow-request`, {
    method: 'POST',
  });
}

// Admin - Matches
export async function getAdminMatches(status?: string): Promise<Match[]> {
  const params = status ? `?status=${status}` : '';
  return apiFetch(`/admin/matches${params}`);
}

export async function generateMatches(): Promise<{ matches: Match[]; matches_created: number; unmatched_guests: string[]; message: string }> {
  return apiFetch('/admin/matches/generate', {
    method: 'POST',
  });
}

export async function sendMatchRequest(id: string): Promise<{ message: string }> {
  return apiFetch(`/admin/matches/${id}/send`, {
    method: 'POST',
  });
}

export async function finalizeMatch(id: string): Promise<{ message: string }> {
  return apiFetch(`/admin/matches/${id}/finalize`, {
    method: 'POST',
  });
}

export async function editMatch(id: string, hostId: string): Promise<Match> {
  return apiFetch(`/admin/matches/${id}`, {
    method: 'PUT',
    body: JSON.stringify({ host_id: hostId }),
  });
}

export async function deleteMatch(id: string): Promise<{ message: string }> {
  return apiFetch(`/admin/matches/${id}`, {
    method: 'DELETE',
  });
}

export async function sendDayOfReminder(id: string): Promise<{ message: string }> {
  return apiFetch(`/admin/matches/${id}/send-reminder`, {
    method: 'POST',
  });
}

// Match Response (using action token, not session)
export async function getMatchDetails(token: string): Promise<{ match: Match; guest: Guest; host: Partial<Host> }> {
  return apiFetch(`/matches/details?token=${token}`);
}

export async function respondToMatch(token: string, action?: 'accept' | 'decline'): Promise<{ message: string; status: string }> {
  return apiFetch('/matches/respond', {
    method: 'POST',
    body: JSON.stringify(action ? { token, action } : { token }),
  });
}

// Attendance confirmation
export async function confirmAttendance(token: string): Promise<{ 
  message: string; 
  host_name: string; 
  host_address: string; 
  host_phone: string;
}> {
  return apiFetch('/attendance/confirm', {
    method: 'POST',
    body: JSON.stringify({ token }),
  });
}

// No-show reporting
export async function getNoShowReportForm(token: string): Promise<{ 
  host_name: string;
  guests: Array<{ match_id: string; guest_name: string; party_size: number }>;
}> {
  return apiFetch(`/noshow/form?token=${token}`);
}

export async function submitNoShowReport(token: string, guestIds: string[]): Promise<{ message: string }> {
  return apiFetch('/noshow/report', {
    method: 'POST',
    body: JSON.stringify({ token, guest_ids: guestIds }),
  });
}
