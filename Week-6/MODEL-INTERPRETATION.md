# Model Interpretation

Location (artifacts)
- Model: src/models/best_model.pkl (XGBClassifier)
- Metrics: src/evaluation/metrics.json
- SHAP summary: src/evaluation/shap_summary.png
- Confusion matrix: src/evaluation/confusion_matrix.png
- Feature importances: src/features/feature_importance.png
- Feature list: src/features/feature_list.json

1. Summary metrics (from metrics.json)
- BEST_MODEL (XGBClassifier)
  - accuracy: 0.6524
  - precision: 0.6592
  - recall: 0.3910
  - F1: 0.4908

2. Confusion matrix / class behaviour
- High false negatives relative to true positives (recall ~0.39).  
- If business cost of missed positives is high, adjust threshold or retrain with class-weighting/sampling.

3. Feature importance & SHAP
- Use src/features/feature_importance.png for global importance ranking.  
- Use SHAP (src/evaluation/shap_analysis.py / shap_summary.png) for:
  - Directional effect (which features increase/decrease predicted probability)
  - Interaction effects and per-sample explanations
- Action: inspect top 10 SHAP features for leakage or proxies of target; remove or transform if leakage found.

