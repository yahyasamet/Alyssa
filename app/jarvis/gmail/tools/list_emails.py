"""
List emails tool for Gmail integration.
"""

from .gmail_utils import get_gmail_service, decode_message_body, get_header_value, format_email_date


def list_emails(
    query: str = "",
    max_results: int = 10,
    include_body: bool = False
) -> dict:
    """
    List emails from Gmail inbox with optional search query.

    Args:
        query (str): Gmail search query (e.g., "is:unread", "from:example@gmail.com", "subject:meeting")
        max_results (int): Maximum number of emails to return (default: 10)
        include_body (bool): Whether to include email body content (default: False)

    Returns:
        dict: Information about emails or error details
    """
    try:
        # Get Gmail service
        service = get_gmail_service()
        if not service:
            return {
                "status": "error",
                "message": "Failed to authenticate with Gmail. Please check credentials.",
                "emails": [],
            }

        # Search for messages
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            return {
                "status": "success",
                "message": "No emails found matching the criteria.",
                "emails": [],
            }

        # Get detailed information for each message
        emails = []
        for message in messages:
            msg = service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()

            payload = msg['payload']
            headers = payload.get('headers', [])

            email_data = {
                "id": message['id'],
                "thread_id": msg.get('threadId'),
                "subject": get_header_value(headers, 'Subject'),
                "from": get_header_value(headers, 'From'),
                "to": get_header_value(headers, 'To'),
                "date": format_email_date(get_header_value(headers, 'Date')),
                "snippet": msg.get('snippet', ''),
                "labels": msg.get('labelIds', []),
            }

            # Include body if requested
            if include_body:
                email_data["body"] = decode_message_body(payload)

            emails.append(email_data)

        return {
            "status": "success",
            "message": f"Found {len(emails)} email(s).",
            "emails": emails,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching emails: {str(e)}",
            "emails": [],
        }
