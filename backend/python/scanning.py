import sqlite3
from scapy.all import ARP, Ether, srp
from database.database_manager import insert_device, is_device_whitelisted
import requests

def scan_network():
    devices = []
    # Define the target IP range (replace with your network range if needed)
    target_ip = "192.168.1.1/24"
    
    # Create an ARP request packet
    arp_request = ARP(pdst=target_ip)
    # Create an Ethernet frame to broadcast the ARP request
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Combine the Ethernet frame and ARP request
    arp_request_broadcast = broadcast / arp_request

    try:
        # Send the packet and capture responses
        answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    except Exception as e:
        print(f"Error during network scan: {str(e)}")
        return devices  # Return an empty list if an error occurs

    # Process the responses
    for sent, received in answered_list:
        device = {"ip": received.psrc, "mac": received.hwsrc}
        devices.append(device)
    
    return devices

def process_devices():
    devices = scan_network()
    for device in devices:
        if not is_device_whitelisted(device["mac"]):
            # Log unauthorized devices
            insert_device(device["ip"], device["mac"], authorized=False)
            
            # Trigger SMS alert
            alert_message = {
                "message": f"Unauthorized device detected: IP={device['ip']}, MAC={device['mac']}",
                "phoneNumber": "admin_number"  # Replace with actual admin phone number
            }
            try:
                response = requests.post("http://localhost:3000/api/alerts", json=alert_message)
                response.raise_for_status()  # Raise an error for unsuccessful HTTP responses
            except requests.RequestException as e:
                print(f"Failed to send SMS alert: {str(e)}")
