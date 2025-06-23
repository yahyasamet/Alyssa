"""
Update ticket tool for Firestore integration.
"""
from .tickets_utils import get_firestore_client
from datetime import datetime

def update_ticket(ticketId: str, update_data: dict) -> dict:
    """
    Update a ticket's status or other fields.

    Args:
        ticketId (str): The ID of the ticket to update.
        update_data (dict): A dictionary with fields to update (e.g., {'status': 'closed', 'priority': 'low'}).

    Returns:
        dict: The result of the update operation.
    """
    try:
        db = get_firestore_client()
        if not db:
            return {"status": "error", "message": "Failed to connect to Firestore."}

        doc_ref = db.collection('tickets').document(ticketId)
        
        # Add updatedAt timestamp
        update_data['updatedAt'] = datetime.now()

        doc_ref.update(update_data)

        return {
            "status": "success",
            "message": f"Ticket '{ticketId}' updated successfully."
        }
    except Exception as e:
        return {"status": "error", "message": f"Error updating ticket: {str(e)}"}
