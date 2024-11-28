import requests

def send_sms(message, phone_number):
    """Send SMS via the Node.js service."""
    sms_data = {
        "message": message,
        "phoneNumber": phone_number
    }
    try:
        response = requests.post("http://localhost:3001/send-sms", json=sms_data)
        if response.status_code == 200:
            print("SMS sent successfully")
        else:
            print("Failed to send SMS", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error calling SMS service: {e}")
