"""
Read email tool for Gmail integration.
"""

from .gmail_utils import get_gmail_service, decode_message_body, get_header_value, format_email_date


def read_email(
    message_id: str
) -> dict:
    """
    Read a specific email by its ID.

    Args:
        message_id (str): The ID of the email to read

    Returns:
        dict: Email content and metadata or error details
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
        message = service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()

        payload = message['payload']
        headers = payload.get('headers', [])

        # Extract email details
        email_data = {
            "id": message['id'],
            "thread_id": message.get('threadId'),
            "subject": get_header_value(headers, 'Subject'),
            "from": get_header_value(headers, 'From'),
            "to": get_header_value(headers, 'To'),
            "cc": get_header_value(headers, 'Cc'),
            "bcc": get_header_value(headers, 'Bcc'),
            "date": format_email_date(get_header_value(headers, 'Date')),
            "body": decode_message_body(payload),
            "snippet": message.get('snippet', ''),
            "labels": message.get('labelIds', []),
        }

        return {
            "status": "success",
            "message": "Email retrieved successfully",
            "email": email_data,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error reading email: {str(e)}",
        }
