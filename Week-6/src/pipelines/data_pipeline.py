import os
import pandas as pd
import numpy as np

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(SRC_DIR, "data", "raw", "data.csv")
PROCESSED_DATA_DIR = os.path.join(SRC_DIR, "data", "processed")
OUTPUT_PATH = os.path.join(PROCESSED_DATA_DIR, "final.csv")


os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
 
def load_data():
    try:
        df = pd.read_csv(RAW_DATA_PATH)
    except UnicodeDecodeError:
        df = pd.read_csv(RAW_DATA_PATH, encoding='latin1')
    print(f"Data loaded: {df.shape}")
    return df

def clean_data(df):
    df = df.drop_duplicates()


    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns


    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    print(df[numeric_cols])
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    mask = pd.Series(True, index=df.index)
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        mask &= df[col].between(lower, upper)

    df = df[mask]

    return df


def save_data(df):
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Cleaned data saved at: {OUTPUT_PATH}")

def main():
    df = load_data()
    df = clean_data(df)
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    save_data(df)

if __name__ == "__main__":
    main()

