from flask import Flask, request, jsonify
from scanning import scan_network, process_devices
from sms import send_sms
import sqlite3

app = Flask(__name__)

# Database file location
DATABASE = "D:\\Projects\\WIFI-NETWORK-INTRUSION-DETECTION\\database\\network_monitor.db"

def get_db_connection():
    """Create and return a SQLite database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/scan', methods=['GET'])
def scan():
    """Scan the network and save devices to the database."""
    devices = scan_network()
    for device in devices:
        process_devices(device['ip'], device['mac'])
        # Replace '+254XXXXXXXXX' with the actual phone number to notify
        send_sms(f"New device detected: {device['ip']} - {device['mac']}", "+254XXXXXXXXX")
    return jsonify(devices)

@app.route('/add-device', methods=['POST'])
def add_device():
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
    return jsonify(devices_list)

if __name__ == "__main__":
    # Update the port to 5000 for Flask
    app.run(debug=True, port=5000)

