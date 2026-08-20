from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="Used Car Arbitrage API")

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir,"..","..","models","arbitrage_model.pkl")

if not os.path.exists(model_path):
    model_path = 'models/arbitrage_model.pkl'

model = joblib.load(model_path)

class CarFeatures(BaseModel):
    Year : int
    Clean_Kilometers : int
    Brand : str
    Model : str
    Fuel_type : str
    Transmission : str

@app.post("/predict")

def predict_price(car : CarFeatures):
    try:

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
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction Failed:{str(e)}")

@app.get("/")

def read_root():
    return {"Message":"Arbitrage Engine API is live!"}
