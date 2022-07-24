from airflow.decorators import task, dag
from datetime import datetime

#@task.docker(image='python:3.9-slim-bullseye', multiple_outputs=False)
# @task.virtualenv(
#     use_dill=True,
#     system_site_packages=False,
#     requirements=['funcsigs'],
# )
@task
def add_task(x, y):
	print(f'args: x = {x}, y = {y}')
	return x + y;

@dag(start_date=datetime(2022, 1, 1))
def dag1():
	start = add_task.override(task_id='start')(1, 2)
	for i in range(3):
		start >> add_task.override(task_id=f'add_start{i}')(start, i)

@dag(start_date=datetime(2022, 1, 1))
def dag2():
	start = add_task(1, 2)
	for i in range(3):
		start >> add_task.override(task_id=f'new_add_{i}')(start, i)

pipeline_4_dag_1 = dag1()
pipeline_4_dag_2 = dag2()