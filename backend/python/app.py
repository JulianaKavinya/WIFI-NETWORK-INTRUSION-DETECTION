from flask import Flask, request, jsonify, Response
from scapy.all import ARP, Ether, srp  
from scanning import scan_network, process_devices  # Import your custom modules
from sms import send_sms
from database.database_manager import get_db_connection, insert_device
import sqlite3
from flask_cors import CORS
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

# Database file location
DATABASE = "D:\\Projects\\WIFI-NETWORK-INTRUSION-DETECTION\\database\\network_monitor.db"

# Database connection helper
def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row  # Access rows as dictionaries
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        raise

# Route: Home
@app.route('/')
def home():
    return "Welcome to the WiFi Network Intrusion Detection System!"

# Route: Scan Network
@app.route('/scan', methods=['GET'])
def scan():
    """Scan the network and save devices to the database."""
    try:
        devices = scan_network()  # Assume this returns a list of device dictionaries
        if not devices:
            return jsonify({"message": "No devices found."}), 200

        for device in devices:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM devices WHERE mac = ?", (device['mac'],))
            existing_device = cursor.fetchone()

            # Insert new device if not already in the database
            if not existing_device:
                cursor.execute(
                    "INSERT INTO devices (mac, name, authorized) VALUES (?, ?, ?)",
                    (device['mac'], device.get('name', 'Unknown'), 1)
                )
                conn.commit()
            conn.close()

            # Send SMS notification
            try:
                send_sms(f"New device detected: {device['ip']} - {device['mac']}", "+254XXXXXXXXX")
            except Exception as sms_error:
                print(f"Error sending SMS: {sms_error}")
                return jsonify({"error": f"Failed to send SMS: {str(sms_error)}"}), 500

        return jsonify({"devices": devices, "message": "Scan completed successfully."}), 200
    except Exception as e:
        print(f"Error during scanning: {e}")
        return jsonify({"error": "An error occurred during scanning.", "details": str(e)}), 500

# Route: Add Device
@app.route('/add-device', methods=['POST'])
def add_device():
    """Add a new device to the database."""
    data = request.json
    mac = data.get('mac')
    name = data.get('name')

    if not mac or not name:
        return jsonify({"error": "MAC address and name are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO devices (mac, name, authorized) VALUES (?, ?, ?)", 
            (mac, name, 1)
        )
        conn.commit()
        return jsonify({"success": True, "message": "Device added successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Device with this MAC address already exists"}), 409
    except Exception as e:
        print(f"Error adding device: {e}")
        return jsonify({"error": "An error occurred while adding the device."}), 500
    finally:
        conn.close()

# Route: Get Devices
@app.route('/get-devices', methods=['GET'])
def get_devices():
    """Retrieve all devices from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        devices = cursor.execute("SELECT * FROM devices").fetchall()
        conn.close()
        devices_list = [dict(device) for device in devices]
        return jsonify(devices_list), 200
    except Exception as e:
        print(f"Error retrieving devices: {e}")
        return jsonify({"error": "An error occurred while retrieving devices."}), 500

# Route: Logs
@app.route('/logs', methods=['GET'])
def get_logs():
    """Retrieve logs (placeholder functionality)."""
    logs = []  # Add your actual logs implementation here
    return jsonify(logs)

# Route: Stream Updates (SSE)
@app.route('/stream-updates', methods=['GET'])
def stream_updates():
    """Stream live updates using Server-Sent Events (SSE)."""
    def generate():
        while True:
            yield f"data: {json.dumps({'mac': '11:22:33:44:55:66', 'ip': '192.168.1.4'})}\n\n"
    
    response = Response(generate(), content_type='text/event-stream')
    # Add CORS headers
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Cache-Control'] = 'no-cache'
    return response

# Main entry point
if __name__ == "__main__":
    print("Available Routes:", app.url_map)
    app.run(debug=True, port=5000)
