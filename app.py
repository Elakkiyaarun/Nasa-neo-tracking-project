import streamlit as st
import numpy as np
import pickle


# Load the trained model
with open('C:/Users/admin/guvi 2025/project 3/best_model.pkl', 'rb') as f:
    model = pickle.load(f)

st.title("🚕 Urban Taxi Fare Predictor")

# --- Input fields from dataset ---

passenger_count = st.number_input("Passenger Count", min_value=1, max_value=6, value=1)

payment_type = st.selectbox("Payment Type", ['Credit Card', 'Cash', 'Dispute', 'Unknown'])
payment_mapping = {
    'Credit Card': 1,
    'Cash': 2,
    'No Charge': 3,
    'Dispute': 4,
    'Unknown': 5
}
payment_code = payment_mapping[payment_type]

distance_km = st.number_input("Trip Distance (km)", min_value=0.0, format="%.2f")

pickup_day = st.selectbox("Pickup Day", ['Tuesday',])

# Map days to numbers
day_mapping = {
     'Tuesday': 0
}
pickup_day_encoded = day_mapping[pickup_day]


is_night = st.selectbox("Is Night?", ['Yes', 'No'])
is_night_code = 1 if is_night == 'Yes' else 0

trip_duration_min = st.number_input("Trip Duration (in minutes)", min_value=0.0, format="%.2f")

# --- Prediction ---
if st.button("Predict Fare 💰"):
    input_data = np.array([[passenger_count, payment_code, distance_km,
                          pickup_day_encoded, is_night_code, trip_duration_min]])
    
    prediction = model.predict(input_data)[0]
    st.success(f"🚖 Estimated Fare Amount: ${prediction:.2f}")
