import sqlite3

DATABASE = "D:\\Projects\\WIFI-NETWORK-INTRUSION-DETECTION\\database\\network_monitor.db"

def get_db_connection():
    """Create and return a SQLite database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def is_device_whitelisted(mac_address):
    connection = sqlite3.connect("database/network_monitor.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM whitelist WHERE mac = ?", (mac_address,))
    result = cursor.fetchone()
    connection.close()
    return result is not None

def insert_device(ip, mac, authorized=False):
    connection = sqlite3.connect("database/network_monitor.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO devices (ip, mac, authorized) VALUES (?, ?, ?)", (ip, mac, authorized))
    connection.commit()
    connection.close()
