import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

from src.features.feature_selector import select_features

RANDOM_STATE = 42


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
FEATURE_DIR = os.path.join(BASE_DIR, "features")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(FEATURE_DIR, exist_ok=True)

DATA_PATH = os.path.join(PROCESSED_DIR, "final.csv")


def generate_features(df):
    df = df.copy()

    # Date features
    df["InvoiceYear"] = df["InvoiceDate"].dt.year
    df["InvoiceMonth"] = df["InvoiceDate"].dt.month
    df["InvoiceDay"] = df["InvoiceDate"].dt.day
    df["InvoiceHour"] = df["InvoiceDate"].dt.hour
    df["InvoiceWeekday"] = df["InvoiceDate"].dt.weekday

    # Price features
    df["LogUnitPrice"] = np.log1p(df["UnitPrice"])
    df["UnitPriceSquared"] = df["UnitPrice"] ** 2

    # Text feature
    df["DescriptionLength"] = df["Description"].astype(str).apply(len)

    return df

def frequency_encode(train, test, col):
    freq = train[col].value_counts(normalize=True)
    train[col] = train[col].map(freq)
    test[col] = test[col].map(freq).fillna(0)
    return train, test

def build_features(df, target_col):

    df = df.copy()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")


    y = df[target_col].values
    X = df.drop(columns=[target_col])


    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE
    )

    for col in ["InvoiceNo", "StockCode", "CustomerID", "Description"]:
        X_train, X_test = frequency_encode(X_train, X_test, col)

    X_train = pd.get_dummies(X_train, columns=["Country"], drop_first=True)
    X_test = pd.get_dummies(X_test, columns=["Country"], drop_first=True)

    X_train, X_test = X_train.align(X_test, axis=1, fill_value=0)

    X_train = generate_features(X_train)
    X_test = generate_features(X_test)

    X_train.drop(columns=["InvoiceDate"], inplace=True)
    X_test.drop(columns=["InvoiceDate"], inplace=True)

    X_train = X_train.astype(float)
    X_test = X_test.astype(float)

    scaler = StandardScaler()
    X_train = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=X_train.columns,
        index=X_train.index
    )
    X_test = pd.DataFrame(
        scaler.transform(X_test),
        columns=X_test.columns,
        index=X_test.index
    )

    selector = select_features(X_train.values, y_train)
    X_train_sel = selector.transform(X_train.values)
    X_test_sel = selector.transform(X_test.values)

    selected_features = X_train.columns[selector.get_support()].tolist()

    with open(os.path.join(FEATURE_DIR, "feature_list.json"), "w") as f:
        json.dump(selected_features, f, indent=2)

    np.save(os.path.join(PROCESSED_DIR, "X_train.npy"), X_train_sel)
    np.save(os.path.join(PROCESSED_DIR, "X_test.npy"), X_test_sel)
    np.save(os.path.join(PROCESSED_DIR, "y_train.npy"), y_train)
    np.save(os.path.join(PROCESSED_DIR, "y_test.npy"), y_test)

    return X_train_sel, X_test_sel, y_train, y_test, selected_features


if __name__ == "__main__":

    df = pd.read_csv(DATA_PATH)

    X_train, X_test, y_train, y_test, features = build_features(
        df, target_col="TotalPrice"
    )

    model = RandomForestRegressor(
        n_estimators=150,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    importances = model.feature_importances_
    top_idx = np.argsort(importances)[-20:]

    plt.figure(figsize=(10, 6))
    plt.barh(range(len(top_idx)), importances[top_idx])
    plt.yticks(range(len(top_idx)), np.array(features)[top_idx])
    plt.title("Top Feature Importances")
    plt.tight_layout()
    plt.savefig(os.path.join(FEATURE_DIR, "feature_importance.png"))

    print("✅ Feature engineering completed successfully.")
