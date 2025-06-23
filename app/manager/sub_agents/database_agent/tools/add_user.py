

from .database_utils import db, serialize_firestore_value
from datetime import datetime

def add_user(fullname :str , email :str , phone :str , zone :str , planId :str , subscriptionStatus :str) -> dict:
    """
    Add a new user to the Firestore users collection.

    Args:
        fullname (str): User's full name
        email (str): User's email address
        phone (str, optional): User's phone number
        zone (str, optional): User's zone
        planId (str, optional): User's plan ID
        subscriptionStatus (str, optional): User's subscription status

    Returns:
        dict: Result of the add operation including the new user ID
    """
    try:
        # Create user_data dictionary from parameters
        user_data = {
            'fullName': fullname,
            'email': email,
            'phone': phone,
            'zone': zone,
            'planId': planId,
            'subscriptionStatus': subscriptionStatus
        }
        
        print(f"Adding user with data: {user_data}")
        
        # Validate required fields
        if not fullname or not email:
            return {
                "status": "error",
                "message": "Missing required field: fullName or email",
                "user_id": None
            }
        
        # Add timestamp
        user_data['createdAt'] = datetime.now()
        user_data['updatedAt'] = datetime.now()
        
        # Get users collection reference
        users_ref = db.collection('users')
        
        # Add the user to Firestore
        doc_ref = users_ref.add(user_data)
        user_id = doc_ref[1].id  # Get the document ID
        
        return {
            "status": "success",
            "message": f"User added successfully",
            "user_id": user_id,
            "data": {k: serialize_firestore_value(v) for k, v in user_data.items()}
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error adding user: {str(e)}",
            "user_id": None
        }