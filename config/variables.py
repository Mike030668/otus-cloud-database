"""
Module: variables.py
Description:
    This module contains the environment variables.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# Load environment variables
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')
SSL_PATH = os.getenv('SSL_PATH')

S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')
S3_ACCESS_KEY = os.getenv('S3_ACCESS')
S3_SECRET_KEY = os.getenv('S3_SECRET')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
