import streamlit as st
import requests

st.set_page_config(page_title="Arbitrage Engine",page_icon=" ",layout="centered")
st.title("Used Car Arbitrage Engine")
st.markdown('''
Find Mispriced deals in the Market.
''')
st.divider()

col1, col2 = st.columns(2)

with col1:
    brand = st.text_input("Brand",placeholder="eg. Hyundai, Maruti, Honda").title()
    model_name = st.text_input("Model",placeholder="eg. Creta, Swift, City").title()
    year = st.number_input("Manufacturing Year",min_value=2000,max_value=2025,value=2019,step=1)

with col2:
    kilometers = st.number_input("Kilometers Driven", min_value=0,max_value=500000,value=45000, step = 1000)
    Fuel_Type = st.selectbox("Fuel Type",["Petrol","Diesel","CNG"])
    transmission = st.selectbox("Transmission",["Manual","Automatic"])

st.divider()
if st.button("Evaluate Listing",type="primary",use_container_width=True):
    payload = {
        "Year":year,
        "Clean_Kilometers":kilometers,
        "Brand":brand,
        "Model":model_name,
        "Fuel_Type":Fuel_Type,
        "Transmission":transmission
    }

    with st.spinner("Analyzing market patterns..."):
        try:
            response = requests.post("http://127.0.0.1:8000/predict",json=payload)

            if response.status_code == 200:
                predicted_price = response.json()['Predicted Price']

                st.success("Valuation complete")
                st.metric(label="Estimated Fair Market Value",value=f"{predicted_price:,}")
                st.info("**Arbitrage Tip:** ")

            else:
                error_detail = response.json().get('detail',response.text)
                st.error(f"Model Rejection : {error_detail}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to backend API. Ensure it is running on port 8000")