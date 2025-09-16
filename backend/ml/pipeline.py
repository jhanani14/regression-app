from math import sqrt
import pandas as pd
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
    confusion_matrix,
)
from sklearn.impute import SimpleImputer

# Models
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso
from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier,
    GradientBoostingRegressor,
    GradientBoostingClassifier,
)
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier


def _make_ohe():
    """Safe OneHotEncoder for sklearn versions"""
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


ALGORITHMS = {
    # Regression
    "linear_regression": LinearRegression(),
    "ridge_regression": Ridge(),
    "lasso_regression": Lasso(),
    "random_forest_regressor": RandomForestRegressor(),
    "gradient_boosting_regressor": GradientBoostingRegressor(),
    "decision_tree_regressor": DecisionTreeRegressor(),

    # Classification
    "logistic_regression": LogisticRegression(max_iter=1000),
    "random_forest_classifier": RandomForestClassifier(),
    "gradient_boosting_classifier": GradientBoostingClassifier(),
    "decision_tree_classifier": DecisionTreeClassifier(),
    "svm_classifier": SVC(probability=True),
    "knn_classifier": KNeighborsClassifier(),
}


def train_pipeline(
    df: pd.DataFrame,
    target: str,
    test_size: float = 0.2,
    algorithm: str = "linear_regression",
):
    """Train regression/classification pipeline with preprocessing + metrics"""
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in dataframe")

    X = df.drop(columns=[target])
    y = df[target]

    # Identify column types
    numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = [c for c in X.columns if c not in numeric_cols]

    # Preprocessors
    numeric_tf = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_tf = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", _make_ohe()),
        ]
    )

    preprocessor = ColumnTransformer(
        [
            ("num", numeric_tf, numeric_cols),
            ("cat", categorical_tf, categorical_cols),
        ]
    )

    # Select algorithm
    model = ALGORITHMS.get(algorithm)
    if not model:
        raise ValueError(f"Algorithm '{algorithm}' not supported")

    pipeline = Pipeline([("pre", preprocessor), ("model", model)])

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)

    # Metrics
    if any(k in algorithm for k in ["classifier", "logistic", "svm", "knn"]):
        metrics = {
            "accuracy": float(accuracy_score(y_test, preds)),
            "precision": float(
                precision_score(y_test, preds, average="weighted", zero_division=0)
            ),
            "recall": float(
                recall_score(y_test, preds, average="weighted", zero_division=0)
            ),
            "f1": float(f1_score(y_test, preds, average="weighted")),
        }
    else:  # regression
        mse = mean_squared_error(y_test, preds)
        rmse = float(sqrt(mse))
        metrics = {
            "rmse": rmse,
            "r2": float(r2_score(y_test, preds)),
        }

    return pipeline, metrics, X_test, y_test, preds
