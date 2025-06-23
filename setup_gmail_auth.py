#!/usr/bin/env python3
"""
Gmail Authentication Setup Script

This script helps you set up OAuth2 authentication for Gmail access.
Run this script to authorize the application and generate the required token.

Requirements:
1. A credentials.json file from Google Cloud Console with Gmail API enabled
2. The google-auth, google-auth-oauthlib, and google-api-python-client packages

Usage:
    python setup_gmail_auth.py
"""

import json
import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scopes
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send", 
    "https://www.googleapis.com/auth/gmail.modify"
]

# Paths
TOKEN_PATH = Path(os.path.expanduser("~/.credentials/gmail_token.json"))
CREDENTIALS_PATH = Path("credentials.json")


def setup_gmail_auth():
    """Set up Gmail OAuth2 authentication."""
    
    print("Gmail Authentication Setup")
    print("=" * 40)
    
    # Check if credentials.json exists
    if not CREDENTIALS_PATH.exists():
        print(f"❌ Error: {CREDENTIALS_PATH} not found!")
        print("\nTo fix this:")
        print("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
        print("2. Create a new project or select an existing one")
        print("3. Enable the Gmail API")
        print("4. Create OAuth2 credentials (Desktop application)")
        print("5. Download the credentials file and save it as 'credentials.json'")
        return False
    
    print(f"✅ Found credentials file: {CREDENTIALS_PATH}")
    
    # Check if we already have a valid token
    creds = None
    if TOKEN_PATH.exists():
        print(f"✅ Found existing token: {TOKEN_PATH}")
        creds = Credentials.from_authorized_user_info(
            json.loads(TOKEN_PATH.read_text()), SCOPES
        )
    
    # If there are no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("🔐 Starting OAuth2 flow...")
            print("This will open your web browser for authentication.")
            
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        print(f"💾 Saving token to: {TOKEN_PATH}")
        TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_PATH.write_text(creds.to_json())
    
    # Test the connection
    print("🧪 Testing Gmail API connection...")
    try:
        service = build("gmail", "v1", credentials=creds)
        profile = service.users().getProfile(userId="me").execute()
        
        print("✅ Gmail API connection successful!")
        print(f"📧 Email: {profile.get('emailAddress')}")
        print(f"📊 Total messages: {profile.get('messagesTotal', 'Unknown')}")
        print(f"🏷️  Total threads: {profile.get('threadsTotal', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Error testing Gmail API: {e}")
        return False
    
    print("\n🎉 Gmail authentication setup complete!")
    print("You can now use the Gmail agent tools.")
    return True


if __name__ == "__main__":
    setup_gmail_auth()
