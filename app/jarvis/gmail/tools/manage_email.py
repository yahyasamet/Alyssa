"""
Manage email tool for Gmail integration.
"""

from .gmail_utils import get_gmail_service


def manage_email(
    message_id: str,
    action: str
) -> dict:
    """
    Manage an email (mark as read/unread, delete, archive, etc.).

    Args:
        message_id (str): The ID of the email to manage
        action (str): Action to perform ("mark_read", "mark_unread", "delete", "archive", "star", "unstar")

    Returns:
        dict: Operation status and details
    """
    try:
        # Get Gmail service
        service = get_gmail_service()
        if not service:
            return {
                "status": "error",
                "message": "Failed to authenticate with Gmail. Please check credentials.",
            }

        if action == "mark_read":
            # Remove UNREAD label
            service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            message = "Email marked as read"

        elif action == "mark_unread":
            # Add UNREAD label
            service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': ['UNREAD']}
            ).execute()
            message = "Email marked as unread"

        elif action == "delete":
            # Move to trash
            service.users().messages().trash(
                userId='me',
                id=message_id
            ).execute()
            message = "Email moved to trash"

        elif action == "archive":
            # Remove INBOX label
            service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['INBOX']}
            ).execute()
            message = "Email archived"

        elif action == "star":
            # Add STARRED label
            service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': ['STARRED']}
            ).execute()
            message = "Email starred"

        elif action == "unstar":
            # Remove STARRED label
            service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['STARRED']}
            ).execute()
            message = "Email unstarred"

        else:
            return {
                "status": "error",
                "message": f"Unknown action: {action}. Available actions: mark_read, mark_unread, delete, archive, star, unstar"
            }

        return {
            "status": "success",
            "message": message,
            "message_id": message_id,
            "action": action,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error managing email: {str(e)}",
        }
