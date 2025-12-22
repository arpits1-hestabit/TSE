import os
import json
import joblib
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

RANDOM_STATE = 42
N_SPLITS = 5


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
MODEL_DIR = os.path.join(BASE_DIR, "models")
EVAL_DIR = os.path.join(BASE_DIR, "evaluation")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(EVAL_DIR, exist_ok=True)


X_train = np.load(os.path.join(PROCESSED_DIR, "X_train.npy"))
X_test = np.load(os.path.join(PROCESSED_DIR, "X_test.npy"))
y_train = np.load(os.path.join(PROCESSED_DIR, "y_train.npy"))
y_test = np.load(os.path.join(PROCESSED_DIR, "y_test.npy"))

y_train = (y_train > 10).astype(int)
y_test = (y_test > 10).astype(int)

MODELS = {
    "LogisticRegression": LogisticRegression(
        penalty="l2",
        max_iter=1000,
        random_state=RANDOM_STATE
    ),
    "RandomForest": RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=RANDOM_STATE,
        n_jobs=-1
    ),
    "XGBoost": XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="binary:logistic",
        eval_metric="logloss",
        tree_method="hist",   
        random_state=RANDOM_STATE,
        n_jobs=-1
    ),
    "NeuralNetwork": MLPClassifier(
    hidden_layer_sizes=(32,),
    alpha=0.01,                
    max_iter=200,
    early_stopping=True,       
    validation_fraction=0.1,
    n_iter_no_change=10,
    solver="adam",
    random_state=RANDOM_STATE,
    verbose=False
)

}

def cross_validate(model, X, y):
    skf = StratifiedKFold(
        n_splits=N_SPLITS,
        shuffle=True,
        random_state=RANDOM_STATE
    )

    scores = {
        "accuracy": [],
        "precision": [],
        "recall": [],
        "f1": [],
        "roc_auc": []
    }

    for train_idx, val_idx in skf.split(X, y):
        X_tr, X_val = X[train_idx], X[val_idx]
        y_tr, y_val = y[train_idx], y[val_idx]

        model.fit(X_tr, y_tr)
        y_pred = model.predict(X_val)
        y_prob = model.predict_proba(X_val)[:, 1]

        scores["accuracy"].append(accuracy_score(y_val, y_pred))
        scores["precision"].append(precision_score(y_val, y_pred))
        scores["recall"].append(recall_score(y_val, y_pred))
        scores["f1"].append(f1_score(y_val, y_pred))
        scores["roc_auc"].append(roc_auc_score(y_val, y_prob))

    return {k: float(np.mean(v)) for k, v in scores.items()}

def train_and_select(X_train, X_test, y_train, y_test):

    metrics = {}
    best_model = None
    best_f1 = -1

    for name, model in MODELS.items():
        print(f"🔹 Training {name}...")
        cv_scores = cross_validate(model, X_train, y_train)
        metrics[name] = cv_scores

        if cv_scores["f1"] > best_f1:
            best_f1 = cv_scores["f1"]
            best_model = model

    # Retrain best model on full training data
    best_model.fit(X_train, y_train)

    # Final evaluation
    y_pred = best_model.predict(X_test)
    y_prob = best_model.predict_proba(X_test)[:, 1]

    metrics["BEST_MODEL"] = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_prob)
    }

    return best_model, metrics, y_test, y_pred

if __name__ == "__main__":

    best_model, metrics, y_true, y_pred = train_and_select(
        X_train, X_test, y_train, y_test
    )

    # Save best model
    joblib.dump(best_model, os.path.join(MODEL_DIR, "best_model.pkl"))

    # Save metrics
    with open(os.path.join(EVAL_DIR, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(cm)
    disp.plot()
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(EVAL_DIR, "confusion_matrix.png"))

    print("Best model saved.")
