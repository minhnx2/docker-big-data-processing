from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG

from airflow.operators.bash import BashOperator

with DAG(
	'pipeline_1',
	default_args={
		'depends_on_past': False,
		'email': ['asd@admin.com'],
		'email_on_failure': False,
		'email_on_retry': False,
		'retries': 1,
		'retry_delay': timedelta(minutes=5),
		# 'queue': 'bash_queue',
		# 'pool': 'backfill',
		# 'priority_weight': 10,
		# 'end_date': datetime(2022, 7, 30),
		# 'wait_for_downstream': False,
		# 'sla': timedelta(hours=2),
		# 'execution_timeout': timedelta(seconds=300),
		# 'on_failure_callback': some_function,
		# 'on_success_callback': some_function,
		# 'on_retry_callback': some_function,
		# 'sla_miss_callback': some_function,
		# 'trigger_rule': 'all_success'
	},
	description='Simple pipeline 1',
	schedule_interval=timedelta(days=1),
	start_date=datetime(2022, 7, 1),
	catchup=False,
	tags=['example'],
) as dag:
	t1 = BashOperator(
		task_id='print_date',
		bash_command='date'
	)

	t2 = BashOperator(
		task_id='sleep',
		depends_on_past=False,
		bash_command='sleep 5',
		retries=3
	)

	t1.doc_md = dedent(
		"""\
	# Task documentation
		"""
	)

	dag.doc_md = __doc__
	dag.doc_md = """
	Dag document
	"""

	templated_command = dedent(
		"""
		{% for i in range(5) %}
			echo "{{ ds }}"
			echo "{{ macros.ds_add(ds, 7)}}"
		{% endfor %}
		"""
	)

	t3 = BashOperator(
		task_id='templated',
		depends_on_past=False,
		bash_command=templated_command
	)

	t1 >> [t2, t3]
