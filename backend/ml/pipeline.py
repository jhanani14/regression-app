import pandas as pd
from math import sqrt
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.impute import SimpleImputer

from backend.ml.classification_algorithms import CLASSIFICATION_ALGORITHMS
from backend.ml.regression_algorithms import REGRESSION_ALGORITHMS


def _make_ohe():
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def train_pipeline(df: pd.DataFrame, target: str, test_size: float = 0.2, algorithm: str = "linear_regression"):
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in dataframe")

    X = df.drop(columns=[target])
    y = df[target]

    numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = [c for c in X.columns if c not in numeric_cols]

    numeric_tf = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )
    categorical_tf = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", _make_ohe())]
    )

    preprocessor = ColumnTransformer(
        [("num", numeric_tf, numeric_cols), ("cat", categorical_tf, categorical_cols)]
    )

    if algorithm in CLASSIFICATION_ALGORITHMS:
        model = CLASSIFICATION_ALGORITHMS[algorithm]["model"]
    elif algorithm in REGRESSION_ALGORITHMS:
        model = REGRESSION_ALGORITHMS[algorithm]["model"]
    else:
        raise ValueError(f"Algorithm '{algorithm}' not supported")

    pipeline = Pipeline([("pre", preprocessor), ("model", model)])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)

    if any(k in algorithm for k in ["classifier", "logistic", "svm", "knn"]):
        metrics = {
            "accuracy": float(accuracy_score(y_test, preds)),
            "precision": float(precision_score(y_test, preds, average="weighted", zero_division=0)),
            "recall": float(recall_score(y_test, preds, average="weighted", zero_division=0)),
            "f1": float(f1_score(y_test, preds, average="weighted")),
        }
    else:
        mse = mean_squared_error(y_test, preds)
        rmse = float(sqrt(mse))
        metrics = {"rmse": rmse, "r2": float(r2_score(y_test, preds))}

    return pipeline, metrics, X_test, y_test, preds
