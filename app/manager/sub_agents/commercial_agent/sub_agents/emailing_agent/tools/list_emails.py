"""
List emails tool for Gmail integration.
"""

from .gmail_utils import get_gmail_service, get_email_headers


def list_emails(
    max_results: int = 10,
    label: str = "INBOX",
    query: str = "",
) -> dict:
    """
    List emails from Gmail.

    Args:
        max_results (int): Maximum number of emails to return (default: 10)
        label (str): Gmail label to search in (default: "INBOX")
        query (str): Gmail search query (optional)

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

        # Build query with label
        search_query = f"label:{label}"
        if query:
            search_query += f" {query}"

        # Get list of messages
        results = service.users().messages().list(
            userId="me",
            q=search_query,
            maxResults=max_results
        ).execute()

        messages = results.get("messages", [])

        if not messages:
            return {
                "status": "success",
                "message": "No emails found.",
                "emails": [],
            }

        # Get details for each message
        formatted_emails = []
        for message in messages:
            msg = service.users().messages().get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=["From", "To", "Subject", "Date"]
            ).execute()

            headers = get_email_headers(msg["payload"])
            
            formatted_email = {
                "id": message["id"],
                "thread_id": msg.get("threadId", ""),
                "from": headers.get("from", "Unknown"),
                "to": headers.get("to", "Unknown"),
                "subject": headers.get("subject", "No Subject"),
                "date": headers.get("date", "Unknown"),
                "snippet": msg.get("snippet", ""),
                "labels": msg.get("labelIds", []),
            }
            formatted_emails.append(formatted_email)

        return {
            "status": "success",
            "message": f"Found {len(formatted_emails)} email(s).",
            "emails": formatted_emails,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching emails: {str(e)}",
            "emails": [],
        }
