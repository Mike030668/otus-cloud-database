"""
Module: database.py
Description:
    This module contains the database configuration settings.
"""

from sqlalchemy import create_engine

from config.variables import DB_USER, DB_PASS, DB_HOST, DB_NAME, DB_PORT, SSL_PATH


# Database connection URL
SSL_ARGS = {"ssl_ca": SSL_PATH}
CONNECTION_URL_MYSQL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ENGINE_MYSQL = create_engine(CONNECTION_URL_MYSQL, connect_args=SSL_ARGS)
