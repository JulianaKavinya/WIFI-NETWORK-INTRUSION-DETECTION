# seed_data.py
from sqlalchemy.orm import Session
from database.database_manager import add_device, get_all_devices, log_detection_event, get_logs
from database.db import get_db
