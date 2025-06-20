"""
Database utilities for Firestore integration.
"""

from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..', '..', '..', '..')
service_account_path = os.path.join(project_root, 'serviceAccountKey.json')

# Initialize Firebase (following read_firestore_data.py pattern)
cred = credentials.Certificate(service_account_path)
initialize_app(cred)
db = firestore.client()

def serialize_firestore_value(value):
    """Convert Firestore native types to readable strings"""
    if isinstance(value, datetime):
        return value.isoformat()
    return value
