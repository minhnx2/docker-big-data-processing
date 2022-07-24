import json
import pendulum

from textwrap import dedent
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG(
	'pipeline_3',
	default_args={ 'retries': 2 },
	description='pipeline 3',
	schedule_interval=None,
	start_date=pendulum.datetime(2022, 1, 1, tz='UTC'),
	catchup=False,
	tags=['example']
) as dag:
	dag.doc_md = __doc__

	def extract(**kwargs):
		ti = kwargs['ti']
		data_string='{"1": 200, "2": 150, "3": 30}'
		ti.xcom_push('order_data', data_string)

	def transform(**kwargs):
		ti = kwargs['ti']
		extract_data_string = ti.xcom_pull(task_ids='extract', key='order_data')
		order_data = json.loads(extract_data_string)

		total_amount = 0
		for value in order_data.values():
			total_amount += value

		total_value = {'total_value': total_amount}
		total_value_json = json.dumps(total_value)
		ti.xcom_push('total_order_value', total_value_json)

	def load(**kwargs):
		ti = kwargs['ti']
		total_value_string = ti.xcom_pull(task_ids='transform', key='total_order_value')
		total_value = json.loads(total_value_string)

		print(total_value)

	extract_task = PythonOperator(
		task_id='extract',
		python_callable=extract
	)
	extract_task.doc_md = dedent(
	"""
	# Extract task doc
	"""
	)

	transform_task = PythonOperator(
		task_id='transform',
		python_callable=transform
	)
	transform_task.doc_md = dedent(
	"""
	# Transform task doc
	"""
	)

	load_task = PythonOperator(
		task_id='load',
		python_callable=load
	)
	load_task.doc_md = dedent(
	"""
	Load task doc
	"""
	)

	extract_task >> transform_task >> load_task