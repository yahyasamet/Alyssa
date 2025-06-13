"""
Send email tool for Gmail integration.
"""

from .gmail_utils import get_gmail_service, create_message


def send_email(
    to: str,
    subject: str,
    body: str,
    from_email: str = ""
) -> dict:
    """
    Send an email via Gmail.

    Args:
        to (str): Recipient email address
        subject (str): Email subject
        body (str): Email body content
        from_email (str): Sender email address (optional, uses authenticated account if empty)

    Returns:
        dict: Information about the sent email or error details
    """
    try:
        # Get Gmail service
        service = get_gmail_service()
        if not service:
            return {
                "status": "error",
                "message": "Failed to authenticate with Gmail. Please check credentials.",
            }

        # Create the message
        message = create_message(to, subject, body, from_email if from_email else None)

        # Send the message
        sent_message = service.users().messages().send(
            userId='me',
            body=message
        ).execute()

        return {
            "status": "success",
            "message": "Email sent successfully",
            "message_id": sent_message['id'],
            "thread_id": sent_message.get('threadId'),
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error sending email: {str(e)}",
        }
