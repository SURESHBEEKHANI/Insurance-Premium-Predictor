from fastapi import FastAPI
from routes.home import router as home_router
from routes.predict import router as predict_router
from routes.auth import router as auth_router
from fastapi.staticfiles import StaticFiles
from database.database import Base, engine
from model.predict import model, predict_output, MODEL_VERSION
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse  # Ensure this is correctly imported
from fastapi.responses import JSONResponse
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Insurance Premium Prediction API with Auth")

# Include routers
app.include_router(home_router, prefix="/api", tags=["General"])
app.include_router(predict_router, prefix="/api", tags=["Prediction"])
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])


# Machine-readable health check
@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }

@app.on_event("startup")
def load_model():
    """
    Preload the model during app startup to avoid delays during prediction.
    """
    global model
    if model is None:
        raise RuntimeError("Model failed to load. Ensure 'model/model.pkl' exists.")

@app.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content={'response': prediction})
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))

if __name__ == "__main__":
    """
    Run the FastAPI app using uvicorn.
    """
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
# To run the app, use the command: uvicorn app:app --reload
