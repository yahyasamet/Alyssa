"""
Create plan tool for Firestore integration.
"""
from datetime import datetime
from .plans_utils import get_firestore_client

def create_plan(planId: str, name: str, price: float, speed: int, type: str) -> dict:
    """
    Create a new plan in the Firestore plans collection.

    Args:
        planId (str): The unique ID for the plan (e.g., 'basic_20').
        name (str): The display name of the plan (e.g., 'Basic 20Mbps').
        price (float): The price of the plan.
        speed (int): The speed of the plan in Mbps.
        type (str): The type of the plan (e.g., 'basic', 'fiber').

    Returns:
        dict: Result of the create operation.
    """
    try:
        db = get_firestore_client()
        if not db:
            return {"status": "error", "message": "Failed to connect to Firestore."}

        doc_ref = db.collection('plans').document(planId)
        plan_data = {
            'planId': planId,
            'name': name,
            'price': price,
            'speed': speed,
            'type': type,
            'createdAt': datetime.now()
        }
        doc_ref.set(plan_data)

        return {
            "status": "success",
            "message": "Plan created successfully.",
            "planId": planId
        }
    except Exception as e:
        return {"status": "error", "message": f"Error creating plan: {str(e)}"}
