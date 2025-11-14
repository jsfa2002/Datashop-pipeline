import pandas as pd
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from transform import calculate_daily_metrics

def sample_orders_df():
    return pd.DataFrame({
        'order_id': [1,2,3],
        'customer_id': [101,102,101],
        'product_id': [1,2,1],
        'quantity': [2,1,3],
        'unit_price': [10.0,20.0,10.0],
        'order_date': ['2024-01-01']*3
    })

def sample_customers_df():
    return pd.DataFrame({
        'customer_id': [101,102],
        'customer_name': ['Alice','Bob'],
        'email': ['alice@example.com','bob@example.com']
    })

def test_total_sales():
    orders = sample_orders_df()
    customers = sample_customers_df()
    rpt = calculate_daily_metrics(orders, customers)
    assert rpt['total_sales'] == 70.0

def test_top_product():
    orders = sample_orders_df()
    customers = sample_customers_df()
    rpt = calculate_daily_metrics(orders, customers)
    top = rpt['top_5_products'][0]
    assert top['product_id'] == 1
    assert top['quantity'] == 5

def test_customer_largest_purchase():
    orders = sample_orders_df()
    customers = sample_customers_df()
    rpt = calculate_daily_metrics(orders, customers)
    cl = rpt['customer_largest_purchase']
    assert cl['customer_name'] == 'Alice'
    assert cl['total_amount'] == 30.0

def test_handle_empty():
    orders = pd.DataFrame(columns=['order_id','customer_id','product_id','quantity','unit_price','order_date'])
    customers = pd.DataFrame(columns=['customer_id','customer_name','email'])
    rpt = calculate_daily_metrics(orders, customers)
    assert rpt['total_sales'] == 0.0
    assert rpt['top_5_products'] == []
