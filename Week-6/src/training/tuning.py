import os
import json
import optuna
import numpy as np
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold

RANDOM_STATE = 42
N_SPLITS = 5

DATA_DIR = "src/data/processed"
TUNING_DIR = "tuning"
MODEL_DIR = "models"

os.makedirs(TUNING_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)


X_train = np.load(f"{DATA_DIR}/X_train.npy")
y_train = np.load(f"{DATA_DIR}/y_train.npy")

y_train = (y_train > 10).astype(int)

def objective(trial):

    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 400),
        "max_depth": trial.suggest_int("max_depth", 5, 20),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 10),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 5),
        "random_state": RANDOM_STATE,
        "n_jobs": -1
    }

    model = RandomForestClassifier(**params)

    skf = StratifiedKFold(
        n_splits=N_SPLITS,
        shuffle=True,
        random_state=RANDOM_STATE
    )

    scores = []

    for train_idx, val_idx in skf.split(X_train, y_train):
        model.fit(X_train[train_idx], y_train[train_idx])
        preds = model.predict(X_train[val_idx])
        scores.append(f1_score(y_train[val_idx], preds))

    return np.mean(scores)


if __name__ == "__main__":

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=30)

    best_params = study.best_params
    best_params["random_state"] = RANDOM_STATE
    best_params["n_jobs"] = -1

    # Train final tuned model
    best_model = RandomForestClassifier(**best_params)
    best_model.fit(X_train, y_train)

    # Save model
    joblib.dump(best_model, f"{MODEL_DIR}/best_model.pkl")

    # Save results
    results = {
        "best_f1": study.best_value,
        "best_params": best_params
    }

    with open(f"{TUNING_DIR}/results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Hyperparameter tuning completed successfully")
