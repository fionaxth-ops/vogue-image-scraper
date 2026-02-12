from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from selenium.webdriver.support.ui import WebDriverWait
import os
from pathlib import Path
import sys
from urllib.parse import urlparse
from airflow.models import Variable

# Add scripts directory to path BEFORE importing from it
sys.path.insert(0, str(Path(__file__).parent / "scripts"))
from vogue_image_scraper import login_to_vogue, scrape_slideshow, create_driver
from ai_analysis import image_analysis 
from data_to_s3 import upload_to_s3

SLIDESHOW_URL = "https://www.vogue.com/fashion-shows/spring-2026-ready-to-wear/christophe-lemaire/slideshow/collection#1"
BASE_PATH = Path(os.getenv("VOGUE_BASE_DIR", "/tmp/vogue"))
IMAGES_PATH = BASE_PATH / "Projects/vogue_data_pipeline/images"
TEMP_FILE_PATH = BASE_PATH / "Projects/vogue_data_pipeline/data/temp.jsonl"
WAIT_TIME = 20
BUCKET_NAME = "vogue-runway-data"


def process_folder_structure(url:Path)-> dict: 
    """Creates the folder structure for the images based off the information in the URL

    Args:
        url (Path): URL of the slideshow to be scraped

    Returns:
        dict: 
            season (string): Season of the runway show
            designer (string): Designer of the show
            source (string): Host of the image
    """    
    path_parts = urlparse(url).path.strip("/").split("/")
    return {
        "season": path_parts[1],
        "designer": path_parts[2], 
        "source": "vogue" 
    }

def scrape_task(url: Path):
    driver = create_driver()
    wait = WebDriverWait(driver, WAIT_TIME)
    # Moved imports inside the function as Airflow constantly parses the DAG file
    # causing the chrome driver to be initialised 
    login_to_vogue(driver, wait, os.getenv("VOGUE_EMAIL"), os.getenv("VOGUE_PASSWORD"))
    scrape_slideshow(driver, wait, url)

def generate_trend_data(images_path, temp_file_path): 
    image_analysis(images_path, temp_file_path)
    
def load_to_s3(url:Path, bucket:str): 

    folder_dict = process_folder_structure(url)
    base_key = f"{folder_dict['season']}/{folder_dict['designer']}"

    print(str(IMAGES_PATH))
    print(str(TEMP_FILE_PATH))

    for image_file in IMAGES_PATH.iterdir(): 
        if image_file.is_file():
            upload_to_s3(
                bucket=bucket,
                key=f"{base_key}/images/{image_file.name}",
                file_path=str(image_file), 
                ) 
    
    upload_to_s3(
        bucket=bucket,
        key=f"{base_key}/analysis/trends.jsonl",
        file_path=str(TEMP_FILE_PATH)
        )


with DAG(
    dag_id="vogue_ai_data_etl",
    start_date=datetime(year=2025, month=12, day=9, hour=9, minute=0),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    render_template_as_native_obj=True
) as dag:

    extract = PythonOperator(
        
        task_id="scrape_vogue_slideshow",
        python_callable=scrape_task,
        op_args=[SLIDESHOW_URL]
    )
    transform = PythonOperator(
        task_id="get_analysis",
        python_callable=generate_trend_data,
        op_args=[IMAGES_PATH, TEMP_FILE_PATH]
    )
    load = PythonOperator(
        
        task_id = "load_data",
        python_callable=load_to_s3, 
        op_args=[SLIDESHOW_URL, BUCKET_NAME]
    )
    
    extract >> transform >> load