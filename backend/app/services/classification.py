# Lazy-load sklearn to avoid segfault issues in Docker Desktop Mac
# Store only metadata at module level, create models when needed

_CLASSIFICATION_METADATA = {
    "logistic_regression": {
        "type": "classification",
        "description": "Predicts probability of a binary class using a logistic function.",
        "best_for": "Binary classification datasets (yes/no, spam/ham, etc.).",
    },
    "random_forest_classifier": {
        "type": "classification",
        "description": "Ensemble of trees for multi-class classification.",
        "best_for": "Categorical targets with many classes or noisy data.",
    },
    "gradient_boosting_classifier": {
        "type": "classification",
        "description": "Boosting method for classification tasks that focuses on hard-to-classify samples.",
        "best_for": "Complex classification problems where accuracy is critical.",
    },
    "decision_tree_classifier": {
        "type": "classification",
        "description": "Single decision tree model for classification tasks.",
        "best_for": "Small datasets or when model interpretability is key.",
    },
    "svm_classifier": {
        "type": "classification",
        "description": "Finds best hyperplane to separate classes in feature space.",
        "best_for": "Small/medium datasets with clear class boundaries.",
    },
    "knn_classifier": {
        "type": "classification",
        "description": "Predicts class based on the majority of nearest neighbors.",
        "best_for": "Small datasets where decision boundaries are irregular.",
    }
}

def _create_classification_model(algorithm_name):
    """Create a classification model instance when needed"""
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    
    models = {
        "logistic_regression": LogisticRegression(max_iter=1000),
        "random_forest_classifier": RandomForestClassifier(),
        "gradient_boosting_classifier": GradientBoostingClassifier(),
        "decision_tree_classifier": DecisionTreeClassifier(),
        "svm_classifier": SVC(probability=True),
        "knn_classifier": KNeighborsClassifier(),
    }
    return models.get(algorithm_name)

def get_classification_algorithm(algorithm_name):
    """Get classification algorithm with model (lazy-loaded)"""
    metadata = _CLASSIFICATION_METADATA.get(algorithm_name, {})
    if metadata:
        metadata = metadata.copy()
        metadata["model"] = _create_classification_model(algorithm_name)
    return metadata

# For backward compatibility - returns metadata only
CLASSIFICATION_ALGORITHMS = _CLASSIFICATION_METADATA
