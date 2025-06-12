# Insurance Premium Predictor

This project predicts the insurance premium category for users based on their personal and lifestyle details. It uses a machine learning model served via a FastAPI backend and provides a user-friendly interface using Streamlit or Gradio.

## Features

- **FastAPI Backend**: Serves the machine learning model for predictions.
- **Streamlit Frontend**: Provides an interactive UI for users to input their details and view predictions. The title and subtitle are resized for better readability.
- **Authentication**: Includes signup and login functionality for user management.
- **Gradio Interface**: Supports deployment on Hugging Face Spaces.
- **Dockerized Setup**: Easily deployable using Docker.

## Purpose

The Insurance Premium Predictor helps users estimate their insurance premium category (e.g., Low, Medium, High) based on factors such as age, weight, height, income, smoking habits, city, and occupation. This tool is designed to provide insights into premium categories and assist in financial planning.

## Authentication Endpoints

- **`POST /api/auth/signup`**: Allows users to create an account.
- **`POST /api/auth/login`**: Allows users to log in with their credentials.

### Example Signup Request

```json
{
  "username": "testuser",
  "password": "securepassword"
}
```

### Example Login Request

```json
{
  "username": "testuser",
  "password": "securepassword"
}
```

### Example Login Response

```json
{
  "message": "Login successful"
}
```

## How to Run Locally

### Prerequisites

- Python 3.9 or later
- Docker (optional, for containerized deployment)

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd "d:\Insurance Premium Predictor"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI backend:
   ```bash
   uvicorn app:app --reload
   ```

4. Run the Streamlit frontend:
   ```bash
   streamlit run frontend.py
   ```

5. Access the application:
   - FastAPI API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - Streamlit UI: [http://localhost:8501](http://localhost:8501)

## How to Run with Docker

1. Build the Docker image:
   ```bash
   docker build -t insurance-premium-predictor .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 -p 8501:8501 insurance-premium-predictor
   ```

3. Access the application:
   - FastAPI API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - Streamlit UI: [http://127.0.0.1:8501](http://127.0.0.1:8501)

## Deployment on Hugging Face Spaces

This project is configured to run on Hugging Face Spaces using Gradio. To deploy:

1. Create a new Space on Hugging Face.
2. Upload the project files.
3. The Gradio interface will be available at the Space URL.

## API Endpoints

- **`GET /`**: Returns a welcome message.
- **`GET /health`**: Returns the health status of the API.
- **`POST /predict`**: Accepts user input and returns the predicted insurance premium category.

## Input Fields

- **Age**: User's age (1-119 years).
- **Weight**: User's weight in kilograms.
- **Height**: User's height in meters.
- **Annual Income (LPA)**: User's annual income in lakhs per annum.
- **Smoker**: Whether the user is a smoker (Yes/No).
- **City**: The city the user resides in.
- **Occupation**: User's occupation (e.g., private job, student, etc.).

## Example API Request

```json
{
  "age": 30,
  "weight": 65.0,
  "height": 1.7,
  "income_lpa": 10.0,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "private_job"
}
```

## Example API Response

```json
{
  "response": {
    "predicted_category": "Low",
    "confidence": 0.47,
    "class_probabilities": {
      "High": 0.08,
      "Low": 0.47,
      "Medium": 0.45
    }
  }
}
```

## License

This project is licensed under the MIT License.
