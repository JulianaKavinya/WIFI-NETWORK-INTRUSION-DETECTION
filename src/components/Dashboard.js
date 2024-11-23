import React, { useState, useEffect } from 'react';
import '../styles/Dashboard.css';

function Dashboard() {
  const [knownDevices, setKnownDevices] = useState([
    { mac: "00:1A:2B:3C:4D:5E", name: "Laptop" },
    { mac: "11:22:33:44:55:66", name: "Smartphone" },
  ]);

  const [logs, setLogs] = useState([
    { mac: "AA:BB:CC:DD:EE:FF", ip: "192.168.1.101", time: "2024-11-13 10:30 AM" },
    { mac: "FF:EE:DD:CC:BB:AA", ip: "192.168.1.102", time: "2024-11-13 11:15 AM" },
  ]);

  // Placeholder for future useEffect logic
  useEffect(() => {
    console.log("This is a placeholder for future useEffect logic.");
  }, []);

  // Function to show the Add Device form
  const showAddDeviceForm = () => {
    document.getElementById("addDeviceForm").style.display = "block";
  };

  // Function to add a new device
  const addDevice = () => {
    const macAddress = document.getElementById("macAddress").value;
    const deviceName = document.getElementById("deviceName").value;
    
    if (macAddress && deviceName) {
      // Add device to the known devices list
      setKnownDevices([...knownDevices, { mac: macAddress, name: deviceName }]);
      
      // Hide the form
      document.getElementById("addDeviceForm").style.display = "none";
      
      // Reset form fields
      document.getElementById("macAddress").value = "";
      document.getElementById("deviceName").value = "";

      alert("Device added successfully!");
    } else {
      alert("Please enter both MAC Address and Device Name.");
    }
  };

  return (
    <div className="body">
      <div className="container">
        <div className="card">
          <h2>Known Devices</h2>
          <table>
            <thead>
              <tr>
                <th>MAC Address</th>
                <th>Device Name</th>
              </tr>
            </thead>
            <tbody>
              {knownDevices.map((device, index) => (
                <tr key={index}>
                  <td>{device.mac}</td>
                  <td>{device.name}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <button className="btn" onClick={showAddDeviceForm}>Add Device</button>
        </div>

        <div className="card">
          <h2>Detection Logs</h2>
          <table>
            <thead>
              <tr>
                <th>MAC Address</th>
                <th>IP Address</th>
                <th>Time Detected</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log, index) => (
                <tr key={index}>
                  <td>{log.mac}</td>
                  <td>{log.ip}</td>
                  <td>{log.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="form-container" id="addDeviceForm" style={{ display: 'none' }}>
        <h2>Add New Device</h2>
        <input type="text" className="form-input" id="macAddress" placeholder="MAC Address" />
        <input type="text" className="form-input" id="deviceName" placeholder="Device Name" />
        <button className="btn" onClick={addDevice}>Add Device</button>
      </div>
    </div>
  );
}

export default Dashboard;
