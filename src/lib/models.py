"""
Module: models.py
Description:
    This module contains functions to train and evaluate a logistic regression model.
"""

from typing import Callable

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def train_model(x_train: pd.DataFrame, y_train: pd.Series) -> LogisticRegression:
    """
    Train a logistic regression model on the iris dataset.

    Parameters
    ----------
    X_train : pd.DataFrame
        The features of the training data.
    y_train : pd.Series
        The labels of the training data.

    Returns
    -------
    LogisticRegression
        The trained logistic regression model.
    """
    model = LogisticRegression(max_iter=200)
    model.fit(x_train, y_train)
    return model


def evaluate_model(
    model: LogisticRegression,
    x_test: pd.DataFrame,
    y_test: pd.Series,
    metric: Callable = accuracy_score,
) -> None:
    """
    Evaluate the trained model on the test data and log accuracy.

    Parameters
    ----------
    model : LogisticRegression
        The trained model.
    X_test : pd.DataFrame
        The features of the test data.
    y_test : pd.Series
        The labels of the test data.

    Returns
    -------
    None
    """
    y_pred = model.predict(x_test)
    accuracy = metric(y_test, y_pred)

    return accuracy


def predict(model: LogisticRegression, x_test: pd.DataFrame) -> pd.DataFrame:
    """
    Make predictions using the trained model on the test set.

    Parameters
    ----------
    model : LogisticRegression
        The trained model.
    X_test : pd.DataFrame
        The features of the test data.

    Returns
    -------
    pd.DataFrame
        DataFrame containing test features and predicted values.
    """
    predictions = model.predict(x_test)
    x_test = x_test.copy()  # Avoid modifying the original X_test
    x_test["predicted_target"] = predictions
    return x_test
