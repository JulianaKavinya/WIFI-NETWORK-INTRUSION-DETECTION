# database_manager.py
from sqlalchemy.orm import Session
from .models import Device, Log

def add_device(db: Session,ip_address: str, mac_address: str, device_name: str):
    device = Device(ip_address=ip_address, mac_address=mac_address, device_name=device_name)
    db.add(device)
    db.commit()
    db.refresh(device)
    return device

def remove_device(db: Session, mac_address: str):
    device = db.query(Device).filter(Device.mac_address == mac_address).first()
    if device:
        db.delete(device)
        db.commit()

def get_all_devices(db: Session):
    return db.query(Device).all()

def log_detection_event(db: Session, mac_address: str, ip_address: str, alert_sent: bool):
    log = Log(mac_address=mac_address, ip_address=ip_address, alert_sent=alert_sent)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_logs(db: Session, alert_sent: bool = None):
    query = db.query(Log)
    if alert_sent is not None:
        query = query.filter(Log.alert_sent == alert_sent)
    return query.all()
