import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean, Index, func
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nirikshana.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False, "timeout": 30})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class WaterData(Base):
    __tablename__ = "water_data"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True, nullable=True)
    river = Column(String, index=True, nullable=True)
    location = Column(String, index=True, nullable=True)
    ph = Column(Float, nullable=True)
    tds = Column(Float, nullable=True)
    turbidity = Column(Float, nullable=True)
    flow_rate = Column(Float, nullable=True)
    prediction = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    __table_args__ = (Index('idx_device_time', "device_id", "timestamp"),)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True, nullable=True)
    river = Column(String, nullable=True)
    location = Column(String, nullable=True)
    alert_type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    severity = Column(String, nullable=False, default="medium")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(String, nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)
