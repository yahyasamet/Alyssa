"""
Search users tool for Firestore integration.
"""

from .database_utils import get_firestore_client, serialize_firestore_value


def search_users(field: str, value: str, limit: int = 50) -> dict:
    """
    Search users in the Firestore users collection by a specific field and value.

    Args:
        field (str): The field name to search by (e.g., 'email', 'name', 'status').
        value (str): The value to search for.
        limit (int): Maximum number of users to retrieve. Defaults to 50.

    Returns:
        dict: Information about matching users or error details
    """
    try:
        print(f"Searching users by {field} = {value} with limit: {limit}")
        
        if not field or not field.strip():
            return {
                "status": "error",
                "message": "Field name is required and cannot be empty.",
                "users": [],
            }
            
        if not value or not value.strip():
            return {
                "status": "error",
                "message": "Search value is required and cannot be empty.",
                "users": [],
            }
        
        # Get Firestore client
        db = get_firestore_client()
        if not db:
            return {
                "status": "error",
                "message": "Failed to connect to Firestore. Please check credentials.",
                "users": [],
            }

        # Query users collection with field filter
        users_ref = db.collection('users')
        
        # Apply field filter
        query = users_ref.where(field.strip(), '==', value.strip())
        
        # Apply limit
        if limit > 0:
            docs = query.limit(limit).stream()
        else:
            docs = query.stream()

        # Process documents
        users = []
        count = 0
        for doc in docs:
            doc_data = doc.to_dict()
            if doc_data:
                # Serialize Firestore values
                serialized_data = serialize_firestore_value(doc_data)
                
                user_info = {
                    "id": doc.id,
                    "data": serialized_data
                }
                users.append(user_info)
                count += 1

        if count == 0:
            return {
                "status": "success",
                "message": f"No users found with {field} = '{value}'.",
                "users": [],
                "count": 0
            }

        return {
            "status": "success",
            "message": f"Successfully found {count} users with {field} = '{value}'.",
            "users": users,
            "count": count
        }

    except Exception as e:
        error_message = f"Error searching users by {field} = '{value}': {str(e)}"
        print(error_message)
        return {
            "status": "error",
            "message": error_message,
            "users": [],
        }
