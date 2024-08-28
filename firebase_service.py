import firebase_admin
from firebase_admin import credentials, db

class FirebaseService:
    def __init__(self, service_account_key, database_url):
        self.cred = credentials.Certificate(service_account_key)
        self.database_url = database_url

        # Initialize Firebase only if it hasn't been initialized yet
        if not firebase_admin._apps:
            firebase_admin.initialize_app(self.cred, {'databaseURL': self.database_url})

    def load_customer_orders(self, customer_id):
        ref = db.reference(f'Customer/{customer_id}/Orders')
        return ref.get()
    def store_predictions(self, customer_id, item_ids, item_details):
        ref = db.reference(f'Customer/{customer_id}/PredictedItem')
        for item_id in item_ids:
            details = item_details.get(item_id, {})
            unit_price = details.get('price', 0)
            ref.child(item_id).update({
                'cartQty': 1,
                'total': unit_price,
                'unitPrice': unit_price,
                'division': details.get('division', ''),
                'imageUrl': details.get('imageUrl', '')
            })
