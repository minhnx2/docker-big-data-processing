import datetime
import pendulum
import os
import requests

from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

@dag(
	schedule_interval="0 0 * * *",
	start_date=pendulum.datetime(2022, 1, 1, tz='UTC'),
	catchup=False,
	dagrun_timeout=datetime.timedelta(minutes=60)
)

def etl():

	create_employees_schema = PostgresOperator(
		task_id='create_employees_schema',
		postgres_conn_id='pg',
		sql='pipeline_2_sql/employee_schema.sql'
	)

	@task
	def get_data():
		data_path = '/opt/airflow/dags/pipeline_2_data/employees.csv'
		os.makedirs(os.path.dirname(data_path), exist_ok=True)

		url = 'https://raw.githubusercontent.com/apache/airflow/main/docs/apache-airflow/pipeline_example.csv'

		response = requests.request('GET', url)

		with open(data_path, 'w') as file:
			file.write(response.text)

		postgres_hook = PostgresHook(postgres_conn_id='pg')
		conn = postgres_hook.get_conn()
		cur = conn.cursor()
		with open(data_path, 'r') as file:
			cur.copy_expert(
				"COPY employees_temp FROM STDIN WITH CSV HEADER DELIMITER AS ',' QUOTE '\"'",
				file
			)
		conn.commit()

	@task
	def merge_data():
		query = """
			insert into epmployees
			select * from (select distinct * from employees_temp)
			on conflict ("id") do update
			set "id" = excluded."id"; 
		"""
		try:
			postgres_hook = PostgresHook(postgres_conn_id='pg')
			conn = postgres_hook.get_conn()
			cur = conn.cursor()
			cur.execute(query)
			conn.commit()
			return 0
		except Exception as e:
			return 1

	create_employees_schema >> get_data() >> merge_data()

dag = etl()
