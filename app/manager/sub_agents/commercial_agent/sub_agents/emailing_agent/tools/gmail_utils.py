"""
Utility functions for Gmail integration.
"""

import json
import os
from datetime import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define scopes needed for Gmail
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify"
]

# Path for token storage
TOKEN_PATH = Path(os.path.expanduser("~/.credentials/gmail_token.json"))
CREDENTIALS_PATH = Path("credentials.json")


def get_gmail_service():
    """
    Authenticate and create a Gmail service object.

    Returns:
        A Gmail service object or None if authentication fails
    """
    creds = None

    # Check if token exists and is valid
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_info(
            json.loads(TOKEN_PATH.read_text()), SCOPES
        )

    # If credentials don't exist or are invalid, refresh or get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # If credentials.json doesn't exist, we can't proceed with OAuth flow
            if not CREDENTIALS_PATH.exists():
                print(
                    f"Error: {CREDENTIALS_PATH} not found. Please follow setup instructions."
                )
                return None

            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_PATH.write_text(creds.to_json())

    # Create and return the Gmail service
    return build("gmail", "v1", credentials=creds)


def format_email_date(date_str):
    """
    Format an email date into a human-readable string.

    Args:
        date_str (str): The date string from Gmail API

    Returns:
        str: A human-readable date string
    """
    try:
        # Gmail API returns dates in RFC 2822 format
        dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
        return dt.strftime("%Y-%m-%d %I:%M %p")
    except ValueError:
        return date_str


def get_current_time() -> dict:
    """
    Get the current time and date
    """
    now = datetime.now()

    # Format date as MM-DD-YYYY
    formatted_date = now.strftime("%m-%d-%Y")

    return {
        "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "formatted_date": formatted_date,
    }


def decode_email_body(payload):
    """
    Decode email body from Gmail API response.
    
    Args:
        payload: The payload from Gmail API
        
    Returns:
        str: Decoded email body
    """
    body = ""
    
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                if "data" in part["body"]:
                    body = part["body"]["data"]
                    break
            elif part["mimeType"] == "text/html" and not body:
                if "data" in part["body"]:
                    body = part["body"]["data"]
    else:
        if payload["mimeType"] == "text/plain" or payload["mimeType"] == "text/html":
            if "data" in payload["body"]:
                body = payload["body"]["data"]
    
    if body:
        import base64
        return base64.urlsafe_b64decode(body).decode('utf-8')
    
    return "No readable content found"


def get_email_headers(payload):
    """
    Extract common headers from email payload.
    
    Args:
        payload: The payload from Gmail API
        
    Returns:
        dict: Dictionary with common email headers
    """
    headers = {}
    for header in payload.get("headers", []):
        name = header["name"]
        value = header["value"]
        
        if name.lower() in ["from", "to", "subject", "date", "cc", "bcc"]:
            headers[name.lower()] = value
    
    return headers
