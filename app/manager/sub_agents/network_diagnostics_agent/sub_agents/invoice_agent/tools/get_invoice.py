"""
Get invoice tool for Firestore integration.
"""
from .invoice_utils import get_firestore_client, serialize_firestore_value

def get_invoice(invoice_id: str) -> dict:
    """
    Get a specific invoice from the Firestore invoices collection.

    Args:
        invoice_id (str): The invoice ID to retrieve.

    Returns:
        dict: Invoice data or an error message.
    """
    try:
        db = get_firestore_client()
        if not db:
            return {"status": "error", "message": "Failed to connect to Firestore."}

        # Try to get by document ID first
        doc_ref = db.collection('invoices').document(invoice_id)
        doc = doc_ref.get()
        
        if doc.exists:
            invoice_data = serialize_firestore_value(doc.to_dict())
            invoice_data['id'] = doc.id
            return {"status": "success", "invoice": invoice_data}
        
        # If not found by document ID, search by invoiceId field
        query = db.collection('invoices').where('invoiceId', '==', invoice_id).limit(1)
        docs = list(query.stream())
        
        if docs:
            doc = docs[0]
            invoice_data = serialize_firestore_value(doc.to_dict())
            invoice_data['id'] = doc.id
            return {"status": "success", "invoice": invoice_data}
        
        return {"status": "error", "message": f"Invoice with ID '{invoice_id}' not found."}
    
    except Exception as e:
        return {"status": "error", "message": f"Error getting invoice: {str(e)}"}
