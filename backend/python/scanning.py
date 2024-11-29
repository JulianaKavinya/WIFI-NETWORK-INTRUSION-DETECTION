import sqlite3
from scapy.all import ARP, Ether, sr1
from database.database_manager import insert_device, is_device_whitelisted
import requests

def scan_network():
    devices = []
    arp_request = ARP(pdst="192.168.1.1/24")
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = sr1(arp_request_broadcast, timeout=1, verbose=False)

    # Check if we got a response
    if answered_list is None:
        print("No response received")
        return devices  # Return an empty list if no devices responded


    for element in answered_list:
        device = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        devices.append(device)
    return devices

def process_devices():
    devices = scan_network()
    for device in devices:
        if not is_device_whitelisted(device["mac"]):
            # Log unauthorized devices
            insert_device(device["ip"], device["mac"], authorized=False)
            # Trigger SMS alert
            data = {"message": f"Unauthorized device: {device['ip']} ({device['mac']})", "phoneNumber": "admin_number"}
            requests.post("http://localhost:3000/api/alerts", json=data)
