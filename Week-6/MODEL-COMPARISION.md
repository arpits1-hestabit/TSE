# Model Comparison

Task: Classification (target inferred). Primary metrics used: accuracy, precision, recall, F1, ROC AUC.

## Summary of results
- BEST_MODEL
  - accuracy: 0.6524
  - precision: 0.6592
  - recall: 0.3910
  - f1: 0.4908
  - roc_auc: 0.6940

- XGBoost
  - accuracy: 0.6494
  - precision: 0.6607
  - recall: 0.3817
  - f1: 0.4838
  - roc_auc: 0.6905

- RandomForest
  - accuracy: 0.5910
  - precision: 0.7095
  - recall: 0.0849
  - f1: 0.1516
  - roc_auc: 0.6397

- NeuralNetwork
  - accuracy: 0.5885
  - precision: 0.5487
  - recall: 0.2481
  - f1: 0.3412
  - roc_auc: 0.5996

- LogisticRegression
  - accuracy: 0.5696
  - precision: 0.5110
  - recall: 0.0087
  - f1: 0.0172
  - roc_auc: 0.5346

## Conclusion
- Selected XGBoost model for the project.
