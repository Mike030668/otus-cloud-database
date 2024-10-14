"""
Module: object_storage.py
Description:
    This module contains helper functions to upload 
    and download files from an S3-compatible bucket in Yandex Cloud.
"""
from typing import Optional

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
    if object_name is None:
        object_name = file_path.split('/')[-1]

    try:
        s3_resource.Bucket(bucket_name).upload_file(file_path, object_name)
        logger.info(f"Successfully uploaded {file_path} to {bucket_name}/{object_name}")
        return True
    except ClientError as e:
        logger.error(f"Error uploading file to S3: {e}")
        return False

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
    try:
        s3_resource.Bucket(bucket_name).download_file(object_name, file_path)
        logger.info(f"Successfully downloaded {bucket_name}/{object_name} to {file_path}")
        return True
    except ClientError as e:
        logger.error(f"Error downloading file from S3: {e}")
        return False
