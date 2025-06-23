"""
Database utilities for Firestore integration for invoices.
"""

from firebase_admin import credentials, firestore, initialize_app, _apps
from datetime import datetime
import os

# This ensures Firebase is initialized only once.
if not _apps:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..', '..', '..', '..')
    service_account_path = os.path.join(project_root, 'serviceAccountKey.json')
    cred = credentials.Certificate(service_account_path)
    initialize_app(cred)

db = firestore.client()

def get_firestore_client():
    """
    Get the Firestore client instance.
    """
    return db

def serialize_firestore_value(value):
    """Convert Firestore native types to readable strings, handling nested structures."""
    if isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, dict):
        return {k: serialize_firestore_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [serialize_firestore_value(v) for v in value]
    return value
