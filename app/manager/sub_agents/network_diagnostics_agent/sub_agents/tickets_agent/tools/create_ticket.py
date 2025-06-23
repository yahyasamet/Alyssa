"""
Create ticket tool for Firestore integration.
"""
from datetime import datetime
from .tickets_utils import get_firestore_client, serialize_firestore_value
import uuid

def create_ticket(userId: str, category: str, description: str, priority: str) -> dict:
    """
    Create a new ticket in the Firestore tickets collection.

    Args:
        userId (str): The ID of the user creating the ticket.
        category (str): The category of the ticket (e.g., 'outage', 'billing', 'technical').
        description (str): A detailed description of the issue.
        priority (str): The priority of the ticket (e.g., 'low', 'medium', 'high').

    Returns:
        dict: Result of the create operation including the new ticket ID.
    """
    try:
        db = get_firestore_client()
        if not db:
            return {"status": "error", "message": "Failed to connect to Firestore."}

        tickets_ref = db.collection('tickets')
        
        # Generate a unique ticket ID
        ticket_id = f"TICKET_{str(uuid.uuid4().hex[:6]).upper()}"

        ticket_data = {
            'ticketId': ticket_id,
            'userId': userId,
            'category': category,
            'description': description,
            'priority': priority,
            'status': 'open',
            'createdAt': datetime.now(),
            'updatedAt': datetime.now()
        }

        tickets_ref.document(ticket_id).set(ticket_data)

        return {
            "status": "success",
            "message": "Ticket created successfully.",
            "ticket": serialize_firestore_value(ticket_data)
        }
    except Exception as e:
        return {"status": "error", "message": f"Error creating ticket: {str(e)}"}
