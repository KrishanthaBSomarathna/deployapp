# order_predictor.py
import pandas as pd

class OrderPredictor:
    def __init__(self, orders):
        # Initialize the OrderPredictor with customer orders
        self.orders = orders

    def prepare_data(self):
        # Prepare a list to hold order data
        data = []

        # Loop through each order and its details
        for date, order_data in self.orders.items():
            for order_id, order_details in order_data.items():
                for item_id, item_details in order_details['items'].items():
                    # Append relevant order information to the data list
                    data.append({
                        'item_id': item_id,
                        'quantity': item_details['quantity'],
                        'total': item_details['total'],
                        'date': date,
                        'unitPrice': item_details['unitPrice'],
                        'division': item_details['division'],
                    })

        # Convert the data list to a DataFrame
        df = pd.DataFrame(data)

        # Convert the 'date' column to datetime format
        df['date'] = pd.to_datetime(df['date'])

        return df

    def predict_future_item_ids(self, df):
        # Group the DataFrame by item_id and aggregate the quantity and total values
        item_summary = df.groupby('item_id').agg({'quantity': 'sum', 'total': 'sum'}).reset_index()

        # Sort items by total quantity ordered, then by total value spent
        item_summary = item_summary.sort_values(by=['quantity', 'total'], ascending=[False, False])

        # Predict the top N items based on past orders
        predicted_item_ids = item_summary['item_id'].head(5).tolist()  # Example: take the top 5 items

        return predicted_item_ids
