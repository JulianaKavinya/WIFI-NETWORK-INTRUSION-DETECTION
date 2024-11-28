import sqlite3

DB_PATH = "database.db"

# Function to initialize the database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the devices table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            mac TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create the whitelist table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS whitelist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            mac TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Function to save a device to the database
def save_device(ip, mac):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO devices (ip, mac) VALUES (?, ?)", (ip, mac))
    conn.commit()
    conn.close()

# Function to check if a device is in the whitelist
def is_device_whitelisted(mac):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM whitelist WHERE mac = ?", (mac,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Function to add a device to the whitelist
def add_to_whitelist(ip, mac):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO whitelist (ip, mac) VALUES (?, ?)", (ip, mac))
    conn.commit()
    conn.close()
