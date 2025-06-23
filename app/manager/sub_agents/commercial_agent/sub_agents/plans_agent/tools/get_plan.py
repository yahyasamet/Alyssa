"""
Get plan tool for Firestore integration.
"""
from .plans_utils import get_firestore_client, serialize_firestore_value

def get_plan(planId: str) -> dict:
    """
    Get a specific plan by its ID.

    Args:
        planId (str): The ID of the plan to retrieve (e.g., 'basic_20').

    Returns:
        dict: The plan data or an error message.
    """
    try:
        db = get_firestore_client()
        if not db:
            return {"status": "error", "message": "Failed to connect to Firestore."}

        doc_ref = db.collection('plans').document(planId)
        doc = doc_ref.get()

        if not doc.exists:
            return {"status": "not_found", "message": f"Plan with ID '{planId}' not found."}

        return {
            "status": "success",
            "plan": serialize_firestore_value(doc.to_dict())
        }
    except Exception as e:
        return {"status": "error", "message": f"Error getting plan: {str(e)}"}
