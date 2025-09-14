# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# Load data
df = pd.read_csv("synthetic_insurance_claims.csv")
print("✅ Data loaded, shape:", df.shape)

# Split features and target
X = df.drop(columns=["customer_id","churn"])
y = df["churn"]

# Define preprocessing
numeric_features = ["age","tenure","num_claims","claim_amount_total","premium","previous_renewals","satisfaction_score"]
categorical_features = ["gender","policy_type","payment_method","region","has_complaint"]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numeric_features),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features)
])

# Pipeline with RandomForest
pipeline = Pipeline([
    ("pre", preprocessor),
    ("clf", RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42,
        class_weight="balanced"  # <-- add this
    ))
])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
pipeline.fit(X_train, y_train)

# Evaluate
y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:,1]

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_proba))

# Save model
joblib.dump(pipeline, "backend/app/model_pipeline.joblib")
print("✅ Model saved as model_pipeline.joblib")
