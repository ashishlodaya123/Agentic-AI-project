import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FaExclamationTriangle, FaExclamationCircle, FaInfoCircle, FaHeartbeat, FaFileMedical, FaBookMedical, FaPrint, FaUserMd } from 'react-icons/fa';
import { motion } from 'framer-motion';
import { getTaskResult } from '../api';

const Results = () => {
  const { taskId } = useParams();
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const pollResult = setInterval(() => {
      getTaskResult(taskId)
        .then(response => {
          if (response.data.status === 'Success') {
            setResult(response.data.result);
            setLoading(false);
            clearInterval(pollResult);
          } else if (response.data.status === 'Failed') {
            setError('Triage process failed.');
            setLoading(false);
            clearInterval(pollResult);
          }
        })
        .catch(err => {
          setError('Error fetching results.');
          setLoading(false);
          clearInterval(pollResult);
        });
    }, 2000); // Poll every 2 seconds

    return () => clearInterval(pollResult);
  }, [taskId]);

  const handleStartNewTriage = () => {
    navigate('/triage');
  };

  const handlePrintReport = () => {
    window.print();
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card">
          <div className="card-body text-center py-12">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full mx-auto mb-6"
            />
            <h2 className="h2 text-neutral-text mb-2">Analyzing Patient Data</h2>
            <p className="body-large text-neutral-text-secondary">
              Our AI system is processing the patient information...
            </p>
            <div className="mt-6 w-full bg-neutral-border rounded-full h-2.5">
              <motion.div 
                className="bg-primary h-2.5 rounded-full" 
                initial={{ width: "0%" }}
                animate={{ width: "100%" }}
                transition={{ duration: 2, repeat: Infinity }}
              ></motion.div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card">
          <div className="card-body text-center py-12">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
              <FaExclamationTriangle className="h-6 w-6 text-red-600" />
            </div>
            <h3 className="h3 text-neutral-text mt-4">Error</h3>
            <div className="mt-2">
              <p className="body-large text-neutral-text-secondary">{error}</p>
            </div>
            <div className="mt-6">
              <button 
                onClick={handleStartNewTriage}
                className="btn btn-primary"
              >
                Start New Triage
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Check if result exists before accessing its properties
  if (!result || !result.result) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card">
          <div className="card-body text-center py-12">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-amber-100">
              <FaExclamationCircle className="h-6 w-6 text-amber-600" />
            </div>
            <h3 className="h3 text-neutral-text mt-4">Invalid Result Data</h3>
            <div className="mt-2">
              <p className="body-large text-neutral-text-secondary">
                Received invalid result data from the server.
              </p>
            </div>
            <div className="mt-6">
              <button 
                onClick={handleStartNewTriage}
                className="btn btn-primary"
              >
                Start New Triage
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const { final_recommendation, risk_stratification, medical_imaging, knowledge_retrieval } = result.result;

  const getUrgencyConfig = (recommendation) => {
    if (recommendation.includes("High")) {
      return {
        color: "text-red-800",
        bg: "bg-red-100",
        badge: "badge-error",
        border: "border-red-500",
        icon: FaExclamationTriangle
      };
    }
    if (recommendation.includes("Medium")) {
      return {
        color: "text-amber-800",
        bg: "bg-amber-100",
        badge: "badge-warning",
        border: "border-amber-500",
        icon: FaInfoCircle
      };
    }
    return {
      color: "text-green-800",
      bg: "bg-green-100",
      badge: "badge-success",
      border: "border-green-500",
      icon: FaInfoCircle
    };
  };

  const urgencyConfig = getUrgencyConfig(final_recommendation);
  const UrgencyIcon = urgencyConfig.icon;

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="h1 text-neutral-text">Triage Results</h1>
        <p className="body-large text-neutral-text-secondary mt-2">
          Patient assessment completed successfully
        </p>
      </div>

      {/* Final Recommendation */}
      <div className="card mb-8">
        <div className="card-header">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <h2 className="h2 text-neutral-text">Final Triage Recommendation</h2>
            <span className={`badge ${urgencyConfig.badge} mt-2 md:mt-0`}>
              {final_recommendation.includes("High") ? "High Priority" : 
               final_recommendation.includes("Medium") ? "Medium Priority" : "Low Priority"}
            </span>
          </div>
        </div>
        <div className="card-body">
          <div className="prose max-w-none">
            <pre className="whitespace-pre-wrap font-sans body-large text-neutral-text">
              {final_recommendation}
            </pre>
          </div>
        </div>
      </div>

      {/* Detailed Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Risk Stratification */}
        <div className="card">
          <div className="card-header">
            <div className="flex items-center">
              <div className="bg-blue-100 p-2 rounded-lg mr-3">
                <FaHeartbeat className="h-5 w-5 text-primary" />
              </div>
              <h3 className="h3 text-neutral-text">Risk Stratification</h3>
            </div>
          </div>
          <div className="card-body">
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap font-sans body-small text-neutral-text-secondary">
                {risk_stratification}
              </pre>
            </div>
          </div>
        </div>

        {/* Medical Imaging */}
        <div className="card">
          <div className="card-header">
            <div className="flex items-center">
              <div className="bg-green-100 p-2 rounded-lg mr-3">
                <FaFileMedical className="h-5 w-5 text-green-600" />
              </div>
              <h3 className="h3 text-neutral-text">Medical Imaging</h3>
            </div>
          </div>
          <div className="card-body">
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap font-sans body-small text-neutral-text-secondary">
                {medical_imaging}
              </pre>
            </div>
          </div>
        </div>

        {/* Knowledge Retrieval */}
        <div className="card">
          <div className="card-header">
            <div className="flex items-center">
              <div className="bg-purple-100 p-2 rounded-lg mr-3">
                <FaBookMedical className="h-5 w-5 text-purple-600" />
              </div>
              <h3 className="h3 text-neutral-text">Knowledge Retrieval</h3>
            </div>
          </div>
          <div className="card-body">
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap font-sans body-small text-neutral-text-secondary">
                {knowledge_retrieval}
              </pre>
            </div>
          </div>
        </div>
      </div>

      {/* Task Information */}
      <div className="card">
        <div className="card-header">
          <h2 className="h2 text-neutral-text">Task Information</h2>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="body-small text-neutral-text-secondary">Task ID</p>
              <p className="font-mono body-large text-neutral-text">{taskId}</p>
            </div>
            <div>
              <p className="body-small text-neutral-text-secondary">Status</p>
              <span className="badge badge-success">Completed</span>
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="mt-8 flex flex-col sm:flex-row sm:justify-center gap-4">
        <button 
          onClick={handleStartNewTriage}
          className="btn btn-primary"
        >
          <FaUserMd className="mr-2" />
          Start New Triage
        </button>
        <button 
          onClick={handlePrintReport}
          className="btn btn-secondary"
        >
          <FaPrint className="mr-2" />
          Print Report
        </button>
      </div>
    </div>
  );
};

export default Results;