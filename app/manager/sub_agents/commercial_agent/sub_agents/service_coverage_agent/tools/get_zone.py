"""
Get zone tool for Firestore integration.
"""
from .zone_utils import get_firestore_client, serialize_firestore_value

def get_zone(zone_id: str) -> dict:
    """
    Get a specific service coverage zone by its ID from the Firestore zones collection.

    Args:
        zone_id (str): The ID of the zone to retrieve.

    Returns:
        dict: The zone data or an error message.
    """
    try:
        if not zone_id:
            return {"status": "error", "message": "Zone ID is required."}

        db = get_firestore_client()
        if not db:
            return {"status": "error", "message": "Failed to connect to Firestore."}

        doc_ref = db.collection('zones').document(zone_id)
        doc = doc_ref.get()

        if not doc.exists:
            return {"status": "error", "message": f"Zone with ID '{zone_id}' not found."}

        zone_data = serialize_firestore_value(doc.to_dict())
        zone_data['id'] = doc.id  # Include document ID

        return {
            "status": "success",
            "zone": zone_data
        }
    except Exception as e:
        return {"status": "error", "message": f"Error getting zone: {str(e)}"}
