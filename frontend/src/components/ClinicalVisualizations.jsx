import { useState, useEffect } from 'react';
import { 
  FaHeartbeat, FaExclamationTriangle, FaCalendarAlt, 
  FaUserMd, FaChartLine, FaChartPie, FaChartBar
} from 'react-icons/fa';
import { getClinicalVisualization } from '../api';

const ClinicalVisualizations = ({ taskId, patientData, symptomsAnalysis, riskAssessment, 
                                treatmentRecommendations, followupPlan, drugInteractions, 
                                specialistRecommendations }) => {
  const [visualizationData, setVisualizationData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchVisualizationData = async () => {
      if (!patientData) return;
      
      setLoading(true);
      setError(null);
      
      // Debug: Log the data being sent
      console.log('Patient Data being sent:', patientData);
      console.log('Symptoms Analysis being sent:', symptomsAnalysis);
      console.log('Risk Assessment being sent:', riskAssessment);
      
      try {
        const requestData = {
          patient_data: patientData,
          symptoms_analysis: symptomsAnalysis || {},
          risk_assessment: riskAssessment || {},
          treatment_recommendations: treatmentRecommendations || {},
          followup_plan: followupPlan,
          drug_interactions: drugInteractions,
          specialist_recommendations: specialistRecommendations
        };
        
        const response = await getClinicalVisualization(requestData);
        console.log('Clinical Visualization Response:', response);
        if (response.data?.success) {
          console.log('Visualization Data:', response.data.data);
          setVisualizationData(response.data.data);
        } else {
          setError('Failed to fetch visualization data');
        }
      } catch (err) {
        console.error('Error fetching visualization data:', err);
        setError('Error fetching visualization data');
      } finally {
        setLoading(false);
      }
    };
    
    fetchVisualizationData();
  }, [patientData, symptomsAnalysis, riskAssessment, treatmentRecommendations, followupPlan, drugInteractions, specialistRecommendations]);

  // Render vital signs chart
  const renderVitalSignsChart = (vitalData) => {
    console.log('Vital Signs Data:', vitalData); // Debug log
    if (!vitalData || !vitalData.data || vitalData.data.length === 0) {
      return (
        <div className="card">
          <div className="card-header">
            <div className="flex items-center">
              <div className="bg-red-100 p-2 rounded-lg mr-3">
                <FaHeartbeat className="h-5 w-5 text-red-600" />
              </div>
              <h3 className="h3 text-neutral-text">Vital Signs Overview</h3>
            </div>
          </div>
          <div className="card-body">
            <div className="text-center py-8 text-neutral-text-secondary">
              <FaHeartbeat className="mx-auto h-12 w-12 text-gray-300 mb-3" />
              <p>No vital signs data available for visualization.</p>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="card">
        <div className="card-header">
          <div className="flex items-center">
            <div className="bg-red-100 p-2 rounded-lg mr-3">
              <FaHeartbeat className="h-5 w-5 text-red-600" />
            </div>
            <h3 className="h3 text-neutral-text">{vitalData.title}</h3>
          </div>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {vitalData.data.map((vital, index) => (
              <div key={index} className="border border-neutral-border rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <h4 className="font-medium text-neutral-text">{vital.metric}</h4>
                  <span className={`badge ${
                    vital.status === 'normal' ? 'badge-success' :
                    vital.status === 'high' ? 'badge-error' :
                    'badge-warning'
                  }`}>
                    {vital.status}
                  </span>
                </div>
                <div className="text-2xl font-bold text-neutral-text mb-1">
                  {vital.value} <span className="text-sm font-normal text-neutral-text-secondary">{vital.unit}</span>
                </div>
                <div className="text-sm text-neutral-text-secondary">
                  Normal: {vital.normal_range[0]}-{vital.normal_range[1]} {vital.unit}
                </div>
                <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${
                      vital.status === 'normal' ? 'bg-green-500' :
                      vital.status === 'high' ? 'bg-red-500' :
                      'bg-amber-500'
                    }`}
                    style={{ 
                      width: `${Math.min(100, Math.max(0, 
                        ((vital.value - vital.normal_range[0]) / 
                        (vital.normal_range[1] - vital.normal_range[0])) * 100
                      ))}%` 
                    }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // Render risk stratification chart
  const renderRiskChart = (riskData) => {
    console.log('Risk Data:', riskData); // Debug log
    if (!riskData || !riskData.risk_factors || riskData.risk_factors.length === 0) {
      return (
        <div className="card">
          <div className="card-header">
            <div className="flex items-center">
              <div className="bg-amber-100 p-2 rounded-lg mr-3">
                <FaExclamationTriangle className="h-5 w-5 text-amber-600" />
              </div>
              <h3 className="h3 text-neutral-text">Risk Stratification Analysis</h3>
            </div>
          </div>
          <div className="card-body">
            <div className="text-center py-8 text-neutral-text-secondary">
              <FaExclamationTriangle className="mx-auto h-12 w-12 text-gray-300 mb-3" />
              <p>No risk factors data available for visualization.</p>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="card">
        <div className="card-header">
          <div className="flex items-center">
            <div className="bg-amber-100 p-2 rounded-lg mr-3">
              <FaExclamationTriangle className="h-5 w-5 text-amber-600" />
            </div>
            <h3 className="h3 text-neutral-text">{riskData.title}</h3>
          </div>
        </div>
        <div className="card-body">
          <div className="mb-4 p-4 bg-blue-50 rounded-lg">
            <div className="flex justify-between items-center">
              <span className="font-medium text-neutral-text">Overall Risk Score</span>
              <span className="text-2xl font-bold text-neutral-text">{riskData.risk_score.toFixed(2)}</span>
            </div>
            <div className="mt-2">
              <span className="badge badge-error">{riskData.urgency_level}</span>
            </div>
          </div>
          
          <div className="space-y-3">
            <h4 className="font-medium text-neutral-text">Risk Factors</h4>
            {riskData.risk_factors.map((factor, index) => (
              <div key={index} className="border border-neutral-border rounded-lg p-3">
                <div className="flex justify-between items-center mb-2">
                  <h5 className="font-medium text-neutral-text">{factor.factor}</h5>
                  <span className="font-bold text-primary">{factor.weight.toFixed(2)}</span>
                </div>
                <p className="body-small text-neutral-text-secondary">{factor.description}</p>
                <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="h-2 rounded-full bg-primary"
                    style={{ width: `${Math.min(100, factor.weight * 100)}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // Render treatment timeline
  const renderTreatmentTimeline = (timelineData) => {
    if (!timelineData || !timelineData.events || timelineData.events.length === 0) {
      return (
        <div className="card">
          <div className="card-header">
            <div className="flex items-center">
              <div className="bg-green-100 p-2 rounded-lg mr-3">
                <FaCalendarAlt className="h-5 w-5 text-green-600" />
              </div>
              <h3 className="h3 text-neutral-text">Treatment and Follow-up Timeline</h3>
            </div>
          </div>
          <div className="card-body">
            <div className="text-center py-8 text-neutral-text-secondary">
              <FaCalendarAlt className="mx-auto h-12 w-12 text-gray-300 mb-3" />
              <p>No treatment timeline data available for visualization.</p>
            </div>
          </div>
        </div>
      );
    }

    // Group events by time
    const groupedEvents = timelineData.events.reduce((acc, event) => {
      if (!acc[event.time]) {
        acc[event.time] = [];
      }
      acc[event.time].push(event);
      return acc;
    }, {});

    return (
      <div className="card">
        <div className="card-header">
          <div className="flex items-center">
            <div className="bg-green-100 p-2 rounded-lg mr-3">
              <FaCalendarAlt className="h-5 w-5 text-green-600" />
            </div>
            <h3 className="h3 text-neutral-text">{timelineData.title}</h3>
          </div>
        </div>
        <div className="card-body">
          <div className="space-y-6">
            {Object.entries(groupedEvents).map(([time, events], timeIndex) => (
              <div key={timeIndex} className="border-l-2 border-primary pl-4 ml-3">
                <div className="mb-3">
                  <span className="badge badge-primary">{time}</span>
                </div>
                <div className="space-y-3">
                  {events.map((event, eventIndex) => (
                    <div key={eventIndex} className="border border-neutral-border rounded-lg p-3 ml-2">
                      <div className="flex justify-between items-start">
                        <div>
                          <h4 className="font-medium text-neutral-text">{event.event}</h4>
                          <div className="flex items-center mt-1">
                            <span className={`badge ${
                              event.priority === 'high' ? 'badge-error' :
                              event.priority === 'medium' ? 'badge-warning' :
                              'badge-info'
                            }`}>
                              {event.priority}
                            </span>
                            <span className="badge badge-secondary ml-2">{event.category}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // Render symptom distribution chart
  const renderSymptomChart = (symptomData) => {
    if (!symptomData || !symptomData.symptoms || symptomData.symptoms.length === 0) {
      return (
        <div className="card">
          <div className="card-header">
            <div className="flex items-center">
              <div className="bg-purple-100 p-2 rounded-lg mr-3">
                <FaChartPie className="h-5 w-5 text-purple-600" />
              </div>
              <h3 className="h3 text-neutral-text">Symptom Distribution by System</h3>
            </div>
          </div>
          <div className="card-body">
            <div className="text-center py-8 text-neutral-text-secondary">
              <FaChartPie className="mx-auto h-12 w-12 text-gray-300 mb-3" />
              <p>No symptom data available for visualization.</p>
            </div>
          </div>
        </div>
      );
    }

    // Calculate total symptoms
    const totalSymptoms = symptomData.symptoms.reduce((sum, item) => sum + item.count, 0);

    return (
      <div className="card">
        <div className="card-header">
          <div className="flex items-center">
            <div className="bg-purple-100 p-2 rounded-lg mr-3">
              <FaChartPie className="h-5 w-5 text-purple-600" />
            </div>
            <h3 className="h3 text-neutral-text">{symptomData.title}</h3>
          </div>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-3">
              {symptomData.symptoms.map((item, index) => {
                const percentage = totalSymptoms > 0 ? (item.count / totalSymptoms) * 100 : 0;
                return (
                  <div key={index} className="border border-neutral-border rounded-lg p-3">
                    <div className="flex justify-between items-center mb-1">
                      <h4 className="font-medium text-neutral-text">{item.category}</h4>
                      <span className="font-bold text-primary">{item.count}</span>
                    </div>
                    <div className="text-sm text-neutral-text-secondary mb-2">
                      {percentage.toFixed(1)}% of symptoms
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="h-2 rounded-full bg-primary"
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                    <div className="mt-2 flex flex-wrap gap-1">
                      {item.symptoms.map((symptom, symIndex) => (
                        <span key={symIndex} className="badge badge-info text-xs">
                          {symptom}
                        </span>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
            <div className="flex items-center justify-center">
              <div className="relative w-64 h-64">
                {symptomData.symptoms.map((item, index) => {
                  const percentage = totalSymptoms > 0 ? (item.count / totalSymptoms) * 100 : 0;
                  const rotation = symptomData.symptoms.slice(0, index).reduce((sum, prevItem) => {
                    return sum + (prevItem.count / totalSymptoms) * 360;
                  }, 0);
                  
                  // Simple pie chart segment (simplified representation)
                  return (
                    <div 
                      key={index}
                      className="absolute inset-0"
                      style={{
                        clipPath: `path('M 50,50 L 50,0 A 50,50 0 ${percentage > 50 ? 1 : 0},1 ${50 + 50 * Math.cos((rotation + percentage * 3.6 - 90) * Math.PI / 180)},${50 + 50 * Math.sin((rotation + percentage * 3.6 - 90) * Math.PI / 180)} Z')`,
                        backgroundColor: `hsl(${index * 60}, 70%, 50%)`
                      }}
                    ></div>
                  );
                })}
                <div className="absolute inset-8 bg-white rounded-full flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-neutral-text">{totalSymptoms}</div>
                    <div className="text-sm text-neutral-text-secondary">Total Symptoms</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Render patient summary
  const renderPatientSummary = (summaryData) => {
    if (!summaryData) {
      return (
        <div className="card">
          <div className="card-header">
            <div className="flex items-center">
              <div className="bg-blue-100 p-2 rounded-lg mr-3">
                <FaUserMd className="h-5 w-5 text-blue-600" />
              </div>
              <h3 className="h3 text-neutral-text">Patient Summary</h3>
            </div>
          </div>
          <div className="card-body">
            <div className="text-center py-8 text-neutral-text-secondary">
              <FaUserMd className="mx-auto h-12 w-12 text-gray-300 mb-3" />
              <p>No patient summary data available.</p>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="card">
        <div className="card-header">
          <div className="flex items-center">
            <div className="bg-blue-100 p-2 rounded-lg mr-3">
              <FaUserMd className="h-5 w-5 text-blue-600" />
            </div>
            <h3 className="h3 text-neutral-text">Patient Summary</h3>
          </div>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="border border-neutral-border rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-neutral-text">{summaryData.age}</div>
              <div className="body-small text-neutral-text-secondary">Age</div>
            </div>
            <div className="border border-neutral-border rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-neutral-text">{summaryData.gender}</div>
              <div className="body-small text-neutral-text-secondary">Gender</div>
            </div>
            <div className="border border-neutral-border rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-neutral-text">{summaryData.medical_history_count}</div>
              <div className="body-small text-neutral-text-secondary">Medical Conditions</div>
            </div>
            <div className="border border-neutral-border rounded-lg p-4">
              <div className="body-small text-neutral-text-secondary">Chief Complaint</div>
              <div className="text-neutral-text mt-1">{summaryData.chief_complaint}</div>
            </div>
          </div>
          
          {/* Additional patient information */}
          {summaryData.key_symptoms && summaryData.key_symptoms.length > 0 && (
            <div className="mt-4 pt-4 border-t border-neutral-border">
              <h4 className="font-medium text-neutral-text mb-2">Key Symptoms</h4>
              <div className="flex flex-wrap gap-1">
                {summaryData.key_symptoms.map((symptom, index) => (
                  <span key={index} className="badge badge-info text-xs">
                    {symptom}
                  </span>
                ))}
              </div>
            </div>
          )}
          
          {summaryData.vital_signs_summary && summaryData.vital_signs_summary !== "Not recorded" && (
            <div className="mt-3">
              <h4 className="font-medium text-neutral-text mb-1">Vital Signs</h4>
              <div className="body-small text-neutral-text-secondary">
                {summaryData.vital_signs_summary}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {loading ? (
        <div className="text-center py-8">
          <FaChartLine className="mx-auto h-12 w-12 text-gray-300 mb-3 animate-spin" />
          <p className="body-large text-neutral-text-secondary">Loading clinical visualizations...</p>
        </div>
      ) : error ? (
        <div className="text-center py-8">
          <FaExclamationTriangle className="mx-auto h-12 w-12 text-amber-500 mb-3" />
          <p className="body-large text-neutral-text-secondary">{error}</p>
        </div>
      ) : visualizationData ? (
        <>
          {renderPatientSummary(visualizationData.patient_summary)}
          {renderVitalSignsChart(visualizationData.vital_signs_chart)}
          {renderRiskChart(visualizationData.risk_stratification_chart)}
          {renderTreatmentTimeline(visualizationData.treatment_timeline)}
          {renderSymptomChart(visualizationData.symptom_progression)}
        </>
      ) : (
        <div className="text-center py-8">
          <FaChartLine className="mx-auto h-12 w-12 text-gray-300 mb-3" />
          <p className="body-large text-neutral-text-secondary">Clinical visualizations will be generated based on patient data and clinical analysis.</p>
        </div>
      )}
    </div>
  );
};

export default ClinicalVisualizations;