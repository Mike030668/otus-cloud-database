"""
Module: config/object_storage.py
Description:
    This module contains the configuration for the S3 resource.
"""

from boto3 import resource

from config.variables import S3_ACCESS_KEY, S3_ENDPOINT_URL, S3_SECRET_KEY

S3_RESOURCE = resource(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
)
