from flask import Flask, request, jsonify, Response
from scanning import scan_network, process_devices
from sms import send_sms
from database.database_manager import get_db_connection, insert_device
import sqlite3
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database file location
DATABASE = "D:\\Projects\\WIFI-NETWORK-INTRUSION-DETECTION\\database\\network_monitor.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access rows as dictionaries
    return conn

@app.route('/')
def home():
    return "Welcome to the WiFi Network Intrusion Detection System!"

@app.route('/scan', methods=['GET'])
def scan():
    """Scan the network and save devices to the database."""
    devices = scan_network()

    if not devices:
        return jsonify({"message": "No devices found."}), 200

    for device in devices:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices WHERE mac = ?", (device['mac'],))
        existing_device = cursor.fetchone()

        if not existing_device:
            cursor.execute("INSERT INTO devices (mac, name, authorized) VALUES (?, ?, ?)",
                           (device['mac'], device['name'], 1))
            conn.commit()
        conn.close()

        try:
            send_sms(f"New device detected: {device['ip']} - {device['mac']}", "+254XXXXXXXXX")
        except Exception as e:
            return jsonify({"error": f"Failed to send SMS: {str(e)}"}), 500

    return jsonify(devices), 200

@app.route('/add-device', methods=['POST'])
def add_device():
    data = request.json
    mac = data.get('mac')
    name = data.get('name')

    if not mac or not name:
        return jsonify({"error": "MAC address and name are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO devices (mac, name, authorized) VALUES (?, ?, ?)", (mac, name, 1))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Device with this MAC address already exists"}), 409
    finally:
        conn.close()

    return jsonify({"success": True, "message": "Device added successfully"}), 201

@app.route('/get-devices', methods=['GET'])
def get_devices():
    conn = get_db_connection()
    cursor = conn.cursor()
    devices = cursor.execute("SELECT * FROM devices").fetchall()
    conn.close()
    devices_list = [dict(device) for device in devices]
    return jsonify(devices_list), 200

@app.route('/logs', methods=['GET'])
def get_logs():
    logs = []
    return jsonify(logs)

@app.route('/stream-updates', methods=['GET'])
def stream_updates():
    def generate():
        yield f"data: {json.dumps({'mac': '11:22:33:44:55:66', 'ip': '192.168.1.4'})}\n\n"
    
    response = Response(generate(), content_type='text/event-stream')
    # Add CORS headers
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Cache-Control'] = 'no-cache'
    return response

if __name__ == "__main__":
    print("Available Routes:", app.url_map)
    app.run(debug=True, port=5000)
