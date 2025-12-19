# app/services/plots.py

# IMPORTANT: use non-GUI backend for FastAPI / Docker / ECS
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import io
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    RocCurveDisplay
)

# -------------------------
# Regression: residual plot
# -------------------------
def residual_plot(y_true, y_pred):
    fig, ax = plt.subplots()
    ax.scatter(y_pred, y_true - y_pred, alpha=0.6)
    ax.axhline(0, linestyle="--", linewidth=1)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Residuals")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


# -------------------------
# Regression: predicted vs actual
# -------------------------
def predicted_vs_actual(y_true, y_pred):
    fig, ax = plt.subplots()
    ax.scatter(y_true, y_pred, alpha=0.6)
    ax.plot([min(y_true), max(y_true)], [min(y_true), max(y_true)], linestyle="--")
    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


# -------------------------
# Classification: confusion matrix
# -------------------------
def confusion_matrix_plot(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)

    fig, ax = plt.subplots()
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(ax=ax, cmap="Blues", values_format="d", colorbar=False)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


# -------------------------
# Classification: ROC curve
# -------------------------
def roc_curve_plot(model, X_test, y_test):
    """
    Works only if classifier has predict_proba
    """
    try:
        fig, ax = plt.subplots()
        RocCurveDisplay.from_estimator(model, X_test, y_test, ax=ax)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)
        return buf.getvalue()
    except Exception:
        return None
