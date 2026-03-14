import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

# Create models folder if it doesn't exist
os.makedirs("models", exist_ok=True)

# Example resume dataset
data = {
    "resume":[
        "python machine learning data science pandas numpy statistics",
        "java spring boot backend development mysql rest api",
        "html css javascript react frontend ui ux",
        "deep learning python tensorflow ai neural networks",
        "django flask python backend api development",
        "react javascript frontend ui design web development"
    ],
    "role":[
        "Data Scientist",
        "Backend Developer",
        "Frontend Developer",
        "AI Engineer",
        "Backend Developer",
        "Frontend Developer"
    ]
}

df = pd.DataFrame(data)

X = df["resume"]
y = df["role"]

# Convert text to numbers
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Train model
model = MultinomialNB()
model.fit(X_vec, y)

# Save model files
joblib.dump(vectorizer, "models/tfidf_vectorizer.joblib")
joblib.dump(model, "models/resume_model.joblib")

print("✅ Model trained and saved in models folder")