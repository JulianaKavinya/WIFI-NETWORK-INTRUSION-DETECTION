import React from 'react';

function DeviceList({ devices }) {
  return (
    <ul className="device-list">
      {devices.map(device => (
        <li key={device.id}>
          <strong>{device.name}</strong> - {device.ip}
        </li>
      ))}
    </ul>
  );
}

export default DeviceList;
