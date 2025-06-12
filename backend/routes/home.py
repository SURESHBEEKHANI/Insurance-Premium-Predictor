# routes/home.py
from fastapi import APIRouter
from model.predict import model, MODEL_VERSION

# Create router
router = APIRouter()

@router.get("/")
def home():
    """
    Human-readable welcome endpoint.
    """
    return {"message": "Insurance Premium Prediction API"}

@router.get("/health")
def health_check():
    """
    Machine-readable health check endpoint.
    """
    return {
        "status": "OK",
        "version": MODEL_VERSION,
        "model_loaded": model is not None
    }
