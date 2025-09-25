# backend/ml/classification_algorithms.py

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

CLASSIFICATION_ALGORITHMS = {
    "logistic_regression": {
        "type": "classification",
        "description": "Predicts probability of a binary class using a logistic function.",
        "best_for": "Binary classification datasets (yes/no, spam/ham, etc.).",
        "model": LogisticRegression(max_iter=1000),
    },
    "random_forest_classifier": {
        "type": "classification",
        "description": "Ensemble of trees for multi-class classification.",
        "best_for": "Categorical targets with many classes or noisy data.",
        "model": RandomForestClassifier(),
    },
    "gradient_boosting_classifier": {
        "type": "classification",
        "description": "Boosting method for classification tasks that focuses on hard-to-classify samples.",
        "best_for": "Complex classification problems where accuracy is critical.",
        "model": GradientBoostingClassifier(),
    },
    "decision_tree_classifier": {
        "type": "classification",
        "description": "Single decision tree model for classification tasks.",
        "best_for": "Small datasets or when model interpretability is key.",
        "model": DecisionTreeClassifier(),
    },
    "svm_classifier": {
        "type": "classification",
        "description": "Finds best hyperplane to separate classes in feature space.",
        "best_for": "Small/medium datasets with clear class boundaries.",
        "model": SVC(probability=True),
    },
    "knn_classifier": {
        "type": "classification",
        "description": "Predicts class based on the majority of nearest neighbors.",
        "best_for": "Small datasets where decision boundaries are irregular.",
        "model": KNeighborsClassifier(),
    }
}
