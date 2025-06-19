from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("../serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

def serialize_firestore_value(value):
    """Convert Firestore native types to readable strings"""
    if isinstance(value, datetime):
        return value.isoformat()
    return value

def print_collection(collection_name):
    """Read and print all documents from a Firestore collection"""
    print(f"\n--- {collection_name.upper()} ---")
    docs = db.collection(collection_name).stream()
    count = 0
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data = {k: serialize_firestore_value(v) for k, v in doc_data.items()}
        print(f"{doc.id} => {doc_data}")
        count += 1
    if count == 0:
        print("No documents found.")

# List of your collections
collections = [
    "users",
    "tickets",
    "invoices",
    "zones",
    "outages",
    "events",
    "plans"
]

# Print each collection
for col in collections:
    print_collection(col)

print("\nDone printing all Firestore collections.")
