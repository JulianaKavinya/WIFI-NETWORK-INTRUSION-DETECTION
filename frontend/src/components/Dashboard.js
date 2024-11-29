import React, { useState, useEffect } from 'react';
import '../styles/Dashboard.css';
import axios from 'axios';

function Dashboard() {
  const [knownDevices, setKnownDevices] = useState([]);
  const [logs, setLogs] = useState([]);

  // Fetch devices and logs from the backend
  useEffect(() => {
    // Fetch known devices
    axios
      .get("http://localhost:5000/get-devices")
      .then((response) => setKnownDevices(response.data))
      .catch((error) => console.error("Error fetching known devices:", error));

    // Fetch detection logs
    axios
      .get("http://localhost:5000/logs")
      .then((response) => setLogs(response.data))
      .catch((error) => console.error("Error fetching logs:", error));

    // Setup WebSocket for real-time updates (if your backend supports it)
    const eventSource = new EventSource("http://localhost:5000/stream-updates");
    eventSource.onmessage = function(event) {
      console.log("Received event", event.data);
      
    };

    return () => {
      eventSource.close();
    };
  }, [knownDevices]);

  // Add a device to the whitelist
  const addDevice = () => {
    const macAddress = document.getElementById("macAddress").value;
    const deviceName = document.getElementById("deviceName").value;

    if (macAddress && deviceName) {
      axios
        .post("http://localhost:5000/add-device", {
          mac: macAddress,
          name: deviceName,
        })
        .then((response) => {
          alert(response.data.message || "Device added successfully!");
          // Refresh the known devices list
          setKnownDevices([...knownDevices, { mac: macAddress, name: deviceName }]);
          // Reset form and hide it
          document.getElementById("addDeviceForm").style.display = "none";
          document.getElementById("macAddress").value = "";
          document.getElementById("deviceName").value = "";
        })
        .catch((error) => {
          alert(error.response?.data?.error || "Failed to add device");
        });
    } else {
      alert("Please enter both MAC Address and Device Name.");
    }
  };

  // Block a device
  const blockDevice = (mac) => {
    axios
      .post("http://localhost:5000/block", { mac })
      .then(() => {
        alert(`Device with MAC ${mac} has been blocked.`);
        setKnownDevices(knownDevices.filter((device) => device.mac !== mac));
      })
      .catch((error) => console.error("Error blocking device:", error));
  };

  // Allow a device (restore from blocked state)
  const allowDevice = (mac) => {
    axios
      .post("http://localhost:5000/allow", { mac })
      .then(() => {
        alert(`Device with MAC ${mac} has been allowed.`);
      })
      .catch((error) => console.error("Error allowing device:", error));
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
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {knownDevices.map((device, index) => (
                <tr key={index}>
                  <td>{device.mac}</td>
                  <td>{device.name}</td>
                  <td>
                    <button className="btn" onClick={() => blockDevice(device.mac)}>
                      Block
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <button
            className="btn"
            onClick={() => document.getElementById("addDeviceForm").style.display = "block"}
          >
            Add Device
          </button>
        </div>

        <div className="card">
          <h2>Detection Logs</h2>
          <table>
            <thead>
              <tr>
                <th>MAC Address</th>
                <th>IP Address</th>
                <th>Time Detected</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log, index) => (
                <tr key={index}>
                  <td>{log.mac}</td>
                  <td>{log.ip}</td>
                  <td>{log.time}</td>
                  <td>
                    <button className="btn" onClick={() => allowDevice(log.mac)}>
                      Allow
                    </button>
                    <button className="btn" onClick={() => blockDevice(log.mac)}>
                      Block
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="form-container" id="addDeviceForm" style={{ display: "none" }}>
        <h2>Add New Device</h2>
        <input type="text" className="form-input" id="macAddress" placeholder="MAC Address" />
        <input type="text" className="form-input" id="deviceName" placeholder="Device Name" />
        <button className="btn" onClick={addDevice}>
          Add Device
        </button>
      </div>
    </div>
  );
}

export default Dashboard;
