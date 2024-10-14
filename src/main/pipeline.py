"""
Module: extract_and_load.py
Description: 
    This module extracts the iris dataset from sklearn.
    Train model and loads prediction into a MySQL database.
"""

import os
import sys

from loguru import logger
import pandas as pd

from config.database import ENGINE_MYSQL
from config.variables import S3_BUCKET_NAME
from src.lib.data import load_iris_data, split_data, generate_data
from src.lib.models import train_model, evaluate_model, predict
from src.lib.database import create_predictions_table, insert_predictions
from src.lib.object_storage import download_file_from_s3


def main() -> None:
    """
    Main function to orchestrate the data extraction, model training, and prediction loading process.

    Returns
    -------
    None
    """

    logger.info("Starting pipeline process...")

    # EXTRACT
    logger.info("Loading iris dataset...")
    # df = load_iris_data()
    object_name = "iris.parquet"
    file_path = os.path.join("data", "output", object_name)
    download_file_from_s3(
        bucket_name=S3_BUCKET_NAME,
        object_name=object_name,
        file_path=file_path
    )
    df = pd.read_parquet(file_path)
    logger.info("Iris dataset loaded successfully")
    
    logger.info("Generating synthetic data...")
    df_generated = generate_data(n_samples=200)
    logger.info("Synthetic data generated successfully")

    # TRANSFORM
    logger.info("Splitting data into training and test sets...")
    x_train, x_test, y_train, y_test = split_data(df)
    logger.info("Data split successfully")

    logger.info("Training model...")
    model = train_model(x_train, y_train)
    logger.info("Model trained successfully")

    logger.info("Evaluating model...")
    metric = evaluate_model(model, x_test, y_test)
    logger.info(f"Model metric on test data: {metric:.2f}")

    logger.info("Making predictions...")
    predictions_df = predict(model, df_generated)
    logger.info("Predictions made successfully")

    # LOAD
    logger.info("Creating predictions table...")
    create_predictions_table(ENGINE_MYSQL)
    logger.info("Predictions table created successfully")

    logger.info("Inserting predictions into database...")
    insert_predictions(predictions_df, ENGINE_MYSQL)
    logger.info("Predictions inserted successfully")

    logger.info("Pipeline process completed successfully")


if __name__ == "__main__":
    main()
