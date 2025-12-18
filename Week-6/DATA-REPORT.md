# Data Report

## Source files
- EDA notebook: src/notebooks/EDA.ipynb  
- Pipeline script: src/pipelines/pipeline.py  
- Raw input: src/data/raw/data.csv  
- Processed output: src/data/processed/final.csv
---

## Summary
- Pipeline loads src/data/raw/data.csv, performs de-duplication, imputes missing values (numeric → median, categorical → mode), removes outliers by IQR and writes cleaned data to src/data/processed/final.csv.
- EDA notebook reads processed final.csv and inspects types, distributions, correlations and missingness. The notebook converts columns where possible and splits features into numeric and categorical sets.
--- 

## Pipeline behavior 
- Duplicates removed via df.drop_duplicates().
- Missing values:
  - numeric columns: filled with median.
  - categorical columns: filled with mode (first mode value).
- Outlier removal: per-numeric-column IQR filter (rows outside [Q1-1.5*IQR, Q3+1.5*IQR] are dropped).
- Outputs saved to src/data/processed/final.csv.
--- 

## Artifacts
- Cleaned data: src/data/processed/final.csv
- Plots & notebook: src/notebooks/EDA.ipynb
- Pipeline script: src/pipelines/pipeline.py

