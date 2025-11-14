import pandas as pd
import json
from datetime import datetime, timedelta
import os

def read_data(orders_file_path, customers_file_path):
    orders_df = pd.read_csv(orders_file_path)
    customers_df = pd.read_csv(customers_file_path)
    return orders_df, customers_df

def calculate_daily_metrics(orders_df, customers_df):
    if orders_df.empty:
        return {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'total_sales': 0.0,
            'top_5_products': [],
            'customer_largest_purchase': {
                'customer_id': None,
                'customer_name': None,
                'total_amount': 0.0
            }
        }

    orders_df = orders_df.copy()
    orders_df['total_sale'] = orders_df['quantity'] * orders_df['unit_price']
    total_sales = float(orders_df['total_sale'].sum())

    product_sales = orders_df.groupby('product_id').agg({
        'quantity': 'sum',
        'total_sale': 'sum'
    }).reset_index()
    product_sales = product_sales.sort_values('quantity', ascending=False)
    top_5_products = product_sales.head(5)[['product_id','quantity','total_sale']].to_dict('records')

    # Identify largest single-order total (sum of rows per order_id)
    if 'order_id' in orders_df.columns:
        order_totals = orders_df.groupby(['order_id','customer_id'])['total_sale'].sum().reset_index()
        largest = order_totals.loc[order_totals['total_sale'].idxmax()]
        cust_id = int(largest['customer_id'])
        cust_amount = float(largest['total_sale'])
    else:
        order_totals = orders_df.groupby('customer_id')['total_sale'].sum().reset_index()
        largest = order_totals.loc[order_totals['total_sale'].idxmax()]
        cust_id = int(largest['customer_id'])
        cust_amount = float(largest['total_sale'])

    cust_row = customers_df[customers_df['customer_id'] == cust_id]
    cust_name = cust_row['customer_name'].iloc[0] if not cust_row.empty else None

    return {
        'report_date': datetime.now().strftime('%Y-%m-%d'),
        'total_sales': round(total_sales, 2),
        'top_5_products': top_5_products,
        'customer_largest_purchase': {
            'customer_id': cust_id,
            'customer_name': cust_name,
            'total_amount': round(cust_amount, 2)
        }
    }

def generate_daily_report(orders_file_path, customers_file_path, output_path):
    orders_df, customers_df = read_data(orders_file_path, customers_file_path)
    report = calculate_daily_metrics(orders_df, customers_df)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f'Report saved to: {output_path}')
    return report

if __name__ == '__main__':
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    orders_file = f'data/input/orders_{yesterday}.csv'
    customers_file = 'data/input/customers.csv'
    output_file = f'data/output/daily_report_{yesterday}.json'
    generate_daily_report(orders_file, customers_file, output_file)
