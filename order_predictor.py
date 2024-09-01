import pandas as pd

class OrderPredictor:
    def __init__(self, orders):
        # Initialize the OrderPredictor with customer orders
        self.orders = orders

    def prepare_data(self):
        data = []

        # Check if orders data is empty or not in expected format
        if not self.orders or not isinstance(self.orders, dict):
            print("No valid orders data found.")
            return pd.DataFrame()  # Return empty DataFrame

        for date, order_data in self.orders.items():
            # Ensure that order_data is a dictionary
            if not isinstance(order_data, dict):
                print(f"Unexpected order data format for date {date}: {order_data}")
                continue

            for order_id, order_details in order_data.items():
                # Debug print to check the format of order_details
                print(f"Order Details for Order ID {order_id}: {order_details}")

                # Ensure that order_details is a dictionary and has 'items'
                if not isinstance(order_details, dict) or 'items' not in order_details:
                    print(f"Missing or incorrect items field for order ID {order_id}: {order_details}")
                    continue

                items = order_details.get('items', {})

                # Ensure 'items' is a dictionary
                if not isinstance(items, dict):
                    print(f"Unexpected items format for order ID {order_id}: {items}")
                    continue

                for item_id, item_details in items.items():
                    # Ensure item_details is a dictionary and has required fields
                    if not isinstance(item_details, dict):
                        print(f"Unexpected item details format for item ID {item_id}: {item_details}")
                        continue

                    data.append({
                        'item_id': item_id,
                        'item_name': item_details.get('itemName', ''),
                        'quantity': item_details.get('quantity', 0),
                        'total': item_details.get('total', 0),
                        'date': date,
                        'unitPrice': item_details.get('unitPrice', 0),
                        'division': item_details.get('division', ''),
                        'imageUrl': item_details.get('imageUrl', ''),
                    })

        # Convert the data list to a DataFrame
        df = pd.DataFrame(data)
        # Convert the 'date' column to datetime format
        df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Handle any invalid dates

        return df

    def predict_future_item_ids(self, df):
        # Group the DataFrame by item_id, item_name and aggregate the quantity and total values
        item_summary = df.groupby(['item_id', 'item_name']).agg({
            'quantity': 'sum', 
            'total': 'sum',
            'unitPrice': 'min'  # Get the minimum unit price for items with the same name
        }).reset_index()

        # Sort items by item_name, then by unitPrice (ascending) and total quantity (descending)
        item_summary = item_summary.sort_values(by=['item_name', 'unitPrice', 'quantity'], ascending=[True, True, False])

        # Filter to keep only the item with the lowest unit price for each item name
        filtered_item_summary = item_summary.drop_duplicates(subset=['item_name'], keep='first')

        # Predict the top N items based on past orders
        predicted_item_ids = filtered_item_summary['item_id'].head(5).tolist()  # Example: take the top 5 items

        return predicted_item_ids
