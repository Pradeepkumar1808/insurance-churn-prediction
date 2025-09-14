# Insurance Churn Prediction

## Project Overview
This project aims to predict customer churn in the insurance sector using machine learning. It leverages structured customer profile data, policy history, and claim behavior to identify customers likely to leave the service.

The project includes:  
- **Machine Learning Model**: A trained model (`model_pipeline.joblib`) using scikit-learn.  
- **Backend API**: FastAPI to handle CSV uploads and return churn predictions.  
- **Frontend**: React-based interface to upload customer data, visualize predictions, and display performance metrics.

## Features
- Predicts churn probability for each customer in a CSV file.
- Provides interactive visualizations of prediction results.
- Designed with a user-friendly interface for non-technical users.

## Technologies Used
- Python (scikit-learn, pandas, joblib, FastAPI)
- React.js (frontend)
- Uvicorn (ASGI server)
- CSV data handling for predictions

## Folder Structure
insurance_churn_prediction/
├── .venv/ # Virtual environment
├── backend/
│ ├── app/
│ │ ├── main.py # FastAPI application
│ │ ├── model_pipeline.joblib # Trained model
│ │ └── requirements.txt
├── frontend/
│ └── src/ # React frontend source
├── generate_data.py # Synthetic CSV generator
├── synthetic_insurance_claims.csv
├── train_model.py # Script to train ML model
└── README.md


## How to Run
### Backend
1. Activate virtual environment:
   ```bash
   source .venv/bin/activate
Install requirements:

pip install -r backend/app/requirements.txt


Start FastAPI server:

python -m uvicorn app.main:app --reload


Access API at: http://127.0.0.1:8000

Frontend

Navigate to frontend directory:

cd frontend


Install dependencies:

npm install


Start React app:

npm start


Open browser at: http://localhost:3000

Usage

Upload a CSV file with customer data.

The backend API will return churn predictions.

Results and performance metrics are visualized in the frontend.

Performance Metrics

Accuracy: 82%

ROC AUC: 0.615


