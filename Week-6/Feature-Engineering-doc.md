# Feature Engineering 
This document describes the feature engineering pipeline that is used for training the model.

---

## Purpose
Convert cleaned transactional data (src/data/processed/final.csv) into model-ready features:
- encode categoricals
- normalize numerics
- generate 10+ derived features
- apply feature selection
- output train/test datasets and a persisted transform pipeline

---

## Inputs
- Cleaned dataset: src/data/processed/final.csv  
- Pipeline scripts:
  - src/features/build_features.py
  - src/features/feature_selector.py
  - src/features/transform.py (inference-related transforms)

---

## Pipeline steps

1. Load cleaned data (final.csv).  
2. Generate derived features:
   - datetime splits (year, month, day, hour, weekday) if InvoiceDate present
   - numeric transforms (log1p, sqrt, square)
   - pairwise interactions and ratios
   - frequency encoding for categorical(s)
   - text-derived features (Description length, token count)
   - missing-value indicator flags
   (→ ensures 10+ new features are produced)
3. Train/test split (configurable test size, seed; optional stratify for classification).  
4. Preprocessing ColumnTransformer:
   - numeric: median impute → RobustScaler
   - categorical: constant impute → OneHotEncoder (handle_unknown='ignore')
5. Feature pruning:
   - remove zero-variance features (VarianceThreshold)
   - model-based selection via feature_selector.py (RandomForest importance → top-k)
6. Persist artifacts:
   - transformed datasets: src/data/processed/features_train.csv, features_test.csv
   - pipeline artifact: src/data/processed/feature_pipeline.joblib
   - selected feature list: src/features/feature_list.json
   - importance plot: src/features/feature_importance.png

---

