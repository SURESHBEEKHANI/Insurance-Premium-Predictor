# main.py
from fastapi import FastAPI
from routes.predict import router as predict_router
import uvicorn

app = FastAPI(
    title="Insurance Premium Prediction API",
    version="1.0.0"
)

# Register the router
app.include_router(predict_router, prefix="/api", tags=["Prediction"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
