"""
Send email tool for Gmail integration.
"""

import base64
from email.mime.text import MIMEText

from .gmail_utils import get_gmail_service


def send_email(
    to: str,
    subject: str,
    body: str,
    cc: str = "",
    bcc: str = "",
) -> dict:
    """
    Send an email via Gmail.

    Args:
        to (str): Recipient email address
        subject (str): Email subject line
        body (str): Email body content
        cc (str): CC recipients (comma-separated if multiple)
        bcc (str): BCC recipients (comma-separated if multiple)

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

        # Create message
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        
        if cc:
            message['cc'] = cc
        if bcc:
            message['bcc'] = bcc

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send the email
        send_result = service.users().messages().send(
            userId="me",
            body={"raw": raw_message}
        ).execute()

        return {
            "status": "success",
            "message": "Email sent successfully",
            "message_id": send_result["id"],
            "thread_id": send_result.get("threadId", ""),
        }

    except Exception as e:
        return {"status": "error", "message": f"Error sending email: {str(e)}"}
