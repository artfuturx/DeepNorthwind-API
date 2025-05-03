from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from tensorflow import keras

app = FastAPI()

MODEL_PATHS = {
    "reorder": {
        "model": "saved_models/customer_reorder/reorder_model.h5",
        "scaler": "saved_models/customer_reorder/scaler.pkl",
        "features": ['total_orders', 'total_spent', 'avg_order_value']
    },
    "return_risk": {
        "model": "saved_models/return_risk/return_risk_model.h5",
        "scaler": "saved_models/return_risk/scaler.pkl",
        "features": ['quantity', 'unit_price', 'discount', 'total_amount', 'discount_percent']
    },
    "purchase_potential": {
    "model": "saved_models/product_purchase/product_purchase_model.h5",
    "scaler": "saved_models/product_purchase/scaler.pkl",
    "features": [
        "total_orders_x", "total_spent_x", "avg_order_value",
        "order_count_in_category_Beverages", "order_count_in_category_Condiments", "order_count_in_category_Confections", "order_count_in_category_Dairy Products", "order_count_in_category_Grains/Cereals", "order_count_in_category_Meat/Poultry", "order_count_in_category_Produce", "order_count_in_category_Seafood",
        "total_spent_in_category_Beverages", "total_spent_in_category_Condiments", "total_spent_in_category_Confections", "total_spent_in_category_Dairy Products", "total_spent_in_category_Grains/Cereals", "total_spent_in_category_Meat/Poultry", "total_spent_in_category_Produce", "total_spent_in_category_Seafood",
        "total_spent_y", "total_orders_y"
    ]
}
}

def load_model_and_scaler(model_key):
    model = keras.models.load_model(MODEL_PATHS[model_key]["model"])
    scaler = joblib.load(MODEL_PATHS[model_key]["scaler"])
    features = MODEL_PATHS[model_key]["features"]
    return model, scaler, features

class ReorderInput(BaseModel):
    total_orders: float
    total_spent: float
    avg_order_value: float

class ReturnRiskInput(BaseModel):
    quantity: float
    unit_price: float
    discount: float
    total_amount: float
    discount_percent: float

class PurchasePotentialInput(BaseModel):
    spent_beverages: float = 0
    spent_confections: float = 0
    spent_produce: float = 0

@app.post("/predict_reorder")
def predict_reorder(input: ReorderInput):
    model, scaler, features = load_model_and_scaler("reorder")
    X = np.array([[getattr(input, f, 0) for f in features]])
    X_scaled = scaler.transform(X)
    prob = float(model.predict(X_scaled)[0][0])
    return {"reorder_probability": prob}

@app.post("/predict_return_risk")
def predict_return_risk(input: ReturnRiskInput):
    model, scaler, features = load_model_and_scaler("return_risk")
    X = np.array([[getattr(input, f, 0) for f in features]])
    X_scaled = scaler.transform(X)
    prob = float(model.predict(X_scaled)[0][0])
    return {"return_risk_probability": prob}

@app.post("/predict_purchase_potential")
def predict_purchase_potential(input: PurchasePotentialInput):
    model, scaler, features = load_model_and_scaler("purchase_potential")
    print("Beklenen features:", features)
    print("Gelen veri:", input)
    X = np.array([[getattr(input, f, 0) for f in features]])
    X_scaled = scaler.transform(X)
    prob = float(model.predict(X_scaled)[0][0])
    return {"purchase_potential_probability": prob}
