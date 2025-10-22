from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path
import sys
import os
from fastapi.middleware.cors import CORSMiddleware


HERE = Path(__file__).resolve().parent      
ROOT = HERE.parent                        
candidates = [
    ROOT / "models",         
    HERE / "models",            
    Path.cwd() / "models",      
    ROOT / ".." / "models",     
]

model_fname = "bot_model_lr.pkl"
scaler_fname = "scaler_lr.pkl"

def find_file(filename):
    for d in candidates:
        p = d / filename
        if p.exists():
            return p
    return None

model_path = find_file(model_fname)
scaler_path = find_file(scaler_fname)

if model_path is None or scaler_path is None:
    raise FileNotFoundError(
        f"Model or scaler not found. Searched locations:\n" +
        "\n".join(str(d / model_fname) for d in candidates) +
        "\n\nRun training (train_model.py) or move the .pkl files into a 'models' folder at the repo root."
    )

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Ensure models directory exists at repo root (same folder as this script)
models_dir = Path(__file__).resolve().parent / "app" / "models"
models_dir.mkdir(parents=True, exist_ok=True)

# Save model and scaler into repo/models
joblib.dump(model, models_dir / 'bot_model_lr.pkl')
joblib.dump(scaler, models_dir / 'scaler_lr.pkl')
print("Model and scaler saved in:", models_dir)

app = FastAPI(title="Bot Detection API")
origins = [
    "http://localhost:3000", 
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],      # Allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)
class UserData(BaseModel):
    followers_count: float
    following_count: float
    post_count: float
    account_age_days: float
    has_profile_picture: int
    has_bio: int
    avg_post_interval: float

@app.post("/predict")
def predict_bot(user: UserData):
    user_df = pd.DataFrame([user.dict()])
    user_scaled = scaler.transform(user_df)
    prediction = model.predict(user_scaled)[0]
    probability = model.predict_proba(user_scaled)[0][prediction]
    result = {
        "prediction": int(prediction),      
        "probability": float(probability)
    }
    return result

@app.get("/feature_importance")
@app.get("/feature_importance")
def feature_importance():
    feature_names = [
        "followers_count",
        "following_count",
        "post_count",
        "account_age_days",
        "has_profile_picture",
        "has_bio",
        "avg_post_interval"
    ]
    coefficients = pd.Series(model.coef_[0], index=feature_names)
    sorted_features = coefficients.sort_values(ascending=False)
    return sorted_features.to_dict()
@app.get("/")
def root():
    return {"message": "Welcome to the Bot Detection API!"}
