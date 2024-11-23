export async function fetchDevices() {
    const response = await fetch('http://localhost:3000/api/devices');
    const data = await response.json();
    return data;
  }
  