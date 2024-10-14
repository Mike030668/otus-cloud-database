"""
Module: data.py
Description:
    This module contains functions to load, split, and generate data.
"""

from typing import Tuple

import pandas as pd
import numpy as np
from sklearn.datasets import load_iris, make_classification
from sklearn.model_selection import train_test_split


def load_iris_data() -> pd.DataFrame:
    """
    Load the iris dataset from sklearn and convert it to a pandas DataFrame.

    Returns
    -------
    pd.DataFrame
        The iris dataset as a pandas DataFrame.
    """
    iris = load_iris()
    df = pd.DataFrame(
        data=iris["data"],
        columns=["sepal_length", "sepal_width", "petal_length", "petal_width"],
    )
    df["target"] = iris["target"]
    return df


def split_data(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split the iris dataset into training and test sets.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the iris dataset.

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]
        The training features, test features, training labels, and test labels.
    """
    features = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
    target = df["target"]
    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=0.3, random_state=42
    )
    return x_train, x_test, y_train, y_test


def generate_data(n_samples: int = 150) -> pd.DataFrame:
    """
    Generate synthetic data similar to the iris dataset using make_classification,
    ensuring all values are positive.

    Parameters
    ----------
    n_samples : int, optional
        The number of samples to generate, by default 150

    Returns
    -------
    pd.DataFrame
        A DataFrame containing generated features with positive values.
    """
    # Generate base data
    features, _ = make_classification(
        n_samples=n_samples,
        n_features=4,
        n_classes=3,
        n_clusters_per_class=1,
        random_state=42,
    )

    # Transform to ensure positive values and realistic ranges
    features = np.abs(features)  # Make all values positive

    # Scale features to realistic ranges
    features[:, 0] = features[:, 0] * 2 + 4  # sepal length: ~4-8 cm
    features[:, 1] = features[:, 1] * 1.5 + 2  # sepal width: ~2-4.5 cm
    features[:, 2] = features[:, 2] * 3 + 1  # petal length: ~1-7 cm
    features[:, 3] = features[:, 3] * 1.5 + 0.1  # petal width: ~0.1-2.5 cm

    df = pd.DataFrame(
        features, columns=["sepal_length", "sepal_width", "petal_length", "petal_width"]
    )

    return df
