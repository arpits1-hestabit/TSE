import streamlit as st
import requests
import pandas as pd
import os

API_URL = "http://api:8000/predict"
LOG_PATH = "src/logs/prediction_logs.csv"

st.set_page_config(page_title="ML Prediction Dashboard", layout="centered")

st.title("ML Prediction Dashboard")

st.subheader("Enter Input Features")

with st.form("prediction_form"):
    Quantity = st.number_input("Quantity", min_value=1, value=5)
    UnitPrice = st.number_input("Unit Price", min_value=0.01, value=2.5)

    Country = st.selectbox(
        "Country",
        [
            "United Kingdom",
            "France",
            "Germany",
            "Netherlands",
            "Spain",
            "Italy",
            "Belgium",
        ],
    )

    Description = st.text_input(
        "Description",
        "WHITE HANGING HEART T-LIGHT HOLDER"
    )

    InvoiceDate = st.text_input(
        "Invoice Date (YYYY-MM-DD HH:MM)",
        "2010-12-01 08:26"
    )

    submitted = st.form_submit_button("Predict")

if submitted:
    payload = {
        "Quantity": Quantity,
        "UnitPrice": UnitPrice,
        "Country": Country,
        "Description": Description,
        "InvoiceDate": InvoiceDate
    }

    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()

        st.success("Prediction Output:-")
        st.metric("Prediction", result["prediction"])
        st.metric("Probability", round(result["probability"], 3))

    except Exception as e:
        st.error(f"API Error: {e}")

