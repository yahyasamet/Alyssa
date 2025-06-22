"""
Get invoice statistics tool for Firestore integration.
"""
from .invoice_utils import get_firestore_client, serialize_firestore_value
from datetime import datetime

def get_invoice_stats() -> dict:
    """
    Get statistics about invoices from the Firestore invoices collection.

    Returns:
        dict: Invoice statistics or an error message.
    """
    try:
        db = get_firestore_client()
        if not db:
            return {"status": "error", "message": "Failed to connect to Firestore."}

        docs = db.collection('invoices').stream()
        invoices = []
        for doc in docs:
            invoice_data = serialize_firestore_value(doc.to_dict())
            invoice_data['id'] = doc.id
            invoices.append(invoice_data)

        # Calculate statistics
        total_invoices = len(invoices)
        paid_invoices = len([i for i in invoices if i.get('status') == 'paid'])
        unpaid_invoices = len([i for i in invoices if i.get('status') == 'unpaid'])
        overdue_invoices = len([i for i in invoices if i.get('status') == 'overdue'])
        
        # Get unique users
        unique_users = set()
        for invoice in invoices:
            user_id = invoice.get('userId')
            if user_id:
                unique_users.add(user_id)
        
        # Get plan distribution
        plan_distribution = {}
        for invoice in invoices:
            plan_id = invoice.get('planId')
            if plan_id:
                plan_distribution[plan_id] = plan_distribution.get(plan_id, 0) + 1
        
        # Calculate overdue information (invoices past due date)
        current_time = datetime.now()
        actual_overdue = 0
        for invoice in invoices:
            if invoice.get('status') != 'paid':
                due_date_str = invoice.get('dueDate')
                if due_date_str:
                    try:
                        # Handle different date formats
                        if due_date_str.endswith('Z'):
                            due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                        else:
                            due_date = datetime.fromisoformat(due_date_str)
                        
                        if due_date.replace(tzinfo=None) < current_time:
                            actual_overdue += 1
                    except:
                        continue

        stats = {
            "status": "success",
            "total_invoices": total_invoices,
            "invoice_status": {
                "paid": paid_invoices,
                "unpaid": unpaid_invoices,
                "overdue": overdue_invoices,
                "actual_overdue": actual_overdue
            },
            "user_stats": {
                "total_unique_users": len(unique_users),
                "users_with_invoices": list(unique_users)
            },
            "plan_distribution": plan_distribution,
            "payment_rate": {
                "percentage_paid": round((paid_invoices / total_invoices * 100), 2) if total_invoices > 0 else 0,
                "percentage_overdue": round((actual_overdue / total_invoices * 100), 2) if total_invoices > 0 else 0
            }
        }

        return stats
    except Exception as e:
        return {"status": "error", "message": f"Error getting invoice stats: {str(e)}"}
