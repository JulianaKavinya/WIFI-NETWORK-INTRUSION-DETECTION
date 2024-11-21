from scapy.all import ARP, Ether, srp

def scan_network():
    # Set target IP range, e.g., 192.168.1.1/24
    target_ip = "192.168.1.1/24"
    # Create ARP packet
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Send packet and receive response
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices
def save_to_database(devices):
    # Connect to (or create) the database
    conn = sqlite3.connect("db.py")
    cursor = conn.cursor()