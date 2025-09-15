import time
from datetime import datetime

from backend.db import SessionLocal
from seed import generate_record  

def simulate_live(interval_seconds: int = 5):
    """Continuously insert live water data every N seconds."""
    db = SessionLocal()
    try:
        while True:
            now = datetime.utcnow()
            water, alert = generate_record(now)
            db.add(water)
            if alert:
                db.add(alert)
            db.commit()
            print(f"Inserted live record at {now}")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("Stopped live simulation.")
    finally:
        db.close()

if __name__ == "__main__":
    simulate_live(interval_seconds=10)
