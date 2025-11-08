import { useState, useEffect } from "react";
import { FaBrain, FaExclamationTriangle, FaChartBar, FaRedo } from "react-icons/fa";
import { getDifferentialDiagnosis } from "../api";

const DifferentialDiagnosis = ({
  taskId,
  patientData,
  symptomsAnalysis,
  riskAssessment,
}) => {
  const [diagnosisData, setDiagnosisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [refreshCount, setRefreshCount] = useState(0);
  
  // Log props for debugging
  useEffect(() => {
    console.log("DifferentialDiagnosis props:", { taskId, patientData, symptomsAnalysis, riskAssessment });
  }, [taskId, patientData, symptomsAnalysis, riskAssessment]);

  useEffect(() => {
    const fetchDifferentialDiagnosis = async () => {
      if (!patientData) return;

      setLoading(true);
      setError(null);

      try {
        const requestData = {
          patient_data: patientData,
          symptoms_analysis: symptomsAnalysis || {},
          risk_assessment: riskAssessment || {},
        };
        
        console.log("Sending differential diagnosis request:", requestData);

        const response = await getDifferentialDiagnosis(requestData);
        console.log("Received differential diagnosis response:", response.data);
        if (response.data?.success) {
          setDiagnosisData(response.data.data);
          console.log("Set diagnosis data:", response.data.data);
        } else {
          setError("Failed to fetch differential diagnosis data");
        }
      } catch (err) {
        console.error("Error fetching differential diagnosis:", err);
        setError("Error fetching differential diagnosis data");
      } finally {
        setLoading(false);
      }
    };

    fetchDifferentialDiagnosis();
  }, [patientData, symptomsAnalysis, riskAssessment, refreshCount]);
  
  // Log when diagnosisData changes
  useEffect(() => {
    console.log("Diagnosis data updated:", diagnosisData);
  }, [diagnosisData]);
  
  const handleRefresh = () => {
    setRefreshCount(prev => prev + 1);
  };

  if (loading) {
    return (
      <div className="text-center py-8">
        <FaBrain className="mx-auto h-12 w-12 text-gray-300 mb-3 animate-spin" />
        <p className="body-large text-neutral-text-secondary">
          Analyzing differential diagnosis possibilities...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <FaExclamationTriangle className="mx-auto h-12 w-12 text-amber-500 mb-3" />
        <p className="body-large text-neutral-text-secondary">{error}</p>
        <button 
          onClick={handleRefresh}
          className="btn btn-secondary mt-4 flex items-center mx-auto"
        >
          <FaRedo className="mr-2" />
          Retry
        </button>
      </div>
    );
  }

  if (
    !diagnosisData ||
    !diagnosisData.differential_diagnosis ||
    diagnosisData.differential_diagnosis.length === 0
  ) {
    console.log("No diagnosis data to display:", diagnosisData);
    return (
      <div className="text-center py-8">
        <FaBrain className="mx-auto h-12 w-12 text-gray-300 mb-3" />
        <p className="body-large text-neutral-text-secondary">
          No differential diagnosis data available. This feature requires
          patient symptoms and clinical analysis.
        </p>
        <button 
          onClick={handleRefresh}
          className="btn btn-secondary mt-4 flex items-center mx-auto"
        >
          <FaRedo className="mr-2" />
          Retry
        </button>
      </div>
    );
  }
  
  console.log("Displaying diagnosis data:", diagnosisData);

  // Sort by match score
  const sortedDiagnoses = [...diagnosisData.differential_diagnosis].sort(
    (a, b) => b.match_score - a.match_score
  );
  
  console.log("Sorted diagnoses:", sortedDiagnoses);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="h2 text-neutral-text">Differential Diagnosis</h2>
        <button 
          onClick={handleRefresh}
          className="btn btn-secondary btn-sm flex items-center"
        >
          <FaRedo className="mr-1" />
          Refresh
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="card">
          <div className="card-body text-center">
            <div className="text-3xl font-bold text-neutral-text">
              {diagnosisData.total_possibilities}
            </div>
            <div className="body-small text-neutral-text-secondary">
              Possible Diagnoses
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-body text-center">
            <div className="text-3xl font-bold text-primary">
              {sortedDiagnoses[0]?.condition || "N/A"}
            </div>
            <div className="body-small text-neutral-text-secondary">
              Top Diagnosis
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-body text-center">
            <div className="text-3xl font-bold text-neutral-text">
              {(sortedDiagnoses[0]?.confidence_score * 100).toFixed(0)}%
            </div>
            <div className="body-small text-neutral-text-secondary">
              Confidence Level
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {sortedDiagnoses.map((diagnosis, index) => (
          <div key={index} className="card">
            <div className="card-body">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="h3 text-neutral-text">
                    {diagnosis.condition}
                  </h3>
                  <div className="flex items-center mt-1">
                    <span
                      className={`badge ${
                        diagnosis.severity === "high"
                          ? "badge-error"
                          : diagnosis.severity === "moderate"
                          ? "badge-warning"
                          : "badge-info"
                      }`}
                    >
                      {diagnosis.severity} severity
                    </span>
                    <span className="badge badge-secondary ml-2">
                      Prevalence: {(diagnosis.prevalence * 100).toFixed(0)}%
                    </span>
                    {diagnosis.code && (
                      <span className="badge badge-info ml-2">
                        Code: {diagnosis.code}
                      </span>
                    )}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-neutral-text">
                    {diagnosis.match_score.toFixed(1)}
                  </div>
                  <div className="text-sm text-neutral-text-secondary">
                    Match Score
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <div>
                  <h4 className="font-medium text-neutral-text mb-2 flex items-center">
                    <FaChartBar className="mr-2" />
                    Matched Symptoms
                  </h4>
                  <div className="flex flex-wrap gap-1">
                    {diagnosis.matched_symptoms.map((symptom, symIndex) => (
                      <span key={symIndex} className="badge badge-info text-xs">
                        {symptom}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-medium text-neutral-text mb-2 flex items-center">
                    <FaChartBar className="mr-2" />
                    Matched Vital Indicators
                  </h4>
                  <div className="flex flex-wrap gap-1">
                    {diagnosis.matched_vitals.map((vital, vitalIndex) => (
                      <span
                        key={vitalIndex}
                        className="badge badge-warning text-xs"
                      >
                        {vital.replace("_", " ")}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-neutral-border">
                <h4 className="font-medium text-neutral-text mb-2">
                  Recommended Actions
                </h4>
                <ul className="list-disc pl-5 space-y-1">
                  {diagnosis.recommendations?.map((rec, recIndex) => (
                    <li
                      key={recIndex}
                      className="body-small text-neutral-text-secondary"
                    >
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
              
              {diagnosis.description && (
                <div className="mt-4 pt-4 border-t border-neutral-border">
                  <h4 className="font-medium text-neutral-text mb-2">
                    Description
                  </h4>
                  <p className="body-small text-neutral-text-secondary">
                    {diagnosis.description}
                  </p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DifferentialDiagnosis;