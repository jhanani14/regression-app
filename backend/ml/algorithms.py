# backend/ml/algorithms.py

ALGORITHM_INFO = {
    # ========================
    # REGRESSION ALGORITHMS
    # ========================
    "linear_regression": {
        "type": "regression",
        "description": "Fits a straight line to predict a continuous numeric target.",
        "best_for": "Continuous numeric datasets with linear relationships."
    },
    "ridge_regression": {
        "type": "regression",
        "description": "Linear regression with L2 regularization to reduce overfitting.",
        "best_for": "Numeric datasets with many correlated features or risk of overfitting."
    },
    "lasso_regression": {
        "type": "regression",
        "description": "Linear regression with L1 regularization to perform feature selection.",
        "best_for": "Sparse datasets where you want to eliminate irrelevant features."
    },
    "random_forest_regressor": {
        "type": "regression",
        "description": "Ensemble of decision trees for robust predictions.",
        "best_for": "Large datasets with non-linear relationships."
    },
    "gradient_boosting_regressor": {
        "type": "regression",
        "description": "Boosting method that combines weak learners to create strong models.",
        "best_for": "Complex non-linear regression problems where accuracy is key."
    },
    "decision_tree_regressor": {
        "type": "regression",
        "description": "Single decision tree model for regression tasks.",
        "best_for": "Simple datasets where interpretability is important."
    },

    # ========================
    # CLASSIFICATION ALGORITHMS
    # ========================
    "logistic_regression": {
        "type": "classification",
        "description": "Predicts probability of a binary class using a logistic function.",
        "best_for": "Binary classification datasets (yes/no, spam/ham, etc.)."
    },
    "random_forest_classifier": {
        "type": "classification",
        "description": "Ensemble of trees for multi-class classification.",
        "best_for": "Categorical targets with many classes or noisy data."
    },
    "gradient_boosting_classifier": {
        "type": "classification",
        "description": "Boosting method for classification tasks that focuses on hard-to-classify samples.",
        "best_for": "Complex classification problems where accuracy is critical."
    },
    "decision_tree_classifier": {
        "type": "classification",
        "description": "Single decision tree model for classification tasks.",
        "best_for": "Small datasets or when model interpretability is key."
    },
    "svm_classifier": {
        "type": "classification",
        "description": "Finds best hyperplane to separate classes in feature space.",
        "best_for": "Small/medium datasets with clear class boundaries."
    },
    "knn_classifier": {
        "type": "classification",
        "description": "Predicts class based on the majority of nearest neighbors.",
        "best_for": "Small datasets where decision boundaries are irregular."
    }
}
