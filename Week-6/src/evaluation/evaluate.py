import os
import json
import joblib
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import roc_curve, auc

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
EVAL_DIR = os.path.join(BASE_DIR, "evaluation")

os.makedirs(EVAL_DIR, exist_ok=True)

# Loading model and data
model = joblib.load(MODEL_PATH)

X_test = np.load(os.path.join(DATA_DIR, "X_test.npy"))
y_test = np.load(os.path.join(DATA_DIR, "y_test.npy"))

y_test = (y_test > 10).astype(int)

y_prob = model.predict_proba(X_test)[:, 1]

# ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

# Best threshold (Youden's J)
best_idx = np.argmax(tpr - fpr)
best_threshold = thresholds[best_idx]

with open(os.path.join(EVAL_DIR, "threshold.json"), "w") as f:
    json.dump(
        {
            "best_threshold": float(best_threshold),
            "roc_auc": float(roc_auc)
        },
        f,
        indent=2
    )

# Plot ROC
plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(EVAL_DIR, "roc_curve.png"))

print("ROC curve saved")
print("Best threshold:", best_threshold)
print("AUC:", roc_auc)
