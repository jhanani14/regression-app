# Lazy-load sklearn to avoid segfault issues in Docker Desktop Mac
# Store only metadata at module level, create models when needed

_REGRESSION_METADATA = {
    "linear_regression": {
        "type": "regression",
        "description": "Fits a straight line to predict a continuous numeric target.",
        "best_for": "Continuous numeric datasets with linear relationships.",
    },
    "ridge_regression": {
        "type": "regression",
        "description": "Linear regression with L2 regularization to reduce overfitting.",
        "best_for": "Numeric datasets with many correlated features or risk of overfitting.",
    },
    "lasso_regression": {
        "type": "regression",
        "description": "Linear regression with L1 regularization to perform feature selection.",
        "best_for": "Sparse datasets where you want to eliminate irrelevant features.",
    },
    "random_forest_regressor": {
        "type": "regression",
        "description": "Ensemble of decision trees for robust predictions.",
        "best_for": "Large datasets with non-linear relationships.",
    },
    "gradient_boosting_regressor": {
        "type": "regression",
        "description": "Boosting method that combines weak learners to create strong models.",
        "best_for": "Complex non-linear regression problems where accuracy is key.",
    },
    "decision_tree_regressor": {
        "type": "regression",
        "description": "Single decision tree model for regression tasks.",
        "best_for": "Simple datasets where interpretability is important.",
    },
}

def _create_regression_model(algorithm_name):
    """Create a regression model instance when needed"""
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.tree import DecisionTreeRegressor
    
    models = {
        "linear_regression": LinearRegression(),
        "ridge_regression": Ridge(),
        "lasso_regression": Lasso(),
        "random_forest_regressor": RandomForestRegressor(),
        "gradient_boosting_regressor": GradientBoostingRegressor(),
        "decision_tree_regressor": DecisionTreeRegressor(),
    }
    return models.get(algorithm_name)

def get_regression_algorithm(algorithm_name):
    """Get regression algorithm with model (lazy-loaded)"""
    metadata = _REGRESSION_METADATA.get(algorithm_name, {})
    if metadata:
        metadata = metadata.copy()
        metadata["model"] = _create_regression_model(algorithm_name)
    return metadata

# For backward compatibility - returns metadata only
REGRESSION_ALGORITHMS = _REGRESSION_METADATA
