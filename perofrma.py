import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# --- Paths ---
MODEL_PATH = 'backend/app/model_pipeline.joblib'
DATA_PATH = 'synthetic_insurance_claims.csv'  # replace with your test CSV

# --- Load model ---
model = joblib.load(MODEL_PATH)

# --- Load data ---
data = pd.read_csv(DATA_PATH)

# --- Features and target ---
# Replace 'churn' with your actual target column
TARGET_COLUMN = 'churn'
X = data.drop(columns=[TARGET_COLUMN, 'customer_id'])  # drop ID if present
y = data[TARGET_COLUMN]

# --- Predict ---
y_pred = model.predict(X)

# --- Accuracy ---
acc = accuracy_score(y, y_pred)
print(f"Accuracy: {acc:.4f}")

# --- Classification Report ---
print("\nClassification Report:")
print(classification_report(y, y_pred))

# --- Confusion Matrix ---
cm = confusion_matrix(y, y_pred)
plt.figure(figsize=(6,4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# --- Optional: Feature Importance ---
try:
    importances = model.named_steps['classifier'].feature_importances_
    feature_names = X.columns
    fi_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
    fi_df = fi_df.sort_values(by='Importance', ascending=False)

    plt.figure(figsize=(8,5))
    sns.barplot(x='Importance', y='Feature', data=fi_df)
    plt.title('Feature Importances')
    plt.show()
except:
    print("Feature importances not available for this model.")
