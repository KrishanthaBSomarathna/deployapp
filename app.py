from flask import Flask, request, jsonify, render_template
from firebase_admin import db
from firebase_service import FirebaseService
from order_predictor import OrderPredictor
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
app = Flask(__name__)

# Initialize Firebase Service
SERVICE_ACCOUNT_KEY = 'sak.json'
DATABASE_URL = 'https://go-cart-68aa2-default-rtdb.firebaseio.com/'
firebase_service = FirebaseService(SERVICE_ACCOUNT_KEY, DATABASE_URL)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    customer_id = data.get('customer_id')

    if not customer_id:
        return jsonify({'error': 'Customer ID is required'}), 400

    orders = firebase_service.load_customer_orders(customer_id)
    predictor = OrderPredictor(orders)
    df = predictor.prepare_data()
    predicted_item_ids = predictor.predict_future_item_ids(df)
    item_details = retrieve_item_details(predicted_item_ids)
    firebase_service.store_predictions(customer_id, predicted_item_ids, item_details)

    return jsonify({'predicted_item_ids': predicted_item_ids, 'item_details': item_details})

def retrieve_item_details(item_ids):
    ref = db.reference('shopitem')
    all_shops = ref.get()
    item_details = {}

    if not all_shops:
        print("No items found in 'shopitem' path.")
        return item_details

    if not item_ids:
        print("No item_ids provided.")
        return item_details

    for shop_id, shop_items in all_shops.items():
        for item_id in item_ids:
            item_data = shop_items.get(item_id)
            if item_data:
                item_details[item_id] = item_data
            else:
                print(f"Item ID {item_id} not found under shop ID {shop_id} in 'shopitem'.")

    return item_details

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
