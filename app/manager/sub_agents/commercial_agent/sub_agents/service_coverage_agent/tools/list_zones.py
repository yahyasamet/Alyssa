"""
List zones tool for Firestore integration.
"""
from .zone_utils import get_firestore_client, serialize_firestore_value

def list_zones() -> dict:
    """
    List all available service coverage zones from the Firestore zones collection.

    Returns:
        dict: A list of all zones or an error message.
    """
    try:
        db = get_firestore_client()
        if not db:
            return {"status": "error", "message": "Failed to connect to Firestore."}

        docs = db.collection('zones').stream()
        zones = []
        for doc in docs:
            zone_data = serialize_firestore_value(doc.to_dict())
            zone_data['id'] = doc.id  # Include document ID
            zones.append(zone_data)

        return {
            "status": "success",
            "count": len(zones),
            "zones": zones
        }
    except Exception as e:
        return {"status": "error", "message": f"Error listing zones: {str(e)}"}
