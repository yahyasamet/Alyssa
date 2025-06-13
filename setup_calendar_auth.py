#!/usr/bin/env python3
"""
Google Services Authentication Setup Script

This script helps you set up OAuth 2.0 credentials for Google Calendar and Gmail integration.
Follow the instructions in the console.
"""

import os
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define scopes needed for Google Calendar and Gmail
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify"
]

# Path for token storage
TOKEN_PATH = Path(os.path.expanduser("~/.credentials/google_services_token.json"))
CREDENTIALS_PATH = Path("credentials.json")


def setup_oauth():
    """Set up OAuth 2.0 for Google Calendar and Gmail"""
    print("\n=== Google Services OAuth Setup ===\n")
    print("This will set up access to:")
    print("- Google Calendar (read/write)")
    print("- Gmail (read, send, compose, modify)")
    print()

    if not CREDENTIALS_PATH.exists():
        print(f"Error: {CREDENTIALS_PATH} not found!")
        print("\nTo set up Google Services integration:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select an existing one")
        print("3. Enable the Google Calendar API")
        print("4. Enable the Gmail API")
        print("5. Create OAuth 2.0 credentials (Desktop application)")
        print(
            "6. Download the credentials and save them as 'credentials.json' in this directory"
        )
        print("\nThen run this script again.")
        return False

    print(f"Found credentials.json. Setting up OAuth flow...")

    try:
        # Run the OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_PATH.write_text(creds.to_json())

        print(f"\nSuccessfully saved credentials to {TOKEN_PATH}")

        # Test the Calendar API connection
        print("\n=== Testing Google Calendar API ===")
        calendar_service = build("calendar", "v3", credentials=creds)
        calendar_list = calendar_service.calendarList().list().execute()
        calendars = calendar_list.get("items", [])

        if calendars:
            print(f"✓ Calendar API connected! Found {len(calendars)} calendars:")
            for calendar in calendars:
                print(f"  - {calendar['summary']} ({calendar['id']})")
        else:
            print("✓ Calendar API connected, but no calendars found.")

        # Test the Gmail API connection
        print("\n=== Testing Gmail API ===")
        gmail_service = build("gmail", "v1", credentials=creds)
        
        # Get user profile
        profile = gmail_service.users().getProfile(userId='me').execute()
        email_address = profile.get('emailAddress', 'Unknown')
        messages_total = profile.get('messagesTotal', 0)
        
        print(f"✓ Gmail API connected!")
        print(f"  - Email: {email_address}")
        print(f"  - Total messages: {messages_total}")
        
        # Test listing recent messages
        messages = gmail_service.users().messages().list(
            userId='me', 
            maxResults=5
        ).execute()
        
        recent_messages = messages.get('messages', [])
        print(f"  - Recent messages accessible: {len(recent_messages)}")

        print("\n🎉 OAuth setup complete! You can now use Google Calendar and Gmail integration.")
        print(f"📁 Credentials saved to: {TOKEN_PATH}")
        
        return True

    except Exception as e:
        print(f"\n❌ Error during setup: {str(e)}")
        print("\nTroubleshooting tips:")
        print("- Make sure you've enabled both Calendar and Gmail APIs in Google Cloud Console")
        print("- Verify your credentials.json is for the correct project")
        print("- Check that your OAuth consent screen is configured properly")
        return False


def test_existing_credentials():
    """Test if existing credentials still work"""
    if not TOKEN_PATH.exists():
        print(f"No existing credentials found at {TOKEN_PATH}")
        return False
    
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
        if not creds.valid:
            if creds.expired and creds.refresh_token:
                print("Refreshing expired credentials...")
                creds.refresh(Request())
                TOKEN_PATH.write_text(creds.to_json())
                print("✓ Credentials refreshed successfully")
            else:
                print("❌ Credentials are invalid and cannot be refreshed")
                return False
        
        # Test both services
        calendar_service = build("calendar", "v3", credentials=creds)
        gmail_service = build("gmail", "v1", credentials=creds)
        
        # Quick test calls
        calendar_service.calendarList().list(maxResults=1).execute()
        gmail_service.users().getProfile(userId='me').execute()
        
        print("✓ Existing credentials are working for both Calendar and Gmail")
        return True
        
    except Exception as e:
        print(f"❌ Error testing existing credentials: {str(e)}")
        return False


if __name__ == "__main__":
    print("=== Google Services Authentication Setup ===\n")
    
    # First, try to test existing credentials
    if test_existing_credentials():
        print("\nExisting credentials are working. No setup needed!")
        print("Run setup_oauth() if you want to reconfigure.")
    else:
        print("Setting up new credentials...\n")
        setup_oauth()