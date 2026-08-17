from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="Used Car Arbitrage API")

model = joblib.load(r"C:\Programming\Machine Learning\Used Car Price Intelligence\Used Car Arbitrage\models\arbitrage_model.pkl")

class CarFeatures(BaseModel):
    Year : int
    Clean_Kilometers : int
    Brand : str
    Model : str
    Fuel_type : str
    Transmission : str

@app.post("/predict")

def predict_price(car : CarFeatures):

    input_data = pd.DataFrame([{
        "Year":car.Year,
        "Clean_Kilometers" : car.Clean_Kilometers,
        "Brand" : car.Brand,
        "Model" : car.Model,
        "Fuel_Type" : car.Fuel_type,
        "Transmission" : car.Transmission
    }])

    prediction = model.predict(input_data)[0]

    return {"Predicted Price": int(prediction)}

@app.get("/")

def read_root():
    return {"Message":"Arbitrage Engine API is live!"}
