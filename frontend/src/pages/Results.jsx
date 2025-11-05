import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getTaskResult } from '../api';
import { motion } from 'framer-motion';

const Results = () => {
  const { taskId } = useParams();
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

  if (loading) {
    return (
      <div className="flex justify-center items-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full"
        />
        <p className="ml-4 text-lg">Analyzing patient data...</p>
      </div>
    );
  }

  if (error) {
    return <p className="text-red-500">{error}</p>;
  }

  const { final_recommendation } = result.result;

  const getUrgencyColor = (recommendation) => {
    if (recommendation.includes("High")) return "bg-red-500";
    if (recommendation.includes("Medium")) return "bg-yellow-500";
    return "bg-green-500";
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Triage Results</h2>
      <div className={`p-4 rounded-lg text-white ${getUrgencyColor(final_recommendation)}`}>
        <pre className="whitespace-pre-wrap">{final_recommendation}</pre>
      </div>
    </div>
  );
};

export default Results;
