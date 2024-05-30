import React, { useState } from 'react';
import axios from 'axios';
import ChatBot from './ChatBot';


function App() {
  const [dbInfo, setDbInfo] = useState({
    host: 'localhost',
    port: '3306', // MySQL default port
    user: 'root',
    password: 'vineesha',
    database: 'internship_management',
  });
  const [isConnected, setIsConnected] = useState(false);

  const handleDbInfoChange = (event) => {
    const { name, value } = event.target;
    setDbInfo((prevDbInfo) => ({
      ...prevDbInfo,
      [name]: value,
    }));
  };

  const handleConnect = async () => {
    try {
      console.log("Sending dbInfo:", dbInfo);  // Debugging line
      const response = await axios.post('http://localhost:5000/api/connect', dbInfo, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      console.log(response.data.status)
      if (response.data.status === 'success') {
        setIsConnected(true);
  
      } else {
        alert('Failed to connect to the database: ' + response.data.message);
      }
    } catch (error) {
      console.error('Connection failed:', error.response || error.message || error);
      alert('Failed to connect to the database: ' + (error.response?.data?.message || error.message));
    }
  };

  return (
    <div className="flex h-screen">
      <div className="w-1/4 bg-gray-200 p-4">
        <h1 className="text-xl font-bold mb-4">Database Connection</h1>
        <div className="space-y-4">
          <label className="block">
            Host:
            <input
              type="text"
              name="host"
              value={dbInfo.host}
              onChange={handleDbInfoChange}
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            />
          </label>
          <label className="block">
            Port:
            <input
              type="text"
              name="port"
              value={dbInfo.port}
              onChange={handleDbInfoChange}
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            />
          </label>
          <label className="block">
            User:
            <input
              type="text"
              name="user"
              value={dbInfo.user}
              onChange={handleDbInfoChange}
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            />
          </label>
          <label className="block">
            Password:
            <input
              type="password"
              name="password"
              value={dbInfo.password}
              onChange={handleDbInfoChange}
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            />
          </label>
          <label className="block">
            Database:
            <input
              type="text"
              name="database"
              value={dbInfo.database}
              onChange={handleDbInfoChange}
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            />
          </label>
          <button
            onClick={handleConnect}
            className="w-full bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600"
          >
            Connect
          </button>
          <div className=' rounded-sm p-2 m-1 text-green-600'>
            {isConnected?<p>Sucessfully Connected!</p>:''}
          </div>
        </div>
      </div>
      
      <div className="flex-1 p-4">
        {isConnected ? <ChatBot dbInfo={dbInfo} /> : <p>Please connect to the database.</p>}
      </div>
    </div>
  );
}

export default App;
