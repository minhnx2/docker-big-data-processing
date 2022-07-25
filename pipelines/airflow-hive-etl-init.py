from __future__ import print_function
import airflow
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow import models
from airflow.settings import Session
import logging
import json

args = {
	'owner': 'airflow',
	'start_date': airflow.utils.dates.days_ago(5),
	'provide_context': True
}

def init_hive():
	logging.info('creating connections, pool and sql path')

	session = Session()

	def create_new_conn(session, attrs):
		new_conn = models.Connection()
		new_conn.conn_id = attrs.get('conn_id')
		new_conn.conn_type = attrs.get('conn_type')
		new_conn.host = attrs.get('host')
		new_conn.port = attrs.get('port')
		new_conn.schema = attrs.get('schema')
		new_conn.login = attrs.get('login')
		new_conn.set_extra(attrs.get('extra'))
		new_conn.set_password(attrs.get('password'))

		session.add(new_conn)
		session.commit()

	create_new_conn(session, {
		'conn_id': 'postgres_oltp',
		'conn_type': 'postgres',
		'host': 'postgres',
		'port': 5432,
		'schema': 'orders',
		'login': 'oltp_read',
		'password': 'oltp_read',
	})

	create_new_conn(session, {
		'conn_id': 'hive_staging',
		'conn_type': 'hive_cli',
		'host': 'host.docker.internal',
		'port': 10000,
		'login': 'admin',
		'password': '',
		'extra': json.dumps({
			'hive_cli_params': '',
			'auth': 'none',
			'use_beeline': 'true'
		}),
	})

	new_var = models.Variable()
	new_var.key = 'sql_path'
	new_var.set_val('/usr/local/airflow/sql')

	session.add(new_var)

	new_var = models.Variable()
	new_var.key = 'hive_sql_path'
	new_var.set_val('/usr/local/airflow/hql')

	session.add(new_var)
	session.commit()
	session.close()

dag = airflow.DAG(
	'airflow-hive-etl-init',
	schedule_interval='@once',
	default_args=args,
	max_active_runs=1
)

t1 = PythonOperator(
	task_id='init_hive',
	python_callable=init_hive,	
	dag=dag
)
