# Deployment Notes

## Project Overview

This project deploys a trained machine learning classification model as a **production-ready API** using **FastAPI**, with optional **Streamlit dashboard** support and **Docker-based containerization**. The system supports prediction logging, request tracking, input validation, model versioning, and basic drift monitoring.

---

## Architecture

```
src/
├── deployment/
│   └── api.py
├── monitoring/
│   └── drift_checker.py
├── models/
│   └── best_model.pkl
├── features/
│   └── feature_list.json
prediction_logs.csv
Dockerfile
requirements.txt
```

---

## API Deployment

### Entry Point

* **Module:** `src/deployment/api.py`
* **ASGI App:** `app`

Run locally:

```bash
uvicorn src.deployment.api:app --reload
```

Health check:

```http
GET /
```

Prediction endpoint:

```http
POST /predict
```

---

## Model Loading

* Models are loaded from:

  ```
  models/best_model.pkl
  ```

MODEL_VERSION=v1


Best practice:
- Never overwrite an existing model
- Store models as:
```

best_model_v1.pkl
best_model_v2.pkl

````

---

## Logging

Predictions are logged to:

```
src/logs/prediction_logs.csv
```

Each log contains:

* request_id
* timestamp
* prediction
* probability
* key input features

Used for:

* Monitoring
* Debugging
* Drift detection

---

## Drift Monitoring

Script:

```
src/monitoring/drift_checker.py
```

Method:

* Kolmogorov–Smirnov test
* Compares training reference vs live data

Output example:

```python
{'Quantity': 'DRIFT', 'UnitPrice': 'NO_DRIFT'}
```

---

## Streamlit Dashboard

Run dashboard:

```bash
streamlit run streamlit_app.py
```

Features:

* Input form
* Live prediction
* Probability display
* Recent prediction logs

 Note: API must be running before dashboard.

---

## Docker Deployment

### Build Image

```bash
docker build -t ml-prediction-api .
```

### Run Container

```bash
docker run -p 8000:8000 --env-file .env ml-prediction-api
```

Ensure:

* `uvicorn` is in `requirements.txt`
* `CMD` uses full python module path

---

## Environment Variables

`.env.example`

```env
MODEL_VERSION=v1
PREDICTION_THRESHOLD=0.3
LOG_PATH=src/prediction_logs.csv
```

---

## Common Issues happened & Fixes

### Feature shape mismatch

-> Ensure training & inference feature list are identical

### Always predicting 0 or 1

-> Adjust threshold
-> Calibrate model

### Docker uvicorn not found

-> Add `uvicorn[standard]` to requirements

### Streamlit cannot reach API

-> API must run on `0.0.0.0` inside Docker


