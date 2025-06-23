"""
Database utilities for Firestore integration.
"""

from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir,'..', '..', '..', '..', '..', '..', '..')
service_account_path = os.path.join(project_root, 'serviceAccountKey.json')

# Initialize Firebase (following read_firestore_data.py pattern)
cred = credentials.Certificate(service_account_path)
initialize_app(cred)
db = firestore.client()

def get_firestore_client():
    """
    Get the Firestore client instance.
    
    Returns:
        firestore.Client: The Firestore client or None if initialization fails
    """
    try:
        return db
    except Exception as e:
        print(f"Error getting Firestore client: {str(e)}")
        return None

def serialize_firestore_value(value):
    """Convert Firestore native types to readable strings"""
    if isinstance(value, datetime):
        return value.isoformat()
    return value
