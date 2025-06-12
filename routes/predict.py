# routes/predict.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from schema.user_input import UserInput  # Input data model
from schema.prediction_response import PredictionResponse  # Output data model
from model.predict import predict_output, model, MODEL_VERSION  # Model and predict function

# Create a new router instance
router = APIRouter()

# Human-readable home route (basic test or welcome message)
@router.get('/')
def home():
    return {'message': 'Insurance Premium Prediction API'}

# Health check route (machine-readable, for monitoring)
@router.get('/health')
def health_check():
    return {
        'status': 'OK',                  # Server is running
        'version': MODEL_VERSION,        # Model version
        'model_loaded': model is not None  # Check if model is loaded
    }

# Prediction route that takes input and returns prediction
@router.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):
    """
    Predict insurance premium based on user input.
    """

    # Convert Pydantic model to dictionary
    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:
        # Make prediction using model
        prediction = predict_output(user_input)

        # Return prediction as JSON
        return JSONResponse(status_code=200, content={'response': prediction})

    except Exception as e:
        # Return error message if something goes wrong
        return JSONResponse(status_code=500, content={"error": str(e)})
