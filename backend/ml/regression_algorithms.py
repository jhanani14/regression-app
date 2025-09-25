# backend/ml/regression_algorithms.py

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor

REGRESSION_ALGORITHMS = {
    "linear_regression": {
        "type": "regression",
        "description": "Fits a straight line to predict a continuous numeric target.",
        "best_for": "Continuous numeric datasets with linear relationships.",
        "model": LinearRegression(),
    },
    "ridge_regression": {
        "type": "regression",
        "description": "Linear regression with L2 regularization to reduce overfitting.",
        "best_for": "Numeric datasets with many correlated features or risk of overfitting.",
        "model": Ridge(),
    },
    "lasso_regression": {
        "type": "regression",
        "description": "Linear regression with L1 regularization to perform feature selection.",
        "best_for": "Sparse datasets where you want to eliminate irrelevant features.",
        "model": Lasso(),
    },
    "random_forest_regressor": {
        "type": "regression",
        "description": "Ensemble of decision trees for robust predictions.",
        "best_for": "Large datasets with non-linear relationships.",
        "model": RandomForestRegressor(),
    },
    "gradient_boosting_regressor": {
        "type": "regression",
        "description": "Boosting method that combines weak learners to create strong models.",
        "best_for": "Complex non-linear regression problems where accuracy is key.",
        "model": GradientBoostingRegressor(),
    },
    "decision_tree_regressor": {
        "type": "regression",
        "description": "Single decision tree model for regression tasks.",
        "best_for": "Simple datasets where interpretability is important.",
        "model": DecisionTreeRegressor(),
    },
}
