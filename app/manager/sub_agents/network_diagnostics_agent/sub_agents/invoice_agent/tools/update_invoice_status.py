"""
Update invoice status tool for Firestore integration.
"""
from .invoice_utils import get_firestore_client, serialize_firestore_value
from datetime import datetime

def update_invoice_status(invoice_id: str, status: str, paid_at: str = None) -> dict:
    """
    Update an invoice's status in the Firestore invoices collection.

    Args:
        invoice_id (str): The invoice ID to update.
        status (str): New status (paid, unpaid, overdue).
        paid_at (str, optional): Payment timestamp (ISO format).

    Returns:
        dict: Success message or error.
    """
    try:
        if not invoice_id or not status:
            return {"status": "error", "message": "Invoice ID and status are required."}
        
        if status not in ['paid', 'unpaid', 'overdue']:
            return {"status": "error", "message": "Status must be 'paid', 'unpaid', or 'overdue'."}

        db = get_firestore_client()
        if not db:
            return {"status": "error", "message": "Failed to connect to Firestore."}

        # First, find the invoice
        # Try to get by document ID first
        doc_ref = db.collection('invoices').document(invoice_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            # If not found by document ID, search by invoiceId field
            query = db.collection('invoices').where('invoiceId', '==', invoice_id).limit(1)
            docs = list(query.stream())
            
            if not docs:
                return {"status": "error", "message": f"Invoice with ID '{invoice_id}' not found."}
            
            doc_ref = docs[0].reference

        # Prepare update data
        update_data = {"status": status}
        
        # If marking as paid, add timestamp
        if status == "paid":
            if paid_at:
                update_data["paidAt"] = paid_at
            else:
                update_data["paidAt"] = datetime.now().isoformat()
        elif status in ["unpaid", "overdue"]:
            # Remove paidAt field if changing from paid to unpaid/overdue
            update_data["paidAt"] = None

        # Update the document
        doc_ref.update(update_data)

        return {
            "status": "success", 
            "message": f"Invoice {invoice_id} status updated to {status}.",
            "updated_fields": update_data
        }
    
    except Exception as e:
        return {"status": "error", "message": f"Error updating invoice: {str(e)}"}
