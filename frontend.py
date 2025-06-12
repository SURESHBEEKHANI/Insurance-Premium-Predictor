import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Insurance Premium Predictor", layout="centered")

# Resize title and subtitle
st.markdown("<h1 style='text-align: center; font-size: 36px;'>Insurance Premium Category Predictor</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 20px;'>Enter your details below to predict your insurance premium category:</h3>", unsafe_allow_html=True)

# Session state to track login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Sidebar for Authentication
with st.sidebar:
    st.markdown("## Authentication")
    auth_mode = st.selectbox("Choose an option", ["Login", "Signup"], help="Select whether to log in or sign up.")

    if auth_mode == "Login":
        st.markdown("### Login")
        login_username = st.text_input("Username", key="login_username", help="Enter your username.")
        login_password = st.text_input("Password", type="password", key="login_password", help="Enter your password.")
        if st.button("Login"):
            login_data = {"username": login_username, "password": login_password}
            try:
                with st.spinner("Logging in..."):
                    response = requests.post(API_URL + "/api/auth/login", json=login_data, timeout=10)
                    response.raise_for_status()
                    st.success("Login successful!")
                    st.session_state.logged_in = True  # Set login status to True
            except requests.exceptions.HTTPError as e:
                st.error(f"Login failed: {response.json().get('detail', str(e))}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")

    elif auth_mode == "Signup":
        st.markdown("### Signup")
        signup_username = st.text_input("Signup Username", key="signup_username", help="Enter a unique username.")
        signup_password = st.text_input("Signup Password", type="password", key="signup_password", help="Enter a secure password.")
        if st.button("Signup"):
            signup_data = {"username": signup_username, "password": signup_password}
            try:
                with st.spinner("Creating account..."):
                    response = requests.post(API_URL + "/api/auth/signup", json=signup_data, timeout=10)
                    response.raise_for_status()
                    st.success("Account created successfully! You can now log in.")
            except requests.exceptions.HTTPError as e:
                st.error(f"Signup failed: {response.json().get('detail', str(e))}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")

# Show Prediction Section only if logged in
if st.session_state.logged_in:
    # Display all input fields in a single column
    age = st.number_input("Age", min_value=1, max_value=119, value=30, help="Enter your age in years.")
    weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0, help="Enter your weight in kilograms.")
    height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7, help="Enter your height in meters.")
    income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0, help="Enter your annual income in lakhs per annum.")
    smoker = st.selectbox("Are you a smoker?", options=["Yes", "No"], help="Select 'Yes' if you are a smoker, otherwise 'No'.")
    city = st.text_input("City", value="Mumbai", help="Enter the city you reside in.")
    occupation = st.selectbox(
        "Occupation",
        ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'],
        help="Select your occupation from the dropdown."
    )

    # Submit button for Prediction
    if st.button("Predict Premium Category"):
        input_data = {
            "age": age,
            "weight": weight,
            "height": height,
            "income_lpa": income_lpa,
            "smoker": smoker.lower() == "yes",
            "city": city,
            "occupation": occupation
        }

        try:
            with st.spinner("Predicting..."):
                # Increased timeout to 30 seconds
                response = requests.post(API_URL + "/api/predict", json=input_data, timeout=30)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

                result = response.json()
                if "response" in result:
                    prediction = result["response"]
                    st.success(f"Predicted Insurance Premium Category: **{prediction['predicted_category']}**")
                    st.markdown(f"**Confidence:** {prediction['confidence']:.2f}")
                    st.markdown("### Class Probabilities:")
                    st.json(prediction["class_probabilities"])
                else:
                    st.error("Unexpected response format from the API.")
                    st.json(result)

        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the FastAPI server. Please ensure it is running.")
        except requests.exceptions.Timeout:
            st.error("⏳ The request timed out. Please try again later.")
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ An error occurred: {e}")
else:
    st.warning("Please log in to access the prediction feature.")
