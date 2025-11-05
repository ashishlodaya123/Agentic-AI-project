import { useState, useEffect } from 'react';
import { checkBackendStatus } from '../api';

const Home = () => {
  const [backendStatus, setBackendStatus] = useState('Checking...');

  useEffect(() => {
    checkBackendStatus()
      .then(response => {
        if (response.status === 200) {
          setBackendStatus('Connected');
        } else {
          setBackendStatus('Disconnected');
        }
      })
      .catch(() => {
        setBackendStatus('Disconnected');
      });
  }, []);

  return (
    <div className="bg-white p-8 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Welcome to the Agentic Clinical Decision Assistant</h2>
      <p className="text-gray-700 mb-4">
        This application uses a multi-agent AI system to provide real-time triage recommendations based on patient data.
      </p>
      <div className="flex items-center">
        <p className="text-lg font-semibold mr-2">Backend Status:</p>
        <p className={`text-lg font-bold ${backendStatus === 'Connected' ? 'text-green-500' : 'text-red-500'}`}>
          {backendStatus}
        </p>
      </div>
    </div>
  );
};

export default Home;
