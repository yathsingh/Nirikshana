import joblib
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "random_forest_model.pkl")

model = joblib.load(MODEL_PATH)

FEATURES = ["ph", "tds", "turbidity", "flow_rate"]

def predict_water_quality(river, location, ph, tds, turbidity, flow_rate):
 
    X = pd.DataFrame([[ph, tds, turbidity, flow_rate]], columns=FEATURES)

    pred_class = model.predict(X)[0]
    proba = model.predict_proba(X)[0][pred_class]

    label = "safe" if pred_class == 0 else "unsafe"

    return {
        "river": river,
        "location": location,
        "ph": round(ph, 2),
        "tds": round(tds, 1),
        "turbidity": round(turbidity, 2),
        "flow_rate": round(flow_rate, 2),
        "prediction": label,
        "confidence": round(float(proba), 3)
    }
