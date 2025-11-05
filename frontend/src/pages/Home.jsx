import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaCheckCircle, FaExclamationTriangle, FaSkull, FaShieldAlt, FaCogs, FaChartBar, FaUserMd } from 'react-icons/fa';
import { GiMedicalPack } from 'react-icons/gi';
import { checkBackendStatus } from '../api';

const Home = () => {
  const [backendStatus, setBackendStatus] = useState('Checking...');
  const navigate = useNavigate();

  useEffect(() => {
    checkBackendStatus()
      .then(response => {
        if (response && response.status === 200) {
          setBackendStatus('Connected');
        } else {
          setBackendStatus('Disconnected');
        }
      })
      .catch(() => {
        setBackendStatus('Disconnected');
      });
  }, []);

  // Status badge component
  const StatusBadge = ({ status }) => {
    const statusConfig = {
      'Connected': { bg: 'bg-green-100', text: 'text-green-800', label: 'Connected', icon: FaCheckCircle },
      'Disconnected': { bg: 'bg-red-100', text: 'text-red-800', label: 'Disconnected', icon: FaSkull },
      'Checking...': { bg: 'bg-amber-100', text: 'text-amber-800', label: 'Checking...', icon: FaExclamationTriangle }
    };
    
    const config = statusConfig[status] || statusConfig['Disconnected'];
    const Icon = config.icon;
    
    return (
      <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${config.bg} ${config.text}`}>
        <Icon className={`w-4 h-4 mr-2`} />
        {config.label}
      </span>
    );
  };

  const handleStartTriage = () => {
    navigate('/triage');
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary to-secondary rounded-2xl shadow-lg p-8 mb-8">
        <div className="flex flex-col lg:flex-row items-center">
          <div className="lg:w-2/3 mb-8 lg:mb-0 lg:pr-8">
            <h1 className="display text-white mb-4">Agentic Clinical Decision Assistant</h1>
            <p className="text-xl text-blue-100 mb-6">
              AI-powered real-time emergency triage system for healthcare professionals
            </p>
            <div className="flex flex-col sm:flex-row sm:items-center">
              <span className="text-blue-100 font-medium mr-3 mb-2 sm:mb-0">Backend Status:</span>
              <StatusBadge status={backendStatus} />
            </div>
          </div>
          <div className="lg:w-1/3 flex justify-center">
            <div className="bg-white bg-opacity-20 rounded-full p-6">
              <GiMedicalPack className="h-24 w-24 text-white" />
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card transition-all duration-300 hover:shadow-lg">
          <div className="card-body">
            <div className="flex items-center mb-4">
              <div className="bg-blue-100 p-3 rounded-lg mr-4">
                <FaShieldAlt className="h-6 w-6 text-primary" />
              </div>
              <h3 className="h3 text-neutral-text">Real-time Triage</h3>
            </div>
            <p className="body-large text-neutral-text-secondary">
              Instant patient risk assessment based on symptoms and vitals
            </p>
          </div>
        </div>

        <div className="card transition-all duration-300 hover:shadow-lg">
          <div className="card-body">
            <div className="flex items-center mb-4">
              <div className="bg-green-100 p-3 rounded-lg mr-4">
                <FaCogs className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="h3 text-neutral-text">Multi-Agent System</h3>
            </div>
            <p className="body-large text-neutral-text-secondary">
              Specialized AI agents for risk stratification, medical imaging, and knowledge retrieval
            </p>
          </div>
        </div>

        <div className="card transition-all duration-300 hover:shadow-lg">
          <div className="card-body">
            <div className="flex items-center mb-4">
              <div className="bg-purple-100 p-3 rounded-lg mr-4">
                <FaChartBar className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="h3 text-neutral-text">Performance Metrics</h3>
            </div>
            <p className="body-large text-neutral-text-secondary">
              Comprehensive monitoring and analytics for system performance
            </p>
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="card">
        <div className="card-header">
          <h2 className="h2 text-neutral-text">How It Works</h2>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="bg-primary bg-opacity-10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary">1</span>
              </div>
              <h3 className="h3 text-neutral-text mb-2">Patient Intake</h3>
              <p className="body-small text-neutral-text-secondary">
                Enter patient symptoms, vitals, and demographics
              </p>
            </div>
            <div className="text-center">
              <div className="bg-green-500 bg-opacity-10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-green-500">2</span>
              </div>
              <h3 className="h3 text-neutral-text mb-2">AI Analysis</h3>
              <p className="body-small text-neutral-text-secondary">
                Multi-agent system processes the information
              </p>
            </div>
            <div className="text-center">
              <div className="bg-amber-500 bg-opacity-10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-amber-500">3</span>
              </div>
              <h3 className="h3 text-neutral-text mb-2">Risk Assessment</h3>
              <p className="body-small text-neutral-text-secondary">
                Real-time risk stratification and recommendations
              </p>
            </div>
            <div className="text-center">
              <div className="bg-purple-500 bg-opacity-10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-purple-500">4</span>
              </div>
              <h3 className="h3 text-neutral-text mb-2">Actionable Insights</h3>
              <p className="body-small text-neutral-text-secondary">
                Clinical recommendations for immediate action
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-8 text-center">
        <button 
          onClick={handleStartTriage}
          className="btn btn-primary inline-flex items-center"
        >
          Start New Triage
          <FaUserMd className="h-5 w-5 ml-2" />
        </button>
      </div>
    </div>
  );
};

export default Home;