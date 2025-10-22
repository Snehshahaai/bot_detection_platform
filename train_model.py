import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path

np.random.seed(42)
n_samples = 1000
humans = pd.DataFrame({
    'followers_count': np.random.normal(500, 200, n_samples//2).clip(0),
    'following_count': np.random.normal(300, 100, n_samples//2).clip(0),
    'post_count': np.random.normal(800, 400, n_samples//2).clip(0),
    'account_age_days': np.random.normal(1200, 500, n_samples//2).clip(1),
    'has_profile_picture': 1,
    'has_bio': 1,
    'avg_post_interval': np.random.normal(12, 5, n_samples//2).clip(1),
    'is_bot': 0
})

bots = pd.DataFrame({
    'followers_count': np.random.normal(1900, 30, n_samples//2).clip(0),
    'following_count': np.random.normal(1000, 300, n_samples//2).clip(0),
    'post_count': np.random.normal(5000, 2000, n_samples//2).clip(0),
    'account_age_days': np.random.normal(200, 100, n_samples//2).clip(1),
    'has_profile_picture': np.random.choice([0, 1], n_samples//2, p=[0.7, 0.3]),
    'has_bio': np.random.choice([0, 1], n_samples//2, p=[0.6, 0.4]),
    'avg_post_interval': np.random.normal(1, 0.5, n_samples//2).clip(0.1),
    'is_bot': 1
})


data = pd.concat([humans, bots], ignore_index=True)


X = data.drop('is_bot', axis=1)
y = data['is_bot']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))


# Ensure models directory exists at repo root (same folder as this script)
models_dir = Path(__file__).resolve().parent / "models"
models_dir.mkdir(parents=True, exist_ok=True)
print("Saving artifacts to:", models_dir)

sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
conf_path = models_dir / "confusion_matrix.png"
plt.savefig(conf_path)
plt.close()

coefficients = pd.Series(model.coef_[0], index=X.columns)
coefficients.sort_values().plot(kind='barh', figsize=(8,5))
# Save model and scaler into the determined models directory
models_dir = Path(__file__).resolve().parent / "models"
models_dir.mkdir(parents=True, exist_ok=True)
print("Saving artifacts to:", models_dir)

# Save model and scaler into the determined models directory
joblib.dump(model, models_dir / 'bot_model_lr.pkl')
joblib.dump(scaler, models_dir / 'scaler_lr.pkl')
print("Model, scaler and plots saved in:", models_dir)
