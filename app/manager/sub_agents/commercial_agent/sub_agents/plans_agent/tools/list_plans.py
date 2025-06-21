"""
List plans tool for Firestore integration.
"""
from .plans_utils import get_firestore_client, serialize_firestore_value

def list_plans() -> dict:
    """
    List all available plans from the Firestore plans collection.

    Returns:
        dict: A list of all plans or an error message.
    """
    try:
        db = get_firestore_client()
        if not db:
            return {"status": "error", "message": "Failed to connect to Firestore."}

        docs = db.collection('plans').stream()
        plans = []
        for doc in docs:
            plans.append(serialize_firestore_value(doc.to_dict()))

        return {
            "status": "success",
            "count": len(plans),
            "plans": plans
        }
    except Exception as e:
        return {"status": "error", "message": f"Error listing plans: {str(e)}"}
