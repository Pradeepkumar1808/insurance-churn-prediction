from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import io

app = FastAPI()

# Allow React frontend to communicate
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model once
model = joblib.load("app/model_pipeline.joblib")

@app.get("/")
def root():
    return {"message": "Insurance churn prediction API is running."}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        # Predict
        predictions = model.predict(df)
        df["churn_prediction"] = predictions.tolist()

        # Optional: simple summary
        summary = df["churn_prediction"].value_counts().to_dict()
        return {"predictions": df.to_dict(orient="records"), "summary": summary}

    except Exception as e:
        return {"error": str(e)}
