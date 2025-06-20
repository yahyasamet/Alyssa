"""
Get user tool for Firestore integration.
"""

from .database_utils import get_firestore_client, serialize_firestore_value


def get_user(user_id: str) -> dict:
    """
    Get a specific user from the Firestore users collection by ID.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        dict: Information about the user or error details
    """
    try:
        print(f"Getting user with ID: {user_id}")
        
        if not user_id or not user_id.strip():
            return {
                "status": "error",
                "message": "User ID is required and cannot be empty.",
                "user": None,
            }
        
        # Get Firestore client
        db = get_firestore_client()
        if not db:
            return {
                "status": "error",
                "message": "Failed to connect to Firestore. Please check credentials.",
                "user": None,
            }

        # Get user document
        user_ref = db.collection('users').document(user_id.strip())
        doc = user_ref.get()

        if not doc.exists:
            return {
                "status": "error",
                "message": f"User with ID '{user_id}' not found in the database.",
                "user": None,
            }

        # Process document
        doc_data = doc.to_dict()
        if doc_data:
            # Serialize Firestore values
            serialized_data = serialize_firestore_value(doc_data)
            
            user_info = {
                "id": doc.id,
                "data": serialized_data
            }
            
            return {
                "status": "success",
                "message": f"Successfully retrieved user '{user_id}' from the database.",
                "user": user_info
            }
        else:
            return {
                "status": "error",
                "message": f"User with ID '{user_id}' exists but has no data.",
                "user": None,
            }

    except Exception as e:
        error_message = f"Error retrieving user '{user_id}': {str(e)}"
        print(error_message)
        return {
            "status": "error",
            "message": error_message,
            "user": None,
        }
