"""
Module: object_storage.py
Description:
    This module contains helper functions to upload 
    and download files from an S3-compatible bucket in Yandex Cloud.
"""
from typing import Optional
import os
import boto3
from botocore.exceptions import ClientError
from loguru import logger

from config.object_storage import S3_RESOURCE

def upload_file_to_s3(
    file_path: str, 
    bucket_name: str, 
    object_name: Optional[str] = None,
    s3_resource: Optional[boto3.resource] = S3_RESOURCE
) -> bool:
    """
    Upload a file to an S3-compatible bucket in Yandex Cloud.

    Parameters
    ----------
    file_path : str
        Path to the file to upload
    bucket_name : str
        Name of the bucket to upload to
    object_name : str, optional
        S3 object name. If not specified, the filename from file_path is used
    s3_resource : boto3.resource, optional
        Boto3 S3 resource. If not provided, it should be configured globally

    Returns
    -------
    bool
        True if file was uploaded successfully, else False
    """
    access_key = os.getenv("S3_ACCESS_KEY")
    secret_key = os.getenv("S3_SECRET_KEY")
    endpoint_url = os.getenv("S3_ENDPOINT_URL", "https://storage.yandexcloud.net")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint_url
    )

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"Файл {file_path} успешно загружен как {object_name}")
    except ClientError as e:
        print(f"Ошибка загрузки: {e}")

        

def download_file_from_s3(
    bucket_name: str,
    object_name: str,
    file_path: str,
    s3_resource: Optional[boto3.resource] = S3_RESOURCE
) -> bool:
    """
    Download a file from an S3-compatible bucket in Yandex Cloud.

    Parameters
    ----------
    bucket_name : str
        Name of the bucket to download from
    object_name : str
        S3 object name to download
    file_path : str
        Local path to save the downloaded file
    s3_resource : boto3.resource, optional
        Boto3 S3 resource. If not provided, it should be configured globally

    Returns
    -------
    bool
        True if file was downloaded successfully, else False
    """
    # Используем переменные окружения из .env
    access_key = os.getenv("S3_ACCESS_KEY")
    secret_key = os.getenv("S3_SECRET_KEY")
    endpoint_url = os.getenv("S3_ENDPOINT_URL", "https://storage.yandexcloud.net")

    # Создаем клиент S3 с явным указанием endpoint_url
    s3_resource = boto3.resource(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint_url
    )

    try:
        s3_resource.Bucket(bucket_name).download_file(object_name, file_path)
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print("Файл не найден в бакете")
        else:
            raise