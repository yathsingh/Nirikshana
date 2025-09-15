from datetime import datetime, timedelta
import time
from backend.db import SessionLocal, init_db, WaterData, Alert
from seed import generate_record

def simulate_live(interval_seconds: int = 10):
    db = SessionLocal()
    init_db()

    last_record = db.query(WaterData).order_by(WaterData.timestamp.desc()).first()
    if last_record:
        timestamp = last_record.timestamp
    else:
        timestamp = datetime.utcnow()

    while True:
        timestamp += timedelta(seconds=interval_seconds)  
        water, alert = generate_record(timestamp)
        db.add(water)
        if alert:
            db.add(alert)
        db.commit()
        print(f"Inserted live record at {timestamp}")
        time.sleep(interval_seconds)
