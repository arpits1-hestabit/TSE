import os
import pandas as pd
import numpy as np

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(SRC_DIR, "data", "raw", "data.csv")
PROCESSED_DATA_DIR = os.path.join(SRC_DIR, "data", "processed")
OUTPUT_PATH = os.path.join(PROCESSED_DATA_DIR, "final.csv")


os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
 
# Loading dataset
def load_data():
    try:
        df = pd.read_csv(RAW_DATA_PATH)
    except UnicodeDecodeError:
        df = pd.read_csv(RAW_DATA_PATH, encoding='latin1')
    print(f"✅ Data loaded: {df.shape}")
    return df

# Cleaning dataset
def clean_data(df):
    # Remove duplicates
    before_dup = df.shape[0]
    df = df.drop_duplicates()
    print(f"✅ Duplicates removed: {before_dup - df.shape[0]}")

    # Handle missing values(medisn for numeric and mode for categorical)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns

    for col in numeric_cols:
        df[col].fillna(df[col].median(), inplace=True)
    for col in categorical_cols:
        df[col].fillna(df[col].mode()[0], inplace=True)
    print(f"✅ Missing values handled")

    # Remove outliers using IQR method
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower) & (df[col] <= upper)]
    print(f"✅ Outliers removed")
    
    return df

# Save cleaned data
def save_data(df):
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Cleaned data saved at: {OUTPUT_PATH}")

# Main pipeline function
def main():
    df = load_data()
    df = clean_data(df)
    save_data(df)

if __name__ == "__main__":
    main()

