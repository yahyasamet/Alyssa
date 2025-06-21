"""
Get coverage statistics tool for Firestore integration.
"""
from .zone_utils import get_firestore_client, serialize_firestore_value

def get_coverage_stats() -> dict:
    """
    Get statistics about service coverage zones from the Firestore zones collection.

    Returns:
        dict: Coverage statistics or an error message.
    """
    try:
        db = get_firestore_client()
        if not db:
            return {"status": "error", "message": "Failed to connect to Firestore."}

        docs = db.collection('zones').stream()
        zones = []
        for doc in docs:
            zone_data = serialize_firestore_value(doc.to_dict())
            zone_data['id'] = doc.id
            zones.append(zone_data)

        # Calculate statistics
        total_zones = len(zones)
        operational_zones = len([z for z in zones if z.get('status') == 'operational'])
        maintenance_zones = len([z for z in zones if z.get('status') == 'maintenance'])
        offline_zones = len([z for z in zones if z.get('status') == 'offline'])
        
        # Speed statistics
        speeds = [z.get('maxSpeed', 0) for z in zones if z.get('maxSpeed')]
        avg_speed = sum(speeds) / len(speeds) if speeds else 0
        max_speed = max(speeds) if speeds else 0
        min_speed = min(speeds) if speeds else 0
        
        # Technician assignments
        assigned_technicians = set()
        for zone in zones:
            tech = zone.get('technicianAssigned')
            if tech:
                assigned_technicians.add(tech)
        
        stats = {
            "status": "success",
            "total_zones": total_zones,
            "zone_status": {
                "operational": operational_zones,
                "maintenance": maintenance_zones,
                "offline": offline_zones
            },
            "speed_stats": {
                "average_speed": round(avg_speed, 2),
                "max_speed": max_speed,
                "min_speed": min_speed
            },
            "technician_stats": {
                "total_assigned_technicians": len(assigned_technicians),
                "assigned_technicians": list(assigned_technicians)
            },
            "coverage_percentage": {
                "operational": round((operational_zones / total_zones * 100), 2) if total_zones > 0 else 0
            }
        }

        return stats
    except Exception as e:
        return {"status": "error", "message": f"Error getting coverage stats: {str(e)}"}
