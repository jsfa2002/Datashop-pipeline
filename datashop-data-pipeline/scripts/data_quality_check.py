import pandas as pd
import sys

def validate_orders_data(orders_df):
    errors = []
    expected_columns = ['order_id', 'customer_id', 'product_id', 'quantity', 'unit_price', 'order_date']
    missing = set(expected_columns) - set(orders_df.columns)
    if missing:
        errors.append(f'Missing columns in orders: {sorted(list(missing))}')
    for c in ['order_id','customer_id']:
        if c in orders_df.columns and orders_df[c].isnull().any():
            errors.append(f'Null values found in {c}')
    if 'quantity' in orders_df.columns:
        if not pd.api.types.is_numeric_dtype(orders_df['quantity']):
            errors.append('quantity must be numeric')
        elif (orders_df['quantity'] <= 0).any():
            errors.append('quantity must be > 0 for all rows')
    if 'unit_price' in orders_df.columns:
        if not pd.api.types.is_numeric_dtype(orders_df['unit_price']):
            errors.append('unit_price must be numeric')
        elif (orders_df['unit_price'] < 0).any():
            errors.append('unit_price must be >= 0 for all rows')
    return errors

def validate_customers_data(customers_df):
    errors = []
    expected_columns = ['customer_id','customer_name','email']
    missing = set(expected_columns) - set(customers_df.columns)
    if missing:
        errors.append(f'Missing columns in customers: {sorted(list(missing))}')
    if 'customer_id' in customers_df.columns and customers_df['customer_id'].isnull().any():
        errors.append('Null values found in customer_id')
    if 'customer_id' in customers_df.columns and customers_df['customer_id'].duplicated().any():
        errors.append('Duplicate customer_id values found')
    return errors

def run_data_quality_checks(orders_file_path, customers_file_path):
    try:
        orders = pd.read_csv(orders_file_path)
        customers = pd.read_csv(customers_file_path)
    except Exception as e:
        print(f'Error reading files: {e}')
        sys.exit(1)
    errors = []
    errors.extend(validate_orders_data(orders))
    errors.extend(validate_customers_data(customers))
    if errors:
        print('DATA QUALITY ERRORS:')
        for e in errors:
            print('-', e)
        sys.exit(1)
    print('All data quality checks passed.')
    return True

if __name__ == '__main__':
    from datetime import datetime, timedelta
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    orders_file = f'data/input/orders_{yesterday}.csv'
    customers_file = 'data/input/customers.csv'
    run_data_quality_checks(orders_file, customers_file)
