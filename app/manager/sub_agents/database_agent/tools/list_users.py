"""
List users tool for Firestore integration.
"""

from .database_utils import db, serialize_firestore_value


def list_users() -> dict:
    """
    List users from the Firestore users collection.

    Returns:
        dict: Information about users
    """
    try:
        print("Listing users from database")
        
        # Get users collection
        docs = db.collection('users').stream()
        
        users = []
        count = 0
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data = {k: serialize_firestore_value(v) for k, v in doc_data.items()}
            users.append({
                "id": doc.id,
                "data": doc_data
            })
            count += 1

        return {
            "status": "success",
            "message": f"Found {count} users",
            "users": users,
            "count": count
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving users: {str(e)}",
            "users": [],
        }
