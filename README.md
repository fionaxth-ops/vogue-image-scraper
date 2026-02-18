## **Overview**
Scrapes images from Vogue Runway shows, analyses the images with AI and extracts trends and uploads the images and data to S3. This pipeline is automated and triggered through Airflow. 

## **Key Features**
- Scheduled execution.
- AI trend analysis through Gemini.
- Automated image scraping from Vogue. 
- Organised data storage.

## **Installation**
1. Clone the repo.
2. Install requirements.
   * Create a virtualenv and install dependencies. 
   ```zsh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Set environment variables (.env).
   * Create an evironment variable file in project root. 
    ``` .env
    VOGUE_EMAIL=you@example.com
    VOGUE_PASSWORD=your_password
    GEMINI_API_KEY=your_gemini_api_key
    AWS_ACCESS_KEY_ID=AKIA...
    AWS_SECRET_ACCESS_KEY=secret
    AWS_DEFAULT_REGION=us-east-2
    VOGUE_BASE_DIR=/path/to/base
    ```
6. Configure Airflow.
   * Run via [Airflow](https://airflow.apache.org/docs/apache-airflow/stable/start.html) (recommended)
   * Place the repo under your Airflow dags_folder or ensure DAG is discoverable.
   * Trigger the DAG from the Airflow UI and set slideshow_url in the DAG run form, or trigger via CLI:
   ```zsh
   airflow dags trigger vogue_ai_data_etl --conf '{"slideshow_url":"https://www.vogue.com/.../slideshow/collection#1"}'
   ```



