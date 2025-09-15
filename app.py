import os
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Any, Dict

from backend.db import SessionLocal, init_db, WaterData, Alert  
from backend.predict import predict_water_quality

init_db()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "backend", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "backend", "static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

app = FastAPI(title="Nirikshana Water Monitoring API")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class WaterInput(BaseModel):
    device_id: str | None = None
    river: str
    location: str
    ph: float
    tds: float
    turbidity: float
    flow_rate: float


@app.get("/", response_class=JSONResponse)
def read_root():
    return {"message": "Nirikshana API active"}


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.post("/predict")
def predict(data: WaterInput, db: Session = Depends(get_db)):
    """
    Runs the prediction logic, persists a WaterData row, and returns the result.
    The prediction function can return either:
      - a dict with keys: river, location, ph, tds, turbidity, flow_rate, prediction, confidence
      - OR a tuple (prediction_label, confidence)
    This code handles both styles to be robust.
    """

    pred = predict_water_quality(
        data.device_id or "",
        data.river, data.location,
        data.ph, data.tds, data.turbidity, data.flow_rate
    )

    if isinstance(pred, dict):
        result: Dict[str, Any] = pred
    elif isinstance(pred, tuple) and len(pred) >= 2:
        result = {
            "river": data.river,
            "location": data.location,
            "ph": data.ph,
            "tds": data.tds,
            "turbidity": data.turbidity,
            "flow_rate": data.flow_rate,
            "prediction": pred[0],
            "confidence": float(pred[1])
        }
    else:
        result = {
            "river": data.river,
            "location": data.location,
            "ph": data.ph,
            "tds": data.tds,
            "turbidity": data.turbidity,
            "flow_rate": data.flow_rate,
            "prediction": str(pred),
            "confidence": 0.0
        }

    db_entry = WaterData(
        device_id=data.device_id or "",
        river=result.get("river", data.river),
        location=result.get("location", data.location),
        ph=float(result.get("ph", data.ph)),
        tds=float(result.get("tds", data.tds)),
        turbidity=float(result.get("turbidity", data.turbidity)),
        flow_rate=float(result.get("flow_rate", data.flow_rate)),
        prediction=result.get("prediction"),
        confidence=float(result.get("confidence", 0.0))
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    return JSONResponse(content={"prediction": db_entry.prediction, "confidence": db_entry.confidence})


@app.get("/data")
def get_data(limit: int = 50, db: Session = Depends(get_db)):
    """
    Return most recent `limit` WaterData records as JSON.
    """
    rows = db.query(WaterData).order_by(WaterData.timestamp.desc()).limit(limit).all()
    out = []
    for r in rows:
        out.append({
            "id": r.id,
            "device_id": r.device_id,
            "river": r.river,
            "location": r.location,
            "ph": float(r.ph) if r.ph is not None else None,
            "tds": float(r.tds) if r.tds is not None else None,
            "turbidity": float(r.turbidity) if r.turbidity is not None else None,
            "flow_rate": float(r.flow_rate) if r.flow_rate is not None else None,
            "prediction": r.prediction,
            "confidence": float(r.confidence) if r.confidence is not None else None,
            "timestamp": r.timestamp.isoformat() if r.timestamp is not None else None
        })
    return JSONResponse(content=out)


@app.get("/history")
def get_history(limit: int = 20, db: Session = Depends(get_db)):
    rows = db.query(WaterData).order_by(WaterData.timestamp.desc()).limit(limit).all()

    return JSONResponse(content=[{
        "id": r.id,
        "device_id": r.device_id,
        "river": r.river,
        "location": r.location,
        "ph": r.ph,
        "tds": r.tds,
        "turbidity": r.turbidity,
        "flow_rate": r.flow_rate,
        "prediction": r.prediction,
        "confidence": r.confidence,
        "timestamp": r.timestamp.isoformat() if r.timestamp else None
    } for r in rows])


@app.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    total = db.query(func.count(WaterData.id)).scalar()
    safe_count = db.query(func.count(WaterData.id)).filter(WaterData.prediction == "safe").scalar()
    unsafe_count = db.query(func.count(WaterData.id)).filter(WaterData.prediction == "unsafe").scalar()

    river_stats = db.query(
        WaterData.river,
        WaterData.location,
        func.count(WaterData.id).label("count"),
        func.avg(WaterData.ph).label("avg_ph"),
        func.avg(WaterData.tds).label("avg_tds"),
        func.avg(WaterData.turbidity).label("avg_turbidity"),
        func.avg(WaterData.flow_rate).label("avg_flow"),
        func.sum(func.case([(WaterData.prediction == "unsafe", 1)], else_=0)).label("unsafe_count")
    ).group_by(WaterData.river, WaterData.location).all()

    return JSONResponse(content={
        "total_records": int(total or 0),
        "safe": int(safe_count or 0),
        "unsafe": int(unsafe_count or 0),
        "by_location": [
            {
                "river": r.river,
                "location": r.location,
                "count": int(r.count or 0),
                "avg_ph": round(r.avg_ph, 2) if r.avg_ph is not None else None,
                "avg_tds": round(r.avg_tds, 2) if r.avg_tds is not None else None,
                "avg_turbidity": round(r.avg_turbidity, 2) if r.avg_turbidity is not None else None,
                "avg_flow": round(r.avg_flow, 2) if r.avg_flow is not None else None,
                "unsafe_count": int(r.unsafe_count or 0)
            } for r in river_stats
        ]
    })
