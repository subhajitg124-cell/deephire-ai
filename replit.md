# DeepHire - AI Hiring Platform

## Overview
An AI-powered hiring and workforce optimization platform. Uses machine learning (TF-IDF + Naive Bayes) to classify resumes and predict job roles from either pasted text or uploaded PDF files.

## Tech Stack
- **Backend/Server:** FastAPI (Python) with Uvicorn
- **ML:** scikit-learn (TF-IDF vectorizer + Multinomial Naive Bayes classifier)
- **PDF Processing:** pdfminer.six
- **Frontend:** Static HTML/CSS/JS served by FastAPI

## Project Structure
```
app/main.py          - FastAPI app (API routes + serves frontend)
models/              - Pre-trained ML model files (.joblib)
views/index.html     - Frontend HTML
static/              - CSS, JS, logo assets
train_model.py       - Script to retrain ML models
requirements.txt     - Python dependencies
```

## Running the App
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000
```

## Key Endpoints
- `GET /` — Serves the frontend
- `POST /predict-role` — Accepts JSON `{ "text": "..." }`, returns predicted job role
- `POST /upload-resume` — Accepts PDF file upload, returns predicted job role

## Dependencies
All listed in `requirements.txt`. Install with:
```bash
pip install -r requirements.txt
```
