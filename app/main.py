from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi import UploadFile, File
from pdfminer.high_level import extract_text
import joblib
import os

app = FastAPI(
title="AI Hiring Platform",
description="Advanced AI Hiring & Workforce Optimization"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- 1. Robust Path Resolution ---

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
VIEWS_DIR = os.path.join(PROJECT_ROOT, "views")

# Initialize variables

vectorizer = None
classifier_model = None

# --- 2. Load trained AI models ---

print(f"Looking for models in: {MODELS_DIR}")

try:
    vectorizer = joblib.load(os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib"))
    classifier_model = joblib.load(os.path.join(MODELS_DIR, "resume_model.joblib"))
    print("✅ Models loaded successfully!")

except Exception as e:
    print(f"❌ Failed to load models: {e}")

# --- 3. Define input structure ---

class ResumeInput(BaseModel):
    text: str

# --- 4. Web Page Route (Frontend UI) ---

# --- 4. Web Page Route (Frontend UI) ---

@app.get("/")
def home():
    file_path = os.path.join(PROJECT_ROOT, "views", "index.html")
    return FileResponse(file_path)

# --- 5. API Endpoint for Prediction ---

@app.post("/predict-role")
def predict_role(resume: ResumeInput):
    if vectorizer is None or classifier_model is None:
        return {
            "status": "error",
            "message": "Models failed to load. Check terminal for details."
        }

    try:
        # Convert resume text into vector
        vectorized_text = vectorizer.transform([resume.text])

        # Predict job role
        prediction = classifier_model.predict(vectorized_text)

        final_role = str(prediction[0])

        return {
            "status": "success",
            "predicted_role": final_role
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Prediction error: {str(e)}"
        }
        from fastapi import UploadFile, File
import pdfplumber

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    try:

        text = ""

        if file.filename.endswith(".pdf"):
            with pdfplumber.open(file.file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text

        else:
            content = await file.read()
            text = content.decode("utf-8")

        vectorized = vectorizer.transform([text])
        prediction = classifier_model.predict(vectorized)

        return {
            "status":"success",
            "predicted_role": str(prediction[0])
        }

    except Exception as e:
        return {
            "status":"error",
            "message":str(e)
        }
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    if vectorizer is None or classifier_model is None:
        return {"status": "error", "message": "Models not loaded"}

    try:
        # Save uploaded file temporarily
        file_path = f"temp_{file.filename}"

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Extract text from PDF
        text = extract_text(file_path)

        # Convert text to vector
        vectorized_text = vectorizer.transform([text])

        # Predict job role
        prediction = classifier_model.predict(vectorized_text)

        # Remove temp file
        os.remove(file_path)

        return {
            "status": "success",
            "predicted_role": str(prediction[0])
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }