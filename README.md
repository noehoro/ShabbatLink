# ShabbatLink

ShabbatLink is a web application that connects guests looking for Friday night Shabbat dinners with generous hosts in the Manhattan community. Built for the Jewish Latin Center.

## Features

- **Guest Registration**: Find and join Shabbat dinners with compatible hosts
- **Host Registration**: Offer seats at your Shabbat dinner table
- **Smart Matching**: Algorithm-based matching considering location, kosher requirements, languages, and vibe preferences
- **Admin Panel**: Review matches, send requests, and manage the entire matching workflow
- **Privacy-First**: Contact details only shared after mutual acceptance
- **No-Show Policy**: Built-in attendance tracking and no-show reporting

## Tech Stack

- **Frontend**: Next.js 15 (React), TypeScript, CSS Modules
- **Backend**: Flask (Python), SQLAlchemy
- **Database**: SQLite (dev) / PostgreSQL (production)

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- pip

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
python run.py
```

The backend will start at `http://localhost:5001`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will start at `http://localhost:3000`

## Configuration

### Backend Environment Variables

Create a `.env` file in the `backend` directory:

```env
DATABASE_URL=sqlite:///shabbatlink.db
SECRET_KEY=your-secret-key-here
ADMIN_PASSWORD=admin123
FRONTEND_URL=http://localhost:3000
```

### Frontend Environment Variables

Create a `.env.local` file in the `frontend` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:5001/api
```

## Usage Guide

### For Guests

1. Visit the landing page and click "I Want to Attend"
2. Fill out the registration form with your preferences
3. Wait for matching and confirmation
4. Once confirmed, you'll receive host details and dinner information

### For Hosts

1. Visit the landing page and click "I Want to Host"
2. Fill out the registration form with your details and preferences
3. Receive match requests via email
4. Accept or decline guests with one-click links
5. Once finalized, receive guest contact information

### For Admins

1. Navigate to `/admin` and log in with the admin password
2. View dashboard for overview and alerts
3. Generate matches by clicking "Generate Matches"
4. Review proposed matches and send requests to hosts
5. Finalize accepted matches to release contact details
6. Send day-of reminders and manage no-show reports

## Project Structure

```
ShabbatLink/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── matching/        # Matching engine (isolated module)
│   │   └── utils/           # Helper functions
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── app/                 # Next.js pages
│   │   ├── admin/           # Admin panel
│   │   ├── guest/           # Guest pages
│   │   ├── host/            # Host pages
│   │   ├── auth/            # Authentication
│   │   ├── match/           # Match response
│   │   └── attendance/      # Day-of confirmation
│   ├── components/          # Reusable components
│   │   ├── ui/              # UI components
│   │   ├── form/            # Form components
│   │   └── layout/          # Layout components
│   └── lib/                 # API client, constants
│
└── README.md
```

## Matching Algorithm

The matching engine is isolated and plug-and-play. It considers:

1. **Eligibility**: Capacity, kosher compatibility, language overlap, travel distance
2. **Scoring**: Distance fit, vibe similarity, contribution alignment, capacity balance
3. **Assignment**: Greedy algorithm prioritizing harder-to-place guests

To swap algorithms, implement the `MatchingEngineInterface` and update `matching_adapter.py`.

## Match Status Flow

```
proposed → requested → accepted → confirmed
                   ↘ declined
```

- **proposed**: Admin-only, awaiting review
- **requested**: Sent to host, awaiting response
- **accepted**: Host said yes, awaiting admin finalization
- **declined**: Host said no
- **confirmed**: Finalized, contact details released

## API Endpoints

### Public

- `POST /api/guests` - Register as guest
- `POST /api/hosts` - Register as host
- `POST /api/auth/request-link` - Request magic link
- `POST /api/auth/verify` - Verify magic link
- `POST /api/matches/respond` - Host accept/decline (token-based)
- `POST /api/attendance/confirm` - Guest confirm attendance (token-based)

### Admin (requires authentication)

- `POST /api/admin/auth` - Admin login
- `GET /api/admin/dashboard` - Dashboard stats
- `GET /api/admin/guests` - List guests
- `GET /api/admin/hosts` - List hosts
- `GET /api/admin/matches` - List matches
- `POST /api/admin/matches/generate` - Run matching
- `POST /api/admin/matches/{id}/send` - Send request to host
- `POST /api/admin/matches/{id}/finalize` - Finalize match

## Email System

For the pilot, emails are simulated (logged to console and database). Check the backend console output to see email contents with action links.

## Default Admin Password

The default admin password is `admin123`. Change this in production via the `ADMIN_PASSWORD` environment variable.

## Development Notes

- All styling uses CSS Modules (no inline styles)
- JLC branding colors: Teal (#7ECEC5) and Bronze (#8B7355)
- Three token types: Admin session, Magic link (profile edit), Signed action (one-click)
- The matching engine is completely isolated from Flask/SQLAlchemy

## License

Private project for the Jewish Latin Center.
