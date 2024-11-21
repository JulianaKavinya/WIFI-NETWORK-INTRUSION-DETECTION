# detection_system.py

from database.db import SessionLocal
from database.database_manager import (
    add_device,
    remove_device,
    get_all_devices,
    log_detection_event,
    get_logs
)

# Sample function to detect a new device; replace with actual detection logic.
def detect_new_device():
    # Placeholder data simulating a new device detection
    new_device = {
        "ip_address": "192.168.1.101",
        "mac_address": "AA:BB:CC:DD:EE:04",
        "device_name": "New Device"
    }
    return new_device

# Function to handle device detection logic
def handle_device_detection(db):
    # Simulate detecting a new device
    detected_device = detect_new_device()
    
    # Retrieve all known devices
    known_devices = get_all_devices(db)
    known_mac_addresses = {device.mac_address for device in known_devices}
    
    # Check if the device is new
    if detected_device["mac_address"] not in known_mac_addresses:
        # New device detected: add it to the database
        print("New device detected:", detected_device["device_name"])
        
        # Add new device to the database
        add_device(
            db,
            ip_address=detected_device["ip_address"],
            mac_address=detected_device["mac_address"],
            device_name=detected_device["device_name"]
        )
        
        # Log detection event
        log_detection_event(
            db,
            mac_address=detected_device["mac_address"],
            ip_address=detected_device["ip_address"],
            alert_sent=False  # Initially false, update after alert
        )
        
        # Simulate sending an alert (placeholder for actual SMS/notification function)
        print("Sending alert for new device:", detected_device["device_name"])
        
        # Log that the alert was sent
        log_detection_event(
            db,
            mac_address=detected_device["mac_address"],
            ip_address=detected_device["ip_address"],
            alert_sent=True
        )
    else:
        print("Known device detected:", detected_device["device_name"])

# Main detection loop
def main_detection_loop():
    # Create a new database session
    db = SessionLocal()
    
    try:
        # Call detection handling function
        handle_device_detection(db)
    finally:
        # Close the database session
        db.close()

# Run the detection system
if __name__ == "__main__":
    main_detection_loop()
