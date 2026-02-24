import boto3
import logging
from botocore.exceptions import ClientError
#from src.session import SessionClient
#session_client = SessionClient()

def upload_file(bucket_name, file_name):
    s3 = boto3.client("s3")

    try:
        #SessionClient.session_client = session_client.get_session_client("257676781382", "us-east-2")
        #s3_client = SessionClient.session_client.client(service_name='s3', region_name="us-east-2")
        s3.upload_file(file_name, bucket_name, file_name)
        logging.info(f"Uploaded {file_name} to {bucket_name}")
    except ClientError as e:
        logging.error(f"S3 Upload failed: {e}")
        raise


def download_file(bucket_name, file_name, download_name):
    s3 = boto3.client("s3")

    try:
        #SessionClient.session_client = session_client.get_session_client("257676781382", "us-east-2")
        #s3_client = SessionClient.session_client.client(service_name='s3', region_name="us-east-2")
        s3.download_file(bucket_name, file_name, download_name)
        logging.info(f"Downloaded {file_name} from {bucket_name}")
    except ClientError as e:
        logging.error(f"S3 Download failed: {e}")
        raise
