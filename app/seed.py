from firebase_admin import credentials, firestore, initialize_app
import json
import os
from datetime import datetime

def parse_timestamp(timestamp_str):
    """Convert ISO timestamp string to datetime object"""
    if timestamp_str is None:
        return None
    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

def load_json_data(filename):
    """Load data from JSON file"""
    filepath = os.path.join("database", filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Warning: {filepath} not found")
        return []
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in {filepath}")
        return []

def seed_collection(collection_name, data_list, id_field):
    """Seed a Firestore collection with data from JSON"""
    collection_ref = db.collection(collection_name)
    
    for item in data_list:
        # Create a copy to avoid modifying original data
        item_data = item.copy()
        
        # Get document ID from the specified field
        doc_id = item_data.get(id_field)
        if not doc_id:
            print(f"Warning: No {id_field} found for item in {collection_name}")
            continue
        
        # Convert timestamp strings to datetime objects
        for key, value in item_data.items():
            if key.endswith('At') or key.endswith('Time') or key.endswith('Date'):
                if isinstance(value, str):
                    item_data[key] = parse_timestamp(value)
                elif value is None:
                    item_data[key] = None
        
        # Add server timestamp for createdAt if not present
        if 'createdAt' not in item_data:
            item_data['createdAt'] = firestore.SERVER_TIMESTAMP
        
        try:
            collection_ref.document(doc_id).set(item_data)
            print(f"✓ Added {doc_id} to {collection_name}")
        except Exception as e:
            print(f"✗ Error adding {doc_id} to {collection_name}: {e}")

# Initialize Firebase
cred = credentials.Certificate("../serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

print("Starting database seeding...")

# Load and seed all collections
collections_config = [
    ("users", "users.json", "userId"),
    ("tickets", "tickets.json", "ticketId"),
    ("invoices", "invoices.json", "invoiceId"),
    ("zones", "zones.json", "zoneId"),
    ("outages", "outages.json", "outageId"),
    ("events", "events.json", "eventId"),
    ("plans", "plans.json", "planId")
]

for collection_name, json_filename, id_field in collections_config:
    print(f"\nSeeding {collection_name}...")
    data = load_json_data(json_filename)
    if data:
        seed_collection(collection_name, data, id_field)
    else:
        print(f"No data found for {collection_name}")

print("\nDatabase seeding completed!")
