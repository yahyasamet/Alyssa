"""
Get user tool for Firestore integration.
"""

from .database_utils import db , serialize_firestore_value


def get_user_by_id(user_id: str) -> dict:
    """
    Get a specific user by ID from the Firestore users collection.

    Args:
        user_id (str): The ID of the user to retrieve

    Returns:
        dict: Information about the user
    """
    try:
        print(f"Getting user with ID: {user_id}")
        
        # Get specific user document
        doc_ref = db.collection('users').document(user_id)
        doc = doc_ref.get()
        
        if doc.exists:
            doc_data = doc.to_dict()
            doc_data = {k: serialize_firestore_value(v) for k, v in doc_data.items()}
            # print(f"User data: {doc_data}")
            return {
                "status": "success",
                "message": f"User found with ID: {user_id}",
                "user": {
                    "id": doc.id,
                    "data": doc_data
                }
            }
        else:
            return {
                "status": "not_found",
                "message": f"No user found with ID: {user_id}",
                "user": None
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving user: {str(e)}",
            "user": None
        }
