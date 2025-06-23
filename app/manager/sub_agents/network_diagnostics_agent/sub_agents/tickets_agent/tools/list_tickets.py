"""
List tickets tool for Firestore integration.
"""
from .tickets_utils import get_firestore_client, serialize_firestore_value

def list_tickets(limit: int) -> dict:
    """
    List tickets from the Firestore tickets collection.

    Args:
        limit (int): Maximum number of tickets to return.

    Returns:
        dict: A list of tickets or an error message.
    """
    try:
        db = get_firestore_client()
        if not db:
            return {"status": "error", "message": "Failed to connect to Firestore."}

        query = db.collection('tickets').order_by('createdAt', direction='DESCENDING').limit(limit)
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
        return {"status": "error", "message": f"Error listing tickets: {str(e)}"}
