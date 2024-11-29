from flask import Flask, request, jsonify
from scanning import scan_network, process_devices
from sms import send_sms
from database.database_manager import get_db_connection, insert_device
import sqlite3

app = Flask(__name__)

# Database file location
DATABASE = "D:\\Projects\\WIFI-NETWORK-INTRUSION-DETECTION\\database\\network_monitor.db"

@app.route('/')
def home():
    return "Welcome to the WiFi Network Intrusion Detection System!"

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content for favicon

@app.route('/someendpoint', methods=['POST'])
def some_function():
    data = request.form.get('some_key')  # This might return None if 'some_key' is not in the form
    print(f"Data received: {data}")  # Check the value of 'data'
    if data is None:
        return 'Error: No data provided', 400
    # Continue processing if data is not None

@app.route('/api', methods=['GET'])
def api_function():
    response = some_api_call()  # This might return None
    if response is None:
        return 'API Error: No data received', 500

    # Safe to process response since it's not None
    result = response.get('key')  # Example: Accessing data
    return jsonify(result)

@app.route('/scan', methods=['GET'])
def scan():
    """Scan the network and save devices to the database."""
    devices = scan_network()

    if not devices:
        return jsonify({"message": "No devices found."}), 200
    return jsonify(devices), 200

 # Process each detected device
    for device in devices:
        # Insert the device into the database if it doesn't exist
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices WHERE mac = ?", (device['mac'],))
        existing_device = cursor.fetchone()
        
        if not existing_device:  # If device does not already exist in the database
            cursor.execute("INSERT INTO devices (mac, name, authorized) VALUES (?, ?, ?)",
                           (device['mac'], device['name'], 1))
            conn.commit()
        
        conn.close()

        # Optionally send an SMS for each detected device
        try:
            send_sms(f"New device detected: {device['ip']} - {device['mac']}", "+254XXXXXXXXX")
        except Exception as e:
            return jsonify({"error": f"Failed to send SMS: {str(e)}"}), 500

    return jsonify(devices), 200   

@app.route('/add-device', methods=['POST'])
def add_device():
    print("POST request to /add-device")
    """Add a device to the database."""
    data = request.json
    mac = data.get('mac')
    name = data.get('name')

    if not mac or not name:
        return jsonify({"error": "MAC address and name are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Insert into the 'devices' table, assuming it has 'mac', 'name', and 'authorized' columns
        cursor.execute("INSERT INTO devices (mac, name, authorized) VALUES (?, ?, ?)", (mac, name, 1))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Device with this MAC address already exists"}), 409
    finally:
        conn.close()

    return jsonify({"success": True, "message": "Device added successfully"}), 201

@app.route('/get-devices', methods=['GET'])
def get_devices():
    """Retrieve all devices from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    devices = cursor.execute("SELECT * FROM devices").fetchall()
    conn.close()

    # Convert devices to a list of dictionaries
    devices_list = [dict(device) for device in devices]
    return jsonify(devices_list), 200

if __name__ == "__main__":
    # Run the Flask app on port 5000
    app.run(debug=True, port=5000)

print("Available Routes:", app.url_map)
