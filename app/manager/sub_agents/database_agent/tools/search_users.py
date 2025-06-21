"""
Search users tool for Firestore integration.
"""

from .database_utils import db, serialize_firestore_value


def search_users(query: str, field: str, limit: int = 10) -> dict:
    """
    Search users in the Firestore users collection.

    Args:
        query (str, optional): Search term to filter users
        field (str, optional): Specific field to search in ("fullName", "email", "phone", "zone", "planId", "subscriptionStatus", etc.). If None, searches all fields
        limit (int): Maximum number of users to return (default: 10)

    Returns:
        dict: List of users matching the search criteria
    """
    try:
        print(f"Searching users with query: {query}, field: {field}, limit: {limit}")
        
        # Get users collection reference
        users_ref = db.collection('users')
        
        # If no query provided, get all users (limited)
        if not query:
            docs = users_ref.limit(limit).stream()
        else:
            # Search by specified field or all fields (case-insensitive)
            query_lower = query.lower()
            docs = users_ref.limit(limit).stream()
        
        users = []
        for doc in docs:
            if doc.exists:
                doc_data = doc.to_dict()
                
                # If query provided, filter results
                if query:
                    match_found = False
                    
                    if field:
                        # Search in specific field
                        field_value = str(doc_data.get(field, '')).lower()
                        if query_lower in field_value:
                            match_found = True
                    else:
                        # Search in common fields based on your data structure
                        searchable_fields = ['fullName', 'email', 'phone', 'zone', 'planId', 'subscriptionStatus', 'userId']
                        for search_field in searchable_fields:
                            field_value = str(doc_data.get(search_field, '')).lower()
                            if query_lower in field_value:
                                match_found = True
                                break
                    
                    if not match_found:
                        continue
                
                doc_data = {k: serialize_firestore_value(v) for k, v in doc_data.items()}
                users.append({
                    "id": doc.id,
                    "data": doc_data
                })
        
        return {
            "status": "success",
            "message": f"Found {len(users)} users",
            "users": users,
            "total": len(users)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error searching users: {str(e)}",
            "users": [],
            "total": 0
        }
        
