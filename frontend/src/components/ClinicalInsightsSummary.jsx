import { FaBrain, FaChartArea, FaHeartbeat, FaExclamationTriangle } from 'react-icons/fa';

const ClinicalInsightsSummary = ({ differentialDiagnosis, predictiveAnalytics, vitalSignsData, riskAssessment }) => {
  // Get top diagnosis
  const topDiagnosis = differentialDiagnosis?.differential_diagnosis?.[0] || null;
  
  // Get high risk predictions
  const highRiskPredictions = predictiveAnalytics?.complication_predictions?.filter(p => p.risk_level === 'high') || [];
  
  // Get abnormal vitals
  const abnormalVitals = vitalSignsData?.data?.filter(v => v.status !== 'normal') || [];
  
  // Get risk level
  const riskScore = riskAssessment?.risk_score || 0;
  const riskLevel = riskScore > 0.7 ? 'high' : riskScore > 0.4 ? 'moderate' : 'low';

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {/* Top Diagnosis Card */}
      <div className="card">
        <div className="card-body">
          <div className="flex items-center mb-3">
            <div className="bg-indigo-100 p-2 rounded-lg mr-3">
              <FaBrain className="h-5 w-5 text-indigo-600" />
            </div>
            <h3 className="font-medium text-neutral-text">Top Diagnosis</h3>
          </div>
          {topDiagnosis ? (
            <>
              <div className="text-lg font-bold text-neutral-text truncate">
                {topDiagnosis.condition}
              </div>
              <div className="flex items-center mt-1">
                <span className={`badge ${
                  topDiagnosis.severity === 'high' ? 'badge-error' :
                  topDiagnosis.severity === 'moderate' ? 'badge-warning' :
                  'badge-info'
                } text-xs`}>
                  {topDiagnosis.severity}
                </span>
                <span className="badge badge-secondary text-xs ml-2">
                  {(topDiagnosis.confidence_score * 100).toFixed(0)}% confidence
                </span>
              </div>
            </>
          ) : (
            <div className="text-neutral-text-secondary text-sm">
              Not available
            </div>
          )}
        </div>
      </div>

      {/* High Risk Complications Card */}
      <div className="card">
        <div className="card-body">
          <div className="flex items-center mb-3">
            <div className="bg-red-100 p-2 rounded-lg mr-3">
              <FaExclamationTriangle className="h-5 w-5 text-red-600" />
            </div>
            <h3 className="font-medium text-neutral-text">High Risk Issues</h3>
          </div>
          {highRiskPredictions.length > 0 ? (
            <>
              <div className="text-lg font-bold text-error">
                {highRiskPredictions.length} complications
              </div>
              <div className="text-sm text-neutral-text-secondary mt-1">
                Requiring immediate attention
              </div>
            </>
          ) : (
            <div className="text-neutral-text-secondary text-sm">
              No high risk complications
            </div>
          )}
        </div>
      </div>

      {/* Abnormal Vitals Card */}
      <div className="card">
        <div className="card-body">
          <div className="flex items-center mb-3">
            <div className="bg-amber-100 p-2 rounded-lg mr-3">
              <FaHeartbeat className="h-5 w-5 text-amber-600" />
            </div>
            <h3 className="font-medium text-neutral-text">Abnormal Vitals</h3>
          </div>
          {abnormalVitals.length > 0 ? (
            <>
              <div className="text-lg font-bold text-warning">
                {abnormalVitals.length} vitals
              </div>
              <div className="text-sm text-neutral-text-secondary mt-1">
                Outside normal range
              </div>
            </>
          ) : (
            <div className="text-neutral-text-secondary text-sm">
              All vitals normal
            </div>
          )}
        </div>
      </div>

      {/* Overall Risk Card */}
      <div className="card">
        <div className="card-body">
          <div className="flex items-center mb-3">
            <div className="bg-blue-100 p-2 rounded-lg mr-3">
              <FaChartArea className="h-5 w-5 text-blue-600" />
            </div>
            <h3 className="font-medium text-neutral-text">Overall Risk</h3>
          </div>
          <div className={`text-lg font-bold ${
            riskLevel === 'high' ? 'text-error' :
            riskLevel === 'moderate' ? 'text-warning' :
            'text-success'
          }`}>
            {riskLevel.charAt(0).toUpperCase() + riskLevel.slice(1)} risk
          </div>
          <div className="text-sm text-neutral-text-secondary mt-1">
            Risk score: {riskScore.toFixed(2)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClinicalInsightsSummary;