"""
Script: upload_data_to_s3.py
Description:
    This script extracts the iris dataset from sklearn and uploads it to an S3 bucket.
"""

import os

from loguru import logger

from config.variables import S3_BUCKET_NAME

from src.lib.data import load_iris_data
from src.lib.object_storage import upload_file_to_s3



def main() -> None:
    """
    Main function to orchestrate the data extraction, model training, and prediction loading process.

    Returns
    -------
    None
    """
    script_name = os.path.basename(__file__)

    logger.info(f"Starting {script_name}...")

    # EXTRACT
    logger.info("Loading iris dataset...")
    df = load_iris_data()
    logger.info("Iris dataset loaded successfully")

    # SAVE
    logger.info("Saving iris dataset to parquet...")
    file_path = os.path.join("data", "iris.parquet")
    df.to_parquet(file_path, index=False)
    logger.info(f"Iris dataset saved to {file_path}")

    # LOAD
    logger.info("Uploading iris dataset to S3...")
    upload_file_to_s3(
        file_path=file_path,
        bucket_name=S3_BUCKET_NAME,
        object_name="iris.parquet"
    )
    logger.info("Iris dataset uploaded successfully")

    logger.info(f"Finished {script_name}")


if __name__ == "__main__":
    main()
