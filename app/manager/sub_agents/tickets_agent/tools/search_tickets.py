"""
Search tickets tool for Firestore integration.
"""
from .tickets_utils import get_firestore_client, serialize_firestore_value

def search_tickets(field: str, value: str) -> dict:
    """
    Search tickets in the Firestore tickets collection by a specific field and value.

    Args:
        field (str): The field to search by (e.g., 'status', 'priority', 'userId', 'category').
        value (str): The value to search for.
    Returns:
        dict: A list of matching tickets or an error message.
    """
    try:
        db = get_firestore_client()
        if not db:
            return {"status": "error", "message": "Failed to connect to Firestore."}

        query = db.collection('tickets').where(field, '==', value)
        docs = query.stream()

        tickets = []
        for doc in docs:
            tickets.append(serialize_firestore_value(doc.to_dict()))

        return {
            "status": "success",
            "count": len(tickets),
            "tickets": tickets
        }
    except Exception as e:
        return {"status": "error", "message": f"Error searching tickets: {str(e)}"}
