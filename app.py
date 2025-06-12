from fastapi import FastAPI
from routes.home import router as home_router
from routes.predict import router as predict_router
from routes.auth import router as auth_router
from fastapi.staticfiles import StaticFiles
from database.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Insurance Premium Prediction API with Auth")

# Include routers
app.include_router(home_router, prefix="/api", tags=["General"])
app.include_router(predict_router, prefix="/api", tags=["Prediction"])
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])



def main():
    print("Hello from insurance-premium-predictor!")


if __name__ == "__main__":
    main()
