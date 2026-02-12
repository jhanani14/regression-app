from math import sqrt
# Lazy-load pandas and sklearn to avoid segfault issues in Docker Desktop Mac
# These will only be imported when train_pipeline is actually called

# ✅ Import algorithms (lazy-loaded)
from app.services.classification import CLASSIFICATION_ALGORITHMS, get_classification_algorithm
from app.services.regression import REGRESSION_ALGORITHMS, get_regression_algorithm


def _make_ohe():
    """Create OneHotEncoder compatible with scikit-learn version"""
    from sklearn.preprocessing import OneHotEncoder
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def train_pipeline(
    df,  # pd.DataFrame - type hint removed to avoid importing pandas at module level
    target: str,
    test_size: float = 0.2,
    algorithm: str = "linear_regression"
):
    """Train a pipeline (preprocessing + model) and return metrics"""
    # Lazy-load pandas
    import pandas as pd
    
    # Ensure df is a DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df must be a pandas DataFrame")

    # ✅ Ensure target column exists
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in dataframe")

    # ✅ Handle missing target values (y)
    if df[target].isna().sum() > 0:
        print(f"⚠️ Found {df[target].isna().sum()} missing target values — dropping those rows.")
        df = df.dropna(subset=[target])

    # ✅ Separate features and target
    X = df.drop(columns=[target])
    y = df[target]

    # ✅ Handle any empty rows or columns (all NaN)
    X = X.dropna(how="all", axis=0)
    X = X.dropna(how="all", axis=1)

    # ✅ Identify numeric and categorical columns
    numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = [c for c in X.columns if c not in numeric_cols]

    # ✅ Lazy-load sklearn components
    from sklearn.model_selection import train_test_split
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    
    # ✅ Preprocessing for numeric and categorical data
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

    # ✅ Combine preprocessing
    preprocessor = ColumnTransformer(
        [("num", numeric_tf, numeric_cols), ("cat", categorical_tf, categorical_cols)]
    )

    # ✅ Choose model (lazy-loaded to avoid segfault)
    if algorithm in CLASSIFICATION_ALGORITHMS:
        algo_data = get_classification_algorithm(algorithm)
        model = algo_data["model"] if algo_data else None
    elif algorithm in REGRESSION_ALGORITHMS:
        algo_data = get_regression_algorithm(algorithm)
        model = algo_data["model"] if algo_data else None
    else:
        raise ValueError(f"Algorithm '{algorithm}' not supported")
    
    if model is None:
        raise ValueError(f"Failed to create model for algorithm '{algorithm}'")

    # ✅ Build final pipeline
    pipeline = Pipeline([("pre", preprocessor), ("model", model)])

    # ✅ Split and train (train_test_split already imported above)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    # Fit model
    pipeline.fit(X_train, y_train)

    # Predict
    preds = pipeline.predict(X_test)

    # ✅ Lazy-load metrics
    from sklearn.metrics import (
        mean_squared_error,
        r2_score,
        accuracy_score,
        f1_score,
        precision_score,
        recall_score,
    )
    
    # ✅ Compute metrics based on model type
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
    else:
        mse = mean_squared_error(y_test, preds)
        rmse = float(sqrt(mse))
        metrics = {"rmse": rmse, "r2": float(r2_score(y_test, preds))}

    return pipeline, metrics, X_test, y_test, preds
