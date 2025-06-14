"""
Read email tool for Gmail integration.
"""

from .gmail_utils import get_gmail_service, get_email_headers, decode_email_body


def read_email(
    message_id: str,
) -> dict:
    """
    Read a specific email from Gmail.

    Args:
        message_id (str): The ID of the message to read

    Returns:
        dict: Full email content or error details
    """
    try:
        # Get Gmail service
        service = get_gmail_service()
        if not service:
            return {
                "status": "error",
                "message": "Failed to authenticate with Gmail. Please check credentials.",
            }

        # Get the message
        msg = service.users().messages().get(
            userId="me",
            id=message_id,
            format="full"
        ).execute()

        headers = get_email_headers(msg["payload"])
        body = decode_email_body(msg["payload"])

        return {
            "status": "success",
            "message": "Email retrieved successfully",
            "email": {
                "id": message_id,
                "thread_id": msg.get("threadId", ""),
                "from": headers.get("from", "Unknown"),
                "to": headers.get("to", "Unknown"),
                "cc": headers.get("cc", ""),
                "bcc": headers.get("bcc", ""),
                "subject": headers.get("subject", "No Subject"),
                "date": headers.get("date", "Unknown"),
                "body": body,
                "snippet": msg.get("snippet", ""),
                "labels": msg.get("labelIds", []),
                "size": msg.get("sizeEstimate", 0),
            }
        }

    except Exception as e:
        return {"status": "error", "message": f"Error reading email: {str(e)}"}
