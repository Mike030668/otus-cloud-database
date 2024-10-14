"""
Module: database.py
Description:
    This module contains functions to create and insert data into a MySQL database.
"""

from typing import Optional, Tuple

import pandas as pd
from loguru import logger
from sqlalchemy.engine.base import Engine


def execute(query: str, params: Optional[Tuple] = None, con: Engine = None) -> None:
    """
    Execute a SQL query with optional parameters.

    Parameters
    ----------
    query : str
        The SQL query to execute.
    params : tuple, optional
        The parameters for the SQL query.
    con : sqlalchemy.engine.base.Engine
        The database connection engine.

    Returns
    -------
    None
    """
    with con.connect() as connection:
        with connection.begin():
            if params:
                connection.execute(query, params)
            else:
                connection.execute(query)


def create_predictions_table(con: Engine) -> None:
    """
    Create the iris_predictions table if it doesn't exist.

    Parameters
    ----------
    con : sqlalchemy.engine.base.Engine
        The database connection engine.

    Returns
    -------
    None
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS iris_predictions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        sepal_length FLOAT,
        sepal_width FLOAT,
        petal_length FLOAT,
        petal_width FLOAT,
        predicted_target INT
    )
    """
    execute(create_table_query, con=con)
    logger.info("Table 'iris_predictions' created or already exists.")


def insert_predictions(df: pd.DataFrame, con: Engine, batch_size: int = 1000) -> None:
    """
    Insert the predicted data into the iris_predictions table using batch insert.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the test features and predicted values.
    con : sqlalchemy.engine.base.Engine
        The database connection engine.
    batch_size : int, optional
        The number of records to insert in each batch (default is 1000).

    Returns
    -------
    None
    """
    insert_query = """
    INSERT INTO iris_predictions (
        sepal_length, 
        sepal_width, 
        petal_length, 
        petal_width, 
        predicted_target
    )
    VALUES (%s, %s, %s, %s, %s)
    """

    total_rows = df.shape[0]

    try:
        for i in range(0, total_rows, batch_size):
            batch = df.iloc[i : i + batch_size]
            values = [
                (
                    row["sepal_length"],
                    row["sepal_width"],
                    row["petal_length"],
                    row["petal_width"],
                    row["predicted_target"],
                )
                for _, row in batch.iterrows()
            ]
            execute(insert_query, values, con)
            logger.info(
                f"Inserted records {i+1} to {min(i+batch_size, total_rows)} / {total_rows}"
            )

        logger.info(
            f"Successfully inserted {total_rows} predicted records into the database."
        )
    except Exception as e:  # pylint: disable=broad-except
        logger.error(f"An error occurred while inserting predictions: {e}")
    finally:
        logger.info("Prediction insertion completed.")
