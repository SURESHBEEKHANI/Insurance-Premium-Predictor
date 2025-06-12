# routes/predict.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import pickle
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse 
from model.predict import predict_output

# Create router
router = APIRouter()

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

