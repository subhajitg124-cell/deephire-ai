from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pdfminer.high_level import extract_text
import joblib
import os
import uuid

app = FastAPI(
    title="AI Hiring Platform",
    description="Advanced AI Hiring & Workforce Optimization"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------------------
# 1. Robust Path Resolution
# -------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
VIEWS_DIR = os.path.join(PROJECT_ROOT, "views")

vectorizer = None
classifier_model = None

# -------------------------------
# 2. Load Trained Models
# -------------------------------

print(f"Looking for models in: {MODELS_DIR}")

try:
    vectorizer = joblib.load(os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib"))
    classifier_model = joblib.load(os.path.join(MODELS_DIR, "resume_model.joblib"))
    print("✅ Models loaded successfully!")

except Exception as e:
    print(f"❌ Failed to load models: {e}")

# -------------------------------
# 3. Input Structure
# -------------------------------

class ResumeInput(BaseModel):
    text: str

# -------------------------------
# 4. Frontend Route
# -------------------------------

@app.get("/")
def home():
    file_path = os.path.join(VIEWS_DIR, "index.html")
    return FileResponse(file_path)

# -------------------------------
# 5. Resume Text Prediction
# -------------------------------

@app.post("/predict-role")
def predict_role(resume: ResumeInput):

    text = resume.text

    # Validation
    if not text.strip():
        return {
            "status": "error",
            "message": "Resume text cannot be empty"
        }

    if vectorizer is None or classifier_model is None:
        return {
            "status": "error",
            "message": "Models failed to load"
        }

    try:
        # Convert text to vector
        vectorized_text = vectorizer.transform([text])

        # Predict job role
        prediction = classifier_model.predict(vectorized_text)

        return {
            "status": "success",
            "predicted_role": str(prediction[0])
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Prediction error: {str(e)}"
        }

# -------------------------------
# 6. Resume File Upload
# -------------------------------

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    if vectorizer is None or classifier_model is None:
        return {
            "status": "error",
            "message": "Models not loaded"
        }

    try:
        # Unique temporary file
        file_path = f"temp_{uuid.uuid4()}.pdf"

        # Save file
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Extract text
        text = extract_text(file_path)

        # Remove temp file
        os.remove(file_path)

        # Validation
        if not text.strip():
            return {
                "status": "error",
                "message": "Uploaded file has no readable text"
            }

        # Convert text to vector
        vectorized_text = vectorizer.transform([text])

        # Predict role
        prediction = classifier_model.predict(vectorized_text)

        return {
            "status": "success",
            "predicted_role": str(prediction[0])
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }