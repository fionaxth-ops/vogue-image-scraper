import boto3 
import logging
import os
import time 
from dotenv import load_dotenv

load_dotenv()

def upload_to_s3(bucket:str, key:str, content_type: str):
    """Uploads data to S3 depending on data type

    Args:
        content_type (str): enum[image, text]
    """
    
    s3_client = boto3.client('s3',
                            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'), 
                            aws_secret_access_key=os.getenv('AWS_SECRET')
                            )

    s3_client.put_object(Bucket=bucket, Key=key, ContentType=content_type)






