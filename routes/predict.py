# routes/predict.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import pickle
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output

# Create router
router = APIRouter()

# Load the ML model
try:
    with open("model/model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    raise RuntimeError("Model file not found. Ensure 'model/model.pkl' exists.")

# Pydantic model for input validation
class PredictionInput(BaseModel):
    age: int
    weight: float
    height: float
    income_lpa: float
    smoker: bool
    city: str
    occupation: str

@router.post("/predict", response_model=PredictionResponse)
def predict_premium(data: UserInput):
    """
    Predict insurance premium based on user input.
    """
    user_input = {
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }

    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content={"response": prediction})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/predict")
def predict(data: PredictionInput):
    try:
        # Calculate BMI
        bmi = data.weight / (data.height ** 2)

        # Prepare input for the model
        input_data = pd.DataFrame([{
            "bmi": bmi,
            "age": data.age,
            "income_lpa": data.income_lpa,
            "smoker": data.smoker,
            "city": data.city,
            "occupation": data.occupation
        }])

        # Make prediction
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]

        return {
            "predicted_category": prediction,
            "confidence": max(probabilities),
            "class_probabilities": {
                "Low": probabilities[0],
                "Medium": probabilities[1],
                "High": probabilities[2]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
