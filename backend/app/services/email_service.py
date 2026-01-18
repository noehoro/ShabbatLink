"""Email service for sending simulated emails."""
from flask import current_app
from app import db
from app.models.email import Email
from app.config import EmailType, EmailStatus


class EmailService:
    """Service for sending and managing emails (simulated for pilot)."""
    
    @staticmethod
    def queue_email(to_email, to_name, email_type, subject, body):
        """Queue an email for sending (simulated)."""
        email = Email(
            to_email=to_email,
            to_name=to_name,
            email_type=email_type,
            subject=subject,
            body=body,
            status=EmailStatus.QUEUED.value
        )
        db.session.add(email)
        db.session.commit()
        
        # For pilot, immediately mark as sent (simulated)
        email.mark_sent()
        db.session.commit()
        
        # Log to console
        print(f"\n{'='*60}")
        print(f"📧 EMAIL SENT (simulated)")
        print(f"To: {to_name} <{to_email}>")
        print(f"Type: {email_type}")
        print(f"Subject: {subject}")
        print(f"{'='*60}")
        print(body)
        print(f"{'='*60}\n")
        
        return email
    
    @classmethod
    def send_guest_submission_confirmation(cls, guest):
        """Send confirmation email when guest submits registration."""
        subject = "Welcome to ShabbatLink - Registration Confirmed!"
        body = f"""
Dear {guest.full_name},

Thank you for registering with ShabbatLink! We're excited to help you find a wonderful Shabbat dinner experience.

What's next?
- Our team will review your preferences and work on finding the perfect match.
- You'll receive an email once we've confirmed a match for you.
- The host's contact details will be shared only after the match is finalized.

Your registration details:
- Party size: {guest.party_size}
- Neighborhood: {guest.neighborhood}
- Kosher requirement: {guest.kosher_requirement}

If you need to update your information, you can request a login link at any time.

Shabbat Shalom!
The ShabbatLink Team
Jewish Latin Center
"""
        return cls.queue_email(
            guest.email,
            guest.full_name,
            EmailType.GUEST_SUBMISSION_CONFIRMATION.value,
            subject,
            body
        )
    
    @classmethod
    def send_host_submission_confirmation(cls, host):
        """Send confirmation email when host submits registration."""
        subject = "Thank You for Hosting - ShabbatLink Registration Confirmed!"
        body = f"""
Dear {host.full_name},

Thank you so much for offering to host a Shabbat dinner through ShabbatLink! Your generosity helps build our community.

What's next?
- We'll send you match requests with guest profiles soon.
- You can review each request and accept or decline.
- Guest contact details will only be shared after you accept and we finalize the match.

Your hosting details:
- Available seats: {host.seats_available}
- Neighborhood: {host.neighborhood}
- Kosher level: {host.kosher_level}

If you need to update your information, you can request a login link at any time.

Shabbat Shalom!
The ShabbatLink Team
Jewish Latin Center
"""
        return cls.queue_email(
            host.email,
            host.full_name,
            EmailType.HOST_SUBMISSION_CONFIRMATION.value,
            subject,
            body
        )
    
    @classmethod
    def send_magic_link(cls, email, name, user_type, link):
        """Send magic link for profile editing."""
        subject = "Your ShabbatLink Login Link"
        body = f"""
Dear {name},

You requested a login link to edit your ShabbatLink profile. Click the link below to access your profile:

{link}

This link will expire in 15 minutes for security reasons.

If you didn't request this link, you can safely ignore this email.

Shabbat Shalom!
The ShabbatLink Team
Jewish Latin Center
"""
        return cls.queue_email(
            email,
            name,
            EmailType.MAGIC_LINK.value,
            subject,
            body
        )
    
    @classmethod
    def send_match_request_to_host(cls, match, accept_link, decline_link):
        """Send match request to host with accept/decline links."""
        guest = match.guest
        host = match.host
        
        subject = f"New Guest Request for Shabbat Dinner - {guest.full_name}"
        body = f"""
Dear {host.full_name},

Great news! We have a potential guest for your Shabbat dinner:

GUEST DETAILS:
- Name: {guest.full_name}
- Party size: {guest.party_size} {'person' if guest.party_size == 1 else 'people'}
- Neighborhood: {guest.neighborhood}
- Languages: {', '.join(guest.languages)}
- Kosher requirement: {guest.kosher_requirement}

WHY IT'S A FIT:
{match.why_its_a_fit}

To respond to this request, simply click one of the links below:

✅ ACCEPT THIS GUEST:
{accept_link}

❌ DECLINE THIS REQUEST:
{decline_link}

Note: The guest's phone number will only be shared after you accept and we finalize the match.

Thank you for being a wonderful host!

Shabbat Shalom!
The ShabbatLink Team
Jewish Latin Center
"""
        return cls.queue_email(
            host.email,
            host.full_name,
            EmailType.MATCH_REQUEST_TO_HOST.value,
            subject,
            body
        )
    
    @classmethod
    def send_match_confirmed_to_guest(cls, match):
        """Send confirmation to guest after admin finalizes match."""
        guest = match.guest
        host = match.host
        
        subject = "You're Confirmed for Shabbat Dinner!"
        body = f"""
Dear {guest.full_name},

Wonderful news! You're confirmed for Shabbat dinner this Friday!

YOUR HOST:
- Name: {host.full_name}
- Address: {host.address}
- Phone: {host.phone}
- Neighborhood: {host.neighborhood}

{f'What to expect: {host.tagline}' if host.tagline else ''}

IMPORTANT REMINDERS:
- Please arrive on time
- If your plans change, contact your host immediately
- Remember: No-shows affect your ability to use ShabbatLink in the future

You'll receive a reminder on Friday to confirm your attendance.

Have a wonderful Shabbat!

Shabbat Shalom!
The ShabbatLink Team
Jewish Latin Center
"""
        return cls.queue_email(
            guest.email,
            guest.full_name,
            EmailType.MATCH_CONFIRMED_GUEST.value,
            subject,
            body
        )
    
    @classmethod
    def send_match_confirmed_to_host(cls, match):
        """Send confirmation to host after admin finalizes match."""
        guest = match.guest
        host = match.host
        
        subject = f"Guest Confirmed - {guest.full_name}"
        body = f"""
Dear {host.full_name},

Your guest is confirmed for Shabbat dinner!

CONFIRMED GUEST:
- Name: {guest.full_name}
- Party size: {guest.party_size} {'person' if guest.party_size == 1 else 'people'}
- Phone: {guest.phone}
- Languages: {', '.join(guest.languages)}

The guest has been given your address and contact information.

Please reach out to your guest before Friday if you'd like to coordinate anything.

Thank you for hosting!

Shabbat Shalom!
The ShabbatLink Team
Jewish Latin Center
"""
        return cls.queue_email(
            host.email,
            host.full_name,
            EmailType.MATCH_CONFIRMED_HOST.value,
            subject,
            body
        )
    
    @classmethod
    def send_day_of_reminder_to_guest(cls, match, confirm_link):
        """Send day-of reminder with attendance confirmation link."""
        guest = match.guest
        host = match.host
        
        subject = "Shabbat Shalom! Please Confirm Your Attendance"
        body = f"""
Shabbat Shalom, {guest.full_name}!

This is a reminder about your Shabbat dinner tonight!

YOUR DINNER DETAILS:
- Host: {host.full_name}
- Address: {host.address}
- Phone: {host.phone}

Please click below to confirm you're attending:

✅ YES, I'M ATTENDING:
{confirm_link}

IMPORTANT: If you can't make it, please contact your host immediately at {host.phone}.

Have a wonderful Shabbat!

The ShabbatLink Team
Jewish Latin Center
"""
        return cls.queue_email(
            guest.email,
            guest.full_name,
            EmailType.DAY_OF_REMINDER_GUEST.value,
            subject,
            body
        )
    
    @classmethod
    def send_day_of_summary_to_host(cls, host, matches):
        """Send day-of summary to host with guest list."""
        subject = "Your Shabbat Dinner Guest List"
        
        guest_list = ""
        total_guests = 0
        for match in matches:
            guest = match.guest
            guest_list += f"- {guest.full_name} (party of {guest.party_size}) - Phone: {guest.phone}\n"
            total_guests += guest.party_size
        
        body = f"""
Shabbat Shalom, {host.full_name}!

Here's your confirmed guest list for tonight's dinner:

CONFIRMED GUESTS ({total_guests} total):
{guest_list}

All guests have been reminded to confirm their attendance.

If a guest doesn't show up, you can report it after the event using the link we'll send you.

Thank you for hosting! Have a wonderful Shabbat!

The ShabbatLink Team
Jewish Latin Center
"""
        return cls.queue_email(
            host.email,
            host.full_name,
            EmailType.DAY_OF_SUMMARY_HOST.value,
            subject,
            body
        )
    
    @classmethod
    def send_noshow_report_request(cls, host, report_link):
        """Send post-event email asking host to report any no-shows."""
        subject = "ShabbatLink - Report Any No-Shows"
        body = f"""
Dear {host.full_name},

Thank you for hosting a Shabbat dinner! We hope it was wonderful.

We'd like to know if all your guests attended. If anyone didn't show up, please let us know so we can follow up:

📋 REPORT ATTENDANCE:
{report_link}

This helps us maintain a reliable community where hosts can count on their guests.

Thank you for being part of ShabbatLink!

Shabbat Shalom!
The ShabbatLink Team
Jewish Latin Center
"""
        return cls.queue_email(
            host.email,
            host.full_name,
            EmailType.NOSHOW_REPORT_REQUEST.value,
            subject,
            body
        )
