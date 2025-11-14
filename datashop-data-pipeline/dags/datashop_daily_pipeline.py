from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from transform import generate_daily_report
from data_quality_check import run_data_quality_checks

default_args = {
    'owner': 'datashop',
    'depends_on_past': False,
    'start_date': datetime(2024,1,1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def get_yesterday():
    return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

def verify_source_files(**kwargs):
    yesterday = get_yesterday()
    orders_file = f"data/input/orders_{yesterday}.csv"
    customers_file = "data/input/customers.csv"
    if not os.path.exists(orders_file):
        raise FileNotFoundError(orders_file)
    if not os.path.exists(customers_file):
        raise FileNotFoundError(customers_file)
    print('Source files verified.')

def execute_dq(**kwargs):
    yesterday = get_yesterday()
    orders_file = f"data/input/orders_{yesterday}.csv"
    customers_file = "data/input/customers.csv"
    run_data_quality_checks(orders_file, customers_file)

def transform(**kwargs):
    yesterday = get_yesterday()
    orders_file = f"data/input/orders_{yesterday}.csv"
    customers_file = "data/input/customers.csv"
    output_file = f"data/output/daily_report_{yesterday}.json"
    generate_daily_report(orders_file, customers_file, output_file)

with DAG(
    dag_id='datashop_daily_pipeline',
    default_args=default_args,
    schedule_interval='0 2 * * *',
    catchup=False,
    tags=['datashop']
) as dag:
    start = EmptyOperator(task_id='start')
    verify = PythonOperator(task_id='Verificar_Datos_Fuente', python_callable=verify_source_files)
    dq = PythonOperator(task_id='Ejecutar_Control_Calidad', python_callable=execute_dq)
    trans = PythonOperator(task_id='Transformar_Datos', python_callable=transform)
    load = PythonOperator(task_id='Cargar_Resultado', python_callable=lambda: print('Simulated load'))
    end = EmptyOperator(task_id='end')

    start >> verify >> dq >> trans >> load >> end
