import boto3 
import logging
import os
import time 
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client('s3',
                         aws_access_key_id=os.getenv('AWS_ACCESS_KEY'), 
                         aws_secret_access_key=os.getenv('AWS_SECRET')
                         )

bucket_name = 'vogue-runway-data'
file_name = 'data/temp.jsonl'
# I need to pull this through airflow 
current_epoch_time = int(time.time())
file_path = f'lemaire/2026/{current_epoch_time}.jsonl'

# Upload data to S3 bucket with brand, year, season to partition
# I need to get the brand, year and season from the airflow job 
s3_client.upload_file(file_name, bucket_name, file_path)






