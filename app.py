# ============================================================
# CAR PRICE PREDICTION WEB APPLICATION
# ============================================================

import streamlit as st
import pandas as pd
import joblib


# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ------------------------------------------------------------
# Custom CSS
# ------------------------------------------------------------

st.markdown("""
<style>

/* Main application background */
.stApp {
    background-color: #f5f7fa;
}

/* Main container */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main heading */
.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #1f2937;
    margin-bottom: 5px;
}

/* Subtitle */
.main-subtitle {
    text-align: center;
    font-size: 17px;
    color: #6b7280;
    margin-bottom: 35px;
}

/* Section heading */
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #1f2937;
    margin-top: 10px;
    margin-bottom: 15px;
}

/* Card */
.info-card {
    background: white;
    border-radius: 16px;
    padding: 20px 25px;
    margin-bottom: 25px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.04);
}

/* Prediction result */
.prediction-card {
    background: linear-gradient(135deg, #111827, #374151);
    padding: 32px;
    border-radius: 18px;
    text-align: center;
    margin-top: 25px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
}

.prediction-label {
    color: #d1d5db;
    font-size: 16px;
    margin-bottom: 8px;
}

.prediction-price {
    color: white;
    font-size: 42px;
    font-weight: 800;
}

.prediction-note {
    color: #d1d5db;
    font-size: 13px;
    margin-top: 8px;
}

/* Streamlit button */
.stButton > button {
    width: 100%;
    height: 52px;
    border-radius: 10px;
    font-size: 17px;
    font-weight: 700;
}

/* Input fields */
div[data-baseweb="input"] {
    border-radius: 10px;
}

div[data-baseweb="select"] > div {
    border-radius: 10px;
}

/* Footer */
.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 13px;
    margin-top: 50px;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# Load Model
# ------------------------------------------------------------

@st.cache_resource
def load_model():
    return joblib.load("car_price_model.pkl")


try:
    model = load_model()
except Exception as e:
    st.error("Unable to load the prediction model.")
    st.exception(e)
    st.stop()


# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

st.markdown('<div class="main-title">Car Price Predictor</div>',unsafe_allow_html=True)

st.markdown(
    """
    <div class="main-subtitle">
        Get an estimated selling price for your vehicle using
        machine-learning based valuation.
    </div>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# Information Card
# ------------------------------------------------------------

st.markdown("""
<div class="info-card">
    <b>How it works</b><br><br>
    Enter the vehicle information below. Our machine-learning model
    will analyse the vehicle characteristics and estimate its
    expected selling price.
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# Vehicle Details
# ------------------------------------------------------------

st.markdown(
    '<div class="section-title">Vehicle Information</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2, gap="large")


# LEFT COLUMN
with col1:

    car_name = st.text_input(
        "Car Name",
        value="Regenesis Car",
        placeholder="e.g. Toyota Hilux"
    )

    brand = st.text_input(
        "Brand",
        value="Toyota",
        placeholder="e.g. Toyota"
    )

    car_model = st.text_input(
        "Model",
        value="Hilux",
        placeholder="e.g. Hilux"
    )

    vehicle_age = st.number_input(
        "Vehicle Age (Years)",
        min_value=0,
        max_value=50,
        value=5,
        step=1
    )

    km_driven = st.number_input(
        "Kilometres Driven",
        min_value=0,
        value=50000,
        step=1000,
        help="Total kilometres travelled by the vehicle."
    )

    seller_type = st.selectbox(
        "Seller Type",
        [
            "Individual",
            "Dealer",
            "Trustmark Dealer"
        ]
    )


# RIGHT COLUMN
with col2:

    fuel_type = st.selectbox(
        "Fuel Type",
        [
            "Petrol",
            "Diesel",
            "Electric"
        ]
    )

    transmission_type = st.selectbox(
        "Transmission",
        [
            "Manual",
            "Automatic"
        ]
    )

    mileage = st.number_input(
        "Mileage (km/l)",
        min_value=0.0,
        value=18.0,
        step=0.1
    )

    engine = st.number_input(
        "Engine Capacity (CC)",
        min_value=500.0,
        value=1200.0,
        step=50.0
    )

    max_power = st.number_input(
        "Maximum Power (BHP)",
        min_value=20.0,
        value=80.0,
        step=1.0
    )

    seats = st.number_input(
        "Number of Seats",
        min_value=2,
        max_value=15,
        value=5,
        step=1
    )


# ------------------------------------------------------------
# Divider
# ------------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

st.divider()


# ------------------------------------------------------------
# Vehicle Summary
# ------------------------------------------------------------

st.markdown(
    '<div class="section-title">📋 Vehicle Summary</div>',
    unsafe_allow_html=True
)

summary1, summary2, summary3, summary4 = st.columns(4)

summary1.metric(
    "Vehicle",
    f"{brand} {car_model}"
)

summary2.metric(
    "Age",
    f"{vehicle_age} years"
)

summary3.metric(
    "Mileage",
    f"{km_driven:,} km"
)

summary4.metric(
    "Transmission",
    transmission_type
)


st.markdown("<br>", unsafe_allow_html=True)


# ------------------------------------------------------------
# Prediction Button
# ------------------------------------------------------------

predict = st.button(
    "Predict Vehicle Price",
    type="primary",
    use_container_width=True
)


# ------------------------------------------------------------
# Prediction
# ------------------------------------------------------------

if predict:

    input_data = pd.DataFrame({
        "car_name": [car_name],
        "brand": [brand],
        "model": [car_model],
        "vehicle_age": [vehicle_age],
        "km_driven": [km_driven],
        "seller_type": [seller_type],
        "fuel_type": [fuel_type],
        "transmission_type": [transmission_type],
        "mileage": [mileage],
        "engine": [engine],
        "max_power": [max_power],
        "seats": [seats]
    })

    try:

        prediction = model.predict(input_data)[0]

        # ----------------------------------------------------
        # Prediction Result
        # ----------------------------------------------------

        st.markdown(
            f"""
<div class="prediction-card">
<div class="prediction-label">
Estimated Selling Price
</div>

<div class="prediction-price">
R {prediction:,.2f}
</div>

<div class="prediction-note">
Estimated using the trained machine-learning model
</div>
</div>
""",
            unsafe_allow_html=True
        )

        st.success(
            f"Prediction completed successfully for "
            f"{brand} {car_model}."
        )


        # ----------------------------------------------------
        # Prediction Details
        # ----------------------------------------------------

        with st.expander("🔎 View prediction details"):

            details = pd.DataFrame({
                "Vehicle Detail": [
                    "Car Name",
                    "Brand",
                    "Model",
                    "Vehicle Age",
                    "Kilometres Driven",
                    "Seller Type",
                    "Fuel Type",
                    "Transmission",
                    "Mileage",
                    "Engine",
                    "Maximum Power",
                    "Seats"
                ],

                "Value": [
                    car_name,
                    brand,
                    car_model,
                    f"{vehicle_age} years",
                    f"{km_driven:,} km",
                    seller_type,
                    fuel_type,
                    transmission_type,
                    f"{mileage} km/l",
                    f"{engine} CC",
                    f"{max_power} BHP",
                    seats
                ]
            })

            st.dataframe(
                details,
                use_container_width=True,
                hide_index=True
            )

    except Exception as e:

        st.error(
            "An error occurred while generating the prediction."
        )

        st.exception(e)


# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        Car Price Prediction System • Machine Learning Application
        <br>
        Built with Python, Scikit-Learn & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
