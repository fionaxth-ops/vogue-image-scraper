from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import os
from pathlib import Path
import sys
from vogue_image_scraper import login_to_vogue, scrape_slideshow
from urllib.parse import urlparse


sys.path.append(str(Path(__file__).parent / "scripts"))

SLIDESHOW_URL = "https://www.vogue.com/fashion-shows/spring-2026-ready-to-wear/christophe-lemaire/slideshow/collection#1"

def process_folder_structure(url)-> dict: 
    path_parts = urlparse(url).path.strip("/").split("/")
    return {
        "season": path_parts[1],
        "designer": path_parts[2], 
        "source": "vogue" 
    }

def scrape_task(url):
    login_to_vogue(os.getenv("VOGUE_EMAIL"), os.getenv("VOGUE_PASSWORD"))
    scrape_slideshow(url)


with DAG(
    dag_id="vogue_ai_data_etl",
    start_date=datetime(year=2025, month=12, day=9, hour=9, minute=0),
    schedule="@daily",
    catchup=True,
    max_active_runs=1,
    render_template_as_native_obj=True
) as dag:

    extract = PythonOperator(
        task_id="scrape_vogue_slideshow",
        python_callable=scrape_task,
    )
    transform = PythonOperator(
        task_id="get_metadata",

        
    )
