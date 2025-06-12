from fastapi import FastAPI
from routes.home import router as home_router
from routes.predict import router as predict_router
from routes.auth import router as auth_router
from database.database import engine, Base
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Insurance Premium Prediction API with Auth")

# Include routers
app.include_router(home_router, prefix="/api", tags=["General"])
app.include_router(predict_router, prefix="/api", tags=["Prediction"])
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])


if __name__ == "__main__":
    """
    Run the FastAPI app using uvicorn.
    """
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
# To run the app, use the command: uvicorn app:app --reload
