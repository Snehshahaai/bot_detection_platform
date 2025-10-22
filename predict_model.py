import pandas as pd
import joblib

# Load model and scaler
model = joblib.load('../models/bot_model_lr.pkl')
scaler = joblib.load('../models/scaler_lr.pkl')

# Example new user data
new_users = pd.DataFrame([
    {'followers_count': 60, 'following_count': 1200, 'post_count': 4000,
     'account_age_days': 150, 'has_profile_picture':0, 'has_bio':0, 'avg_post_interval':0.5},
    {'followers_count': 600, 'following_count': 350, 'post_count': 900,
     'account_age_days': 1300, 'has_profile_picture':1, 'has_bio':1, 'avg_post_interval':15}
])

# Scale features
new_scaled = scaler.transform(new_users)

# Predict
predictions = model.predict(new_scaled)
print("Predictions (0=human, 1=bot):", predictions)

# Optional: predict probability
probabilities = model.predict_proba(new_scaled)
print("Prediction probabilities:\n", probabilities)
