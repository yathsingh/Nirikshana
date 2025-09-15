import random
from datetime import datetime, timedelta

from backend.db import SessionLocal, init_db, WaterData, Alert
from backend.predict import predict_water_quality

GANGA_LOCATIONS = {
    "Rishikesh": ["Triveni Ghat", "Lakshman Jhula"],
    "Haridwar": ["Har Ki Pauri", "Kankhal"],
    "Kanpur": ["Jajmau", "Siddhnath Ghat"],
    "Varanasi": ["Assi Ghat", "Dashashwamedh Ghat", "Manikarnika Ghat"],
    "Patna": ["Gandhi Ghat", "Kumhrar"],
    "Kolkata": ["Babughat", "Dakshineswar"]
}


def seed_water_data(num_records: int = 150):
    """Seed mock Ganga water data using ML prediction model."""
    db = SessionLocal()
    init_db()

    db.query(Alert).delete()
    db.query(WaterData).delete()

    now = datetime.utcnow()
    inserted_alerts = 0

    for i in range(num_records):
        city = random.choice(list(GANGA_LOCATIONS.keys()))
        location = random.choice(GANGA_LOCATIONS[city])

        ph = round(random.uniform(6.5, 8.5), 2)
        tds = round(random.uniform(100, 600), 1)
        turbidity = round(random.uniform(1, 200), 2)
        flow_rate = round(random.uniform(0.2, 5.0), 2)

        result = predict_water_quality(
            river="Ganga",
            location=f"{city} - {location}",
            ph=ph,
            tds=tds,
            turbidity=turbidity,
            flow_rate=flow_rate
        )

        device_id = f"ganga-{city.lower()}-{random.randint(100,999)}"

        row = WaterData(
            device_id=device_id,
            river=result["river"],
            location=result["location"],
            ph=result["ph"],
            tds=result["tds"],
            turbidity=result["turbidity"],
            flow_rate=result["flow_rate"],
            prediction=result["prediction"],
            confidence=result["confidence"],
            timestamp=now - timedelta(minutes=i)
        )
        db.add(row)

        if result["prediction"] == "unsafe":
            alert = Alert(
                device_id=device_id,
                river=result["river"],
                location=result["location"],
                alert_type="water_quality",
                message=f"Unsafe water quality detected at {result['location']}",
                severity="high" if result["confidence"] > 0.8 else "medium",
                created_at=row.timestamp
            )
            db.add(alert)
            inserted_alerts += 1

    db.commit()
    db.close()
    print(f"Inserted {num_records} WaterData rows.")
    print(f"Generated {inserted_alerts} alerts for unsafe water.")


if __name__ == "__main__":
    seed_water_data(200)
