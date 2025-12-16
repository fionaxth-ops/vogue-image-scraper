from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # points to airflow/dags
SCRIPT_PATH = os.path.join(BASE_DIR, "scripts", "vogue_image_scraper.py")


with DAG(
    dag_id="vogue_ai_data_etl",
    start_date=datetime(year=2025, month=12, day=9, hour=9, minute=0),
    schedule="@daily",
    catchup=True,
    max_active_runs=1,
    render_template_as_native_obj=True
) as dag:

        run_script_task = BashOperator(
            task_id='scrape_images',
            bash_command='python3 /opt/airflow/dags/scripts/vogue_image_scraper.py'
        )   
# from airflow import DAG
# from datetime import datetime
# from airflow.operators.bash import BashOperator
# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # points to airflow/dags
# SCRIPT_PATH = os.path.join(BASE_DIR, "scripts", "vogue_image_scraper.py")


# with DAG(
#     dag_id="vogue_ai_data_etl",
#     start_date=datetime(year=2025, month=12, day=9, hour=9, minute=0),
#     schedule="@daily",
#     catchup=True,
#     max_active_runs=1,
#     render_template_as_native_obj=True
# ) as dag:

#         run_script_task = BashOperator(
#             task_id='scrape_images',
#             bash_command='python3 /usr/local/airflow/dags/scripts/vogue_image_scraper.py',
#         )   