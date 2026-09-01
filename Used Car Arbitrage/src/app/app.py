'''
def load_model():
    return joblib.load("models/arbitrage_model.pkl")

yeh command us case mai kaam karegi jb terminal Used Car Arbitrage folder mai open hoga and hum run use 
"streamlit run src/app/app.py" se kare    
'''

import streamlit as st
import joblib
import pandas as pd
import os
from datetime import datetime

@st.cache_resource
def load_model():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "..", "..", "models", "arbitrage_model.pkl")
    return joblib.load(model_path)

st.set_page_config(page_title="Arbitrage Engine", page_icon=" ", layout="centered")

try:
    model = load_model()
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

st.title("Used Car Arbitrage Engine")
st.markdown('''
Find Mispriced deals in the Market.
''')
st.divider()

col1, col2 = st.columns(2)

current_year = datetime.now().year

with col1:
    brand = st.text_input("Brand", placeholder="eg. Hyundai, Maruti, Honda").strip().title()
    model_name = st.text_input("Model", placeholder="eg. Creta, Swift, City").strip().title()
    year = st.number_input("Manufacturing Year", min_value=2000, max_value=current_year, value=2019, step=1)

with col2:
    kilometers = st.number_input("Kilometers Driven", min_value=0, max_value=500000, value=45000, step=1000)
    Fuel_Type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

st.divider()
if st.button("Evaluate Listing", type="primary", use_container_width=True):
    if not brand or not model_name:
        st.warning("Please provide both Brand and Model name to evaluate.")
    else:
        with st.spinner("Analyzing market patterns..."):
            try:
                car_age = max(0, current_year - year)
                km_per_year = kilometers / (car_age + 1)
                make_model = f"{brand}_{model_name}"

                input_data = pd.DataFrame([{
                    "Fuel_Type": Fuel_Type,
                    "Transmission": transmission,
                    "Clean_Kilometers": kilometers,
                    "Brand": brand,
                    "Model": model_name,
                    "Car_Age": car_age,
                    "Km_per_Year": km_per_year,
                    "Make_Model": make_model
                }])

                prediction = model.predict(input_data)[0]
                predicted_price = int(prediction)

                st.success("Valuation complete")
                st.metric(label="Estimated Fair Market Value", value=f"₹{predicted_price:,}")
                st.info("**Arbitrage Tip:** Compare this fair market value against the seller's asking price to identify potential arbitrage opportunities.")
                
            except Exception as e:
                st.error(f"Model Rejection : {str(e)}")
