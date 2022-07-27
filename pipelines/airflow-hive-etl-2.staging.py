from __future__ import print_function
import airflow
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import Variable

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(5),
    'provide_context': True
}

# tmpl_search_path = Variable.get("sql_path")
tmpl_search_path = "/opt/airflow/dags/airflow-hive-etl-2_sql"

dag = airflow.DAG(
    'staging_oltp',
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=60),
    template_searchpath=tmpl_search_path,
    default_args=args,
    max_active_runs=1)

# stage_customer = PostgresToHiveOperator(
#     sql='select_customer.sql',
#     hive_table='customer_staging',
#     postgres_conn_id='postgres_oltp',
#     hive_cli_conn_id='hive_staging',
#     partition={"change_date": "{{ ds }}"},
#     parameters={"window_start_date": "{{ ds }}", "window_end_date": "{{ tomorrow_ds }}"},
#     task_id='stage_customer',
#     dag=dag)

# stage_orderinfo = PostgresToHiveOperator(
#     sql='select_order_info.sql',
#     hive_table='order_info_staging',
#     postgres_conn_id='postgres_oltp',
#     hive_cli_conn_id='hive_staging',
#     partition={"change_date": "{{ ds }}"},
#     parameters={"window_start_date": "{{ ds }}", "window_end_date": "{{ tomorrow_ds }}"},
#     task_id='stage_orderinfo',
#     dag=dag)

# stage_orderline = PostgresToHiveOperator(
#     sql='select_orderline.sql',
#     hive_table='orderline_staging',
#     postgres_conn_id='postgres_oltp',
#     hive_cli_conn_id='hive_staging',
#     partition={"change_date": "{{ ds }}"},
#     parameters={"window_start_date": "{{ ds }}", "window_end_date": "{{ tomorrow_ds }}"},
#     task_id='stage_orderline',
#     dag=dag)

# stage_product = PostgresToHiveOperator(
#     sql='select_product.sql',
#     hive_table='product_staging',
#     postgres_conn_id='postgres_oltp',
#     hive_cli_conn_id='hive_staging',
#     partition={"change_date": "{{ ds }}"},
#     parameters={"window_start_date": "{{ ds }}", "window_end_date": "{{ tomorrow_ds }}"},
#     task_id='stage_product',
#     dag=dag)

dummy = DummyOperator(
    task_id='dummy',
    dag=dag)

# stage_customer >> dummy
# stage_orderinfo >> dummy
# stage_orderline >> dummy
# stage_product >> dummy

if __name__ == "__main__":
    dag.cli()
