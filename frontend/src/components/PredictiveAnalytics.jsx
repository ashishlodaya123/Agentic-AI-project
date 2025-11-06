import { useState, useEffect } from 'react';
import { FaChartArea, FaExclamationTriangle, FaShieldAlt } from 'react-icons/fa';
import { getPredictiveAnalytics } from '../api';

const PredictiveAnalytics = ({ taskId, patientData, symptomsAnalysis, riskAssessment, treatmentRecommendations }) => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPredictiveAnalytics = async () => {
      if (!patientData) return;
      
      setLoading(true);
      setError(null);
      
      try {
        const requestData = {
          patient_data: patientData,
          symptoms_analysis: symptomsAnalysis || {},
          risk_assessment: riskAssessment || {},
          treatment_recommendations: treatmentRecommendations || {}
        };
        
        const response = await getPredictiveAnalytics(requestData);
        if (response.data?.success) {
          setAnalyticsData(response.data.data);
        } else {
          setError('Failed to fetch predictive analytics data');
        }
      } catch (err) {
        console.error('Error fetching predictive analytics:', err);
        setError('Error fetching predictive analytics data');
      } finally {
        setLoading(false);
      }
    };
    
    fetchPredictiveAnalytics();
  }, [patientData, symptomsAnalysis, riskAssessment, treatmentRecommendations]);

  if (loading) {
    return (
      <div className="text-center py-8">
        <FaChartArea className="mx-auto h-12 w-12 text-gray-300 mb-3 animate-spin" />
        <p className="body-large text-neutral-text-secondary">Analyzing potential complications...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <FaExclamationTriangle className="mx-auto h-12 w-12 text-amber-500 mb-3" />
        <p className="body-large text-neutral-text-secondary">{error}</p>
      </div>
    );
  }

  if (!analyticsData || !analyticsData.complication_predictions || analyticsData.complication_predictions.length === 0) {
    return (
      <div className="text-center py-8">
        <FaChartArea className="mx-auto h-12 w-12 text-gray-300 mb-3" />
        <p className="body-large text-neutral-text-secondary">
          No predictive analytics data available. This feature requires comprehensive patient data.
        </p>
      </div>
    );
  }

  // Sort by risk score
  const sortedPredictions = [...analyticsData.complication_predictions].sort((a, b) => b.risk_score - a.risk_score);
  
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="card">
          <div className="card-body text-center">
            <div className="text-3xl font-bold text-neutral-text">
              {analyticsData.total_predictions}
            </div>
            <div className="body-small text-neutral-text-secondary">
              Potential Complications
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-body text-center">
            <div className="text-3xl font-bold text-error">
              {sortedPredictions.filter(p => p.risk_level === 'high').length}
            </div>
            <div className="body-small text-neutral-text-secondary">
              High Risk Complications
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-body text-center">
            <div className="text-3xl font-bold text-warning">
              {sortedPredictions.filter(p => p.risk_level === 'moderate').length}
            </div>
            <div className="body-small text-neutral-text-secondary">
              Moderate Risk Complications
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {sortedPredictions.map((prediction, index) => (
          <div key={index} className="card">
            <div className="card-body">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="h3 text-neutral-text">{prediction.complication}</h3>
                  <div className="flex items-center mt-1">
                    <span className={`badge ${
                      prediction.risk_level === 'high' ? 'badge-error' :
                      prediction.risk_level === 'moderate' ? 'badge-warning' :
                      'badge-info'
                    }`}>
                      {prediction.risk_level} risk
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-neutral-text">
                    {prediction.risk_score.toFixed(1)}
                  </div>
                  <div className="text-sm text-neutral-text-secondary">Risk Score</div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <div>
                  <h4 className="font-medium text-neutral-text mb-2 flex items-center">
                    <FaChartArea className="mr-2" />
                    Risk Factors Present
                  </h4>
                  <div className="flex flex-wrap gap-1">
                    {prediction.risk_factors_present.map((factor, factorIndex) => (
                      <span key={factorIndex} className="badge badge-error text-xs">
                        {factor.replace('_', ' ')}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium text-neutral-text mb-2 flex items-center">
                    <FaChartArea className="mr-2" />
                    Indicators Present
                  </h4>
                  <div className="flex flex-wrap gap-1">
                    {prediction.indicators_present.map((indicator, indicatorIndex) => (
                      <span key={indicatorIndex} className="badge badge-warning text-xs">
                        {indicator.replace('_', ' ')}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
              
              <div className="mt-4 pt-4 border-t border-neutral-border">
                <h4 className="font-medium text-neutral-text mb-2 flex items-center">
                  <FaShieldAlt className="mr-2" />
                  Prevention Strategies
                </h4>
                <ul className="list-disc pl-5 space-y-1">
                  {prediction.prevention_strategies?.map((strategy, strategyIndex) => (
                    <li key={strategyIndex} className="body-small text-neutral-text-secondary">
                      {strategy}
                    </li>
                  ))}
                </ul>
              </div>
              
              <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                <h4 className="font-medium text-neutral-text mb-1">Monitoring Recommendation</h4>
                <p className="body-small text-neutral-text-secondary">
                  {prediction.monitoring_recommendations}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PredictiveAnalytics;