import os
import json
import joblib
import shap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

MODEL_PATH = os.path.join(BASE_DIR, "src", "models", "best_model.pkl")
DATA_DIR = os.path.join(BASE_DIR, "src", "data", "processed")
FEATURES_PATH = os.path.join(BASE_DIR, "src", "features", "feature_list.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "src", "evaluation")

os.makedirs(OUTPUT_DIR, exist_ok=True)


model = joblib.load(MODEL_PATH)

X_train = np.load(os.path.join(DATA_DIR, "X_train.npy"))

with open(FEATURES_PATH) as f:
    feature_names = json.load(f)


X_sample = X_train[:500]

explainer = shap.TreeExplainer(model)
shap_values = explainer(X_sample)

plt.figure()
shap.summary_plot(
    shap_values.values,
    X_sample,
    feature_names=feature_names,
    max_display=15,
    show=False
)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "shap_summary.png"))
plt.close()

print("SHAP summary plot saved")
