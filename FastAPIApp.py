from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI(title="Obesity Classification API")

# Load model pipeline
with open("C:/Users/ben/Documents/Programming/Python/Python Binus/Model Deployment/UAS/xgb_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

# Skema input SESUAI dengan data training ObesityDataSet2.csv
class ObesityInput(BaseModel):
    Gender: str
    Age: float
    Height_in_m: float
    Weight_in_kg: float
    family_history_with_overweight: str
    High_calorie_diet: str
    Frequency_vegetable_consumption: float
    main_course_per_day: float
    Food_consumption_interval: str
    Smoking: str
    Daily_water_intake: float
    Count_Calorie_intake: str
    Physical_activity_frequency: float
    Time_spent_on_tech: float
    Alcohol_Consumption_Frequency: str
    Main_Transportation: str

# Urutan kolom input sesuai pipeline
expected_columns = [
    'Gender', 'Age', 'Height_in_m', 'Weight_in_kg',
    'family_history_with_overweight', 'High_calorie_diet',
    'Frequency_vegetable_consumption', 'main_course_per_day',
    'Food_consumption_interval', 'Smoking', 'Daily_water_intake',
    'Count_Calorie_intake', 'Physical_activity_frequency',
    'Time_spent_on_tech', 'Alcohol_Consumption_Frequency',
    'Main_Transportation'
]

@app.get("/")
def root():
    return {"message": "Obesity Prediction API is running."}

@app.post("/predict")
def predict(data: ObesityInput):
    try:
        input_df = pd.DataFrame([data.dict()])
        input_df = input_df[expected_columns]

        prediction = model.predict(input_df)[0]
        
        class_mapping = {
            0: "Insufficient_Weight",
            1: "Normal_Weight",
            2: "Overweight_Level_I",
            3: "Overweight_Level_II",
            4: "Obesity_Type_I",
            5: "Obesity_Type_II",
            6: "Obesity_Type_III"
        }

        label = class_mapping.get(int(prediction), "Unknown")

        return {
            "prediction_class": int(prediction),
            "prediction_label": label
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
