import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

dag = DAG('ku_scraping_workflow',
          description='Scraping Event from Stadt Kufstein website',
          schedule_interval='0 22 15 * *',
          start_date=datetime.datetime(2019, 1, 1),
          catchup=False)

prepare_environment = BashOperator(
    task_id='prepare_environment',
    bash_command='pip3 install sqlalchemy && pip3 install beautifulsoup4',
    dag=dag,
)

prepare_db_task = BashOperator(
    task_id='prepare_db_task',
    bash_command='(cd /mnt/c/swe/hausaufgabe_3/event_scraper && python3 declarations.py)',
    dag=dag,
)

scraping_task = BashOperator(
    task_id='scraping_task',
    bash_command='(cd /mnt/c/swe/hausaufgabe_3/event_scraper && python3 main_ku.py)',
    dag=dag,
)

prepare_environment >> prepare_db_task >> scraping_task

