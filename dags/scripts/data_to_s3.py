import boto3 
import os
from dotenv import load_dotenv
import botocore 

# For aws config. 
load_dotenv()

def ensure_bucket(bucket_name: str):
    
    s3_client = boto3.client('s3')
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError:
        # Bucket does not exist, create it
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'us-east-2'}  # change region if needed
        )

def upload_to_s3(bucket: str, key:str, file_path:str):
    """Uploads data to S3 depending on data type

    Args:
        content_type (str): enum[image, text]
    """
    
    s3_client = boto3.client('s3')
    
    ensure_bucket(bucket)
    
    file_path = str(file_path)  # ensure string

    s3_client.upload_file(
                         Filename=file_path,
                         Bucket=bucket, 
                         Key=key
                        )

    




