# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Device(Base):  # Stores MAC addresses of trusted devices.
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    mac_address = Column(String, unique=True, nullable=False)
    device_name = Column(String, nullable=True)
    ip_address = Column(String, unique=True, nullable=False)

    # This creates a relationship between Device and Log models
    logs = relationship("Log", back_populates="device")

class Log(Base):  # Records details of detected devices, including the detection time and alert status.
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, index=True)
    mac_address = Column(String, ForeignKey("devices.mac_address"), nullable=False)
    ip_address = Column(String, nullable=True)
    detected_at = Column(DateTime, default=datetime.utcnow)
    alert_sent = Column(Boolean, default=False)

    # Back reference to the Device model (each log will have a related device)
    device = relationship("Device", back_populates="logs")

