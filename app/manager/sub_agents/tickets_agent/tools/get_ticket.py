"""
Get ticket tool for Firestore integration.
"""
from .tickets_utils import get_firestore_client, serialize_firestore_value

def get_ticket(ticketId: str) -> dict:
    """
    Get a specific ticket by its ID.

    Args:
        ticketId (str): The ID of the ticket to retrieve.

    Returns:
        dict: The ticket data or an error message.
    """
    try:
        db = get_firestore_client()
        if not db:
            return {"status": "error", "message": "Failed to connect to Firestore."}

        doc_ref = db.collection('tickets').document(ticketId)
        doc = doc_ref.get()

        if not doc.exists:
            return {"status": "not_found", "message": f"Ticket with ID '{ticketId}' not found."}

        return {
            "status": "success",
            "ticket": serialize_firestore_value(doc.to_dict())
        }
    except Exception as e:
        return {"status": "error", "message": f"Error getting ticket: {str(e)}"}
