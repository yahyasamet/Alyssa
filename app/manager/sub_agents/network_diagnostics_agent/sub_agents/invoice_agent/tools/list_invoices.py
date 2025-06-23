"""
List invoices tool for Firestore integration.
"""
from .invoice_utils import get_firestore_client, serialize_firestore_value

def list_invoices(user_id: str , status: str) -> dict:
    """
    List invoices from the Firestore invoices collection.

    Args:
        user_id (str, optional): Filter by user ID.
        status (str, optional): Filter by status (paid, unpaid, overdue).

    Returns:
        dict: List of invoices or an error message.
    """
    try:
        db = get_firestore_client()
        if not db:
            return {"status": "error", "message": "Failed to connect to Firestore."}

        query = db.collection('invoices')
        
        # Apply filters
        if user_id:
            query = query.where('userId', '==', user_id)
        if status:
            query = query.where('status', '==', status)

        docs = query.stream()
        invoices = []
        for doc in docs:
            invoice_data = serialize_firestore_value(doc.to_dict())
            invoice_data['id'] = doc.id
            invoices.append(invoice_data)

        return {
            "status": "success",
            "invoices": invoices,
            "count": len(invoices)
        }
    except Exception as e:
        return {"status": "error", "message": f"Error listing invoices: {str(e)}"}
