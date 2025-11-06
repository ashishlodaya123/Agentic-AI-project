import { useState, useEffect } from "react";
import {
  FaPrescription,
  FaCalendarAlt,
  FaExclamationTriangle,
  FaUserMd,
  FaClipboardCheck,
  FaCapsules,
} from "react-icons/fa";

const AdvancedAgentResults = ({
  taskId,
  patientData,
  symptomsAnalysis,
  riskAssessment,
  treatmentRecommendations,
  followupPlan,
  drugInteractions,
  specialistRecommendations,
  qualityAssessment,
}) => {
  // Use the data passed from the parent component instead of fetching it
  const advancedResults = {
    treatment: treatmentRecommendations,
    followup: followupPlan,
    drugInteractions: drugInteractions,
    specialist: specialistRecommendations,
    quality: qualityAssessment,
  };

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const renderTreatmentRecommendations = (treatmentData) => {
    if (!treatmentData || !treatmentData.treatment_plan) return null;

    const plan = treatmentData.treatment_plan;

    return (
      <div className="space-y-6">
        <div>
          <h4 className="font-medium text-neutral-text mb-3">
            Primary Treatment Recommendations
          </h4>
          <ul className="list-disc pl-5 space-y-2">
            {plan.primary_recommendations?.map((rec, index) => (
              <li key={index} className="body-large text-neutral-text">
                {rec}
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h4 className="font-medium text-neutral-text mb-3">
            Secondary Interventions
          </h4>
          <ul className="list-disc pl-5 space-y-2">
            {plan.secondary_recommendations?.map((rec, index) => (
              <li key={index} className="body-large text-neutral-text">
                {rec}
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h4 className="font-medium text-neutral-text mb-3">Follow-up Care</h4>
          <ul className="list-disc pl-5 space-y-2">
            {plan.follow_up_recommendations?.map((rec, index) => (
              <li key={index} className="body-large text-neutral-text">
                {rec}
              </li>
            ))}
          </ul>
        </div>

        {plan.contraindications_checked &&
          plan.contraindications_checked.length > 0 && (
            <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg">
              <h4 className="font-medium text-neutral-text mb-2 flex items-center">
                <FaExclamationTriangle className="mr-2 text-amber-600" />
                Contraindications Checked
              </h4>
              <ul className="list-disc pl-5 space-y-1">
                {plan.contraindications_checked.map(
                  (contraindication, index) => (
                    <li
                      key={index}
                      className="body-small text-neutral-text-secondary"
                    >
                      {contraindication.medication}: {contraindication.reason}
                    </li>
                  )
                )}
              </ul>
            </div>
          )}

        {treatmentData.confidence_score && (
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex justify-between items-center">
              <span className="font-medium text-neutral-text">
                Confidence Score
              </span>
              <span className="font-bold text-primary">
                {treatmentData.confidence_score.toFixed(2)}
              </span>
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderFollowupPlan = (followupData) => {
    if (!followupData || !followupData.followup_schedule) return null;

    const schedule = followupData.followup_schedule;

    return (
      <div className="space-y-6">
        {schedule.immediate_followup &&
          schedule.immediate_followup.length > 0 && (
            <div>
              <h4 className="font-medium text-neutral-text mb-3 flex items-center">
                <FaClipboardCheck className="mr-2 text-red-600" />
                Immediate Follow-up (Next 24 hours)
              </h4>
              <div className="space-y-3">
                {schedule.immediate_followup.map((followup, index) => (
                  <div
                    key={index}
                    className="p-4 bg-red-50 border border-red-200 rounded-lg"
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h5 className="font-medium text-neutral-text">
                          {followup.condition}
                        </h5>
                        <p className="body-small text-neutral-text-secondary mt-1">
                          {followup.parameters?.join(", ")}
                        </p>
                      </div>
                      <span className="badge badge-error">
                        {followup.urgency}
                      </span>
                    </div>
                    <div className="mt-2 flex items-center text-sm text-neutral-text-secondary">
                      <FaCalendarAlt className="mr-1" />
                      Frequency: {followup.frequency} for {followup.duration}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

        {schedule.short_term_followup &&
          schedule.short_term_followup.length > 0 && (
            <div>
              <h4 className="font-medium text-neutral-text mb-3 flex items-center">
                <FaCalendarAlt className="mr-2 text-amber-600" />
                Short-term Follow-up (1-4 weeks)
              </h4>
              <div className="space-y-3">
                {schedule.short_term_followup.map((followup, index) => (
                  <div
                    key={index}
                    className="p-4 bg-amber-50 border border-amber-200 rounded-lg"
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h5 className="font-medium text-neutral-text">
                          {followup.condition}
                        </h5>
                        <p className="body-small text-neutral-text-secondary mt-1">
                          {followup.parameters?.join(", ")}
                        </p>
                      </div>
                      <span className="badge badge-warning">
                        {followup.urgency}
                      </span>
                    </div>
                    <div className="mt-2 flex items-center text-sm text-neutral-text-secondary">
                      <FaCalendarAlt className="mr-1" />
                      Frequency: {followup.frequency} for {followup.duration}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

        {schedule.long_term_followup &&
          schedule.long_term_followup.length > 0 && (
            <div>
              <h4 className="font-medium text-neutral-text mb-3 flex items-center">
                <FaCalendarAlt className="mr-2 text-green-600" />
                Long-term Follow-up (1+ months)
              </h4>
              <div className="space-y-3">
                {schedule.long_term_followup.map((followup, index) => (
                  <div
                    key={index}
                    className="p-4 bg-green-50 border border-green-200 rounded-lg"
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h5 className="font-medium text-neutral-text">
                          {followup.condition}
                        </h5>
                        <p className="body-small text-neutral-text-secondary mt-1">
                          {followup.parameters?.join(", ")}
                        </p>
                      </div>
                      <span className="badge badge-success">
                        {followup.urgency}
                      </span>
                    </div>
                    <div className="mt-2 flex items-center text-sm text-neutral-text-secondary">
                      <FaCalendarAlt className="mr-1" />
                      Frequency: {followup.frequency} for {followup.duration}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

        {schedule.special_considerations &&
          schedule.special_considerations.length > 0 && (
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="font-medium text-neutral-text mb-2">
                Special Considerations
              </h4>
              <ul className="list-disc pl-5 space-y-1">
                {schedule.special_considerations.map((consideration, index) => (
                  <li
                    key={index}
                    className="body-small text-neutral-text-secondary"
                  >
                    <strong>{consideration.type}:</strong>{" "}
                    {consideration.consideration} -{" "}
                    {consideration.recommendation}
                  </li>
                ))}
              </ul>
            </div>
          )}

        {schedule.monitoring_parameters &&
          Object.keys(schedule.monitoring_parameters).length > 0 && (
            <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
              <h4 className="font-medium text-neutral-text mb-2">
                Monitoring Parameters
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {Object.entries(schedule.monitoring_parameters).map(
                  ([category, parameters]) => (
                    <div key={category} className="mb-2">
                      <h5 className="font-medium text-neutral-text capitalize">
                        {category}
                      </h5>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {parameters.map((param, idx) => (
                          <span
                            key={idx}
                            className="badge badge-secondary text-xs"
                          >
                            {param}
                          </span>
                        ))}
                      </div>
                    </div>
                  )
                )}
              </div>
            </div>
          )}

        {followupData.confidence_score && (
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex justify-between items-center">
              <span className="font-medium text-neutral-text">
                Confidence Score
              </span>
              <span className="font-bold text-primary">
                {followupData.confidence_score.toFixed(2)}
              </span>
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderDrugInteractions = (interactionData) => {
    if (!interactionData || !interactionData.safety_assessment) return null;

    const assessment = interactionData.safety_assessment;

    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div>
            <h4 className="font-medium text-neutral-text">
              Overall Safety Assessment
            </h4>
            <p className="body-small text-neutral-text-secondary">
              Confidence Score: {interactionData.confidence_score}
            </p>
          </div>
          <span
            className={`badge ${
              assessment.overall_safety_level === "unsafe"
                ? "badge-error"
                : assessment.overall_safety_level === "caution"
                ? "badge-warning"
                : "badge-success"
            }`}
          >
            {assessment.overall_safety_level?.toUpperCase()}
          </span>
        </div>

        {assessment.high_risk_interactions &&
          assessment.high_risk_interactions.length > 0 && (
            <div>
              <h4 className="font-medium text-neutral-text mb-3 flex items-center text-red-600">
                <FaExclamationTriangle className="mr-2" />
                High-Risk Drug Interactions
              </h4>
              <div className="space-y-3">
                {assessment.high_risk_interactions.map((interaction, index) => (
                  <div
                    key={index}
                    className="p-4 bg-red-50 border border-red-200 rounded-lg"
                  >
                    <h5 className="font-medium text-neutral-text">
                      {interaction.drug1} + {interaction.drug2}
                    </h5>
                    <p className="body-small text-neutral-text-secondary mt-1">
                      {interaction.description}
                    </p>
                    <div className="mt-2 p-2 bg-red-100 rounded">
                      <p className="body-small font-medium text-red-800">
                        {interaction.management}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

        {assessment.moderate_risk_interactions &&
          assessment.moderate_risk_interactions.length > 0 && (
            <div>
              <h4 className="font-medium text-neutral-text mb-3 flex items-center text-amber-600">
                <FaExclamationTriangle className="mr-2" />
                Moderate-Risk Drug Interactions
              </h4>
              <div className="space-y-3">
                {assessment.moderate_risk_interactions.map(
                  (interaction, index) => (
                    <div
                      key={index}
                      className="p-4 bg-amber-50 border border-amber-200 rounded-lg"
                    >
                      <h5 className="font-medium text-neutral-text">
                        {interaction.drug1} + {interaction.drug2}
                      </h5>
                      <p className="body-small text-neutral-text-secondary mt-1">
                        {interaction.description}
                      </p>
                      <div className="mt-2 p-2 bg-amber-100 rounded">
                        <p className="body-small font-medium text-amber-800">
                          {interaction.management}
                        </p>
                      </div>
                    </div>
                  )
                )}
              </div>
            </div>
          )}

        {assessment.recommendations &&
          assessment.recommendations.length > 0 && (
            <div>
              <h4 className="font-medium text-neutral-text mb-3">
                Safety Recommendations
              </h4>
              <ul className="list-disc pl-5 space-y-2">
                {assessment.recommendations.map((rec, index) => (
                  <li key={index} className="body-large text-neutral-text">
                    {rec}
                  </li>
                ))}
              </ul>
            </div>
          )}

        {assessment.patient_specific_risks &&
          assessment.patient_specific_risks.length > 0 && (
            <div className="p-4 bg-indigo-50 border border-indigo-200 rounded-lg">
              <h4 className="font-medium text-neutral-text mb-2">
                Patient-Specific Risks
              </h4>
              <ul className="list-disc pl-5 space-y-1">
                {assessment.patient_specific_risks.map((risk, index) => (
                  <li
                    key={index}
                    className="body-small text-neutral-text-secondary"
                  >
                    {risk}
                  </li>
                ))}
              </ul>
            </div>
          )}
      </div>
    );
  };

  const renderSpecialistRecommendations = (specialistData) => {
    if (!specialistData || !specialistData.specialist_recommendations)
      return null;

    const recommendations = specialistData.specialist_recommendations;

    return (
      <div className="space-y-6">
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex justify-between items-center">
            <div>
              <h4 className="font-medium text-neutral-text">
                Patient Complexity Level
              </h4>
              <p className="body-small text-neutral-text-secondary">
                {recommendations.complexity_level
                  ?.replace("_", " ")
                  .toUpperCase()}
              </p>
            </div>
            <span className="badge badge-info">
              Confidence: {specialistData.confidence_score}
            </span>
          </div>
        </div>

        {recommendations.specialist_recommendations &&
          recommendations.specialist_recommendations.length > 0 && (
            <div>
              <h4 className="font-medium text-neutral-text mb-3">
                Specialist Consultation Recommendations
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {recommendations.specialist_recommendations.map(
                  (rec, index) => (
                    <div key={index} className="card">
                      <div className="card-body">
                        <div className="flex justify-between items-start mb-3">
                          <h5 className="h5 text-neutral-text flex items-center">
                            <FaUserMd className="mr-2 text-primary" />
                            {rec.specialist}
                          </h5>
                          <span
                            className={`badge ${
                              rec.urgency === "immediate"
                                ? "badge-error"
                                : rec.urgency === "urgent"
                                ? "badge-warning"
                                : "badge-info"
                            }`}
                          >
                            {rec.urgency}
                          </span>
                        </div>

                        <div className="mb-3">
                          <p className="body-small text-neutral-text-secondary">
                            <strong>Conditions:</strong>{" "}
                            {rec.conditions?.join(", ")}
                          </p>
                          <p className="body-small text-neutral-text-secondary mt-1">
                            <strong>Timing:</strong> {rec.urgency_description}
                          </p>
                        </div>

                        <div className="p-3 bg-neutral-surface rounded">
                          <p className="body-small text-neutral-text">
                            {rec.consultation_details}
                          </p>
                        </div>

                        <div className="mt-3 p-2 bg-blue-50 rounded">
                          <p className="body-small text-neutral-text-secondary italic">
                            {rec.reasoning}
                          </p>
                        </div>
                      </div>
                    </div>
                  )
                )}
              </div>
            </div>
          )}

        {recommendations.additional_considerations &&
          recommendations.additional_considerations.length > 0 && (
            <div>
              <h4 className="font-medium text-neutral-text mb-3">
                Additional Considerations
              </h4>
              <ul className="list-disc pl-5 space-y-1">
                {recommendations.additional_considerations.map(
                  (consideration, index) => (
                    <li key={index} className="body-large text-neutral-text">
                      {consideration}
                    </li>
                  )
                )}
              </ul>
            </div>
          )}

        {recommendations.comorbidities &&
          recommendations.comorbidities.length > 0 && (
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
              <h4 className="font-medium text-neutral-text mb-2">
                Identified Comorbidities
              </h4>
              <div className="flex flex-wrap gap-2">
                {recommendations.comorbidities.map((comorbidity, index) => (
                  <span key={index} className="badge badge-success">
                    {comorbidity}
                  </span>
                ))}
              </div>
            </div>
          )}
      </div>
    );
  };

  const renderQualityAssessment = (qualityData) => {
    if (!qualityData || !qualityData.qa_report) return null;

    const report = qualityData.qa_report;

    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div>
            <h4 className="font-medium text-neutral-text">
              Quality Assessment Report
            </h4>
            <p className="body-small text-neutral-text-secondary">
              Generated: {new Date(report.timestamp).toLocaleString()}
            </p>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-neutral-text">
              {report.overall_quality_score}
            </div>
            <div className="text-sm text-neutral-text-secondary">
              Quality Score
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="card">
            <div className="card-body text-center">
              <div className="text-3xl font-bold text-primary">
                {report.component_scores?.completeness || 0}
              </div>
              <div className="body-small text-neutral-text-secondary">
                Completeness
              </div>
            </div>
          </div>
          <div className="card">
            <div className="card-body text-center">
              <div className="text-3xl font-bold text-primary">
                {report.component_scores?.consistency || 0}
              </div>
              <div className="body-small text-neutral-text-secondary">
                Consistency
              </div>
            </div>
          </div>
          <div className="card">
            <div className="card-body text-center">
              <div className="text-3xl font-bold text-primary">
                {report.component_scores?.safety || 0}
              </div>
              <div className="body-small text-neutral-text-secondary">
                Safety
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-body">
            <h4 className="font-medium text-neutral-text mb-3">
              Issues Summary
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
              <div className="text-center p-3 bg-red-50 rounded">
                <div className="text-xl font-bold text-red-600">
                  {report.issues_summary?.high_severity || 0}
                </div>
                <div className="body-small text-neutral-text-secondary">
                  High Severity
                </div>
              </div>
              <div className="text-center p-3 bg-amber-50 rounded">
                <div className="text-xl font-bold text-amber-600">
                  {report.issues_summary?.moderate_severity || 0}
                </div>
                <div className="body-small text-neutral-text-secondary">
                  Moderate
                </div>
              </div>
              <div className="text-center p-3 bg-blue-50 rounded">
                <div className="text-xl font-bold text-blue-600">
                  {report.issues_summary?.low_severity || 0}
                </div>
                <div className="body-small text-neutral-text-secondary">
                  Low Severity
                </div>
              </div>
              <div className="text-center p-3 bg-neutral-surface rounded">
                <div className="text-xl font-bold text-neutral-text">
                  {report.issues_summary?.total_issues || 0}
                </div>
                <div className="body-small text-neutral-text-secondary">
                  Total Issues
                </div>
              </div>
            </div>
          </div>
        </div>

        {report.improvement_suggestions &&
          report.improvement_suggestions.length > 0 && (
            <div>
              <h4 className="font-medium text-neutral-text mb-3">
                Improvement Suggestions
              </h4>
              <ul className="list-disc pl-5 space-y-2">
                {report.improvement_suggestions.map((suggestion, index) => (
                  <li key={index} className="body-large text-neutral-text">
                    {suggestion}
                  </li>
                ))}
              </ul>
            </div>
          )}

        {report.compliance_checks && report.compliance_checks.length > 0 && (
          <div className="card">
            <div className="card-body">
              <h4 className="font-medium text-neutral-text mb-3">
                Compliance Checks
              </h4>
              <div className="space-y-2">
                {report.compliance_checks.map((check, index) => (
                  <div
                    key={index}
                    className="flex items-center p-2 rounded border ${check.status === 'passed' ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}"
                  >
                    <span
                      className={`mr-2 ${
                        check.status === "passed"
                          ? "text-green-600"
                          : "text-red-600"
                      }`}
                    >
                      {check.status === "passed" ? "✓" : "✗"}
                    </span>
                    <span className="body-small text-neutral-text">
                      {check.description}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-8">
      {/* Treatment Recommendations */}
      <div className="card">
        <div className="card-header">
          <div className="flex items-center">
            <div className="bg-blue-100 p-2 rounded-lg mr-3">
              <FaPrescription className="h-5 w-5 text-blue-600" />
            </div>
            <h3 className="h3 text-neutral-text">Treatment Recommendations</h3>
          </div>
        </div>
        <div className="card-body">
          {advancedResults.treatment ? (
            renderTreatmentRecommendations(advancedResults.treatment)
          ) : (
            <div className="text-center py-8 text-neutral-text-secondary">
              <FaPrescription className="mx-auto h-12 w-12 text-gray-300 mb-3" />
              <p>
                Treatment recommendations will be generated based on patient
                data and clinical analysis.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Follow-up Plan */}
      <div className="card">
        <div className="card-header">
          <div className="flex items-center">
            <div className="bg-green-100 p-2 rounded-lg mr-3">
              <FaCalendarAlt className="h-5 w-5 text-green-600" />
            </div>
            <h3 className="h3 text-neutral-text">Follow-up Care Plan</h3>
          </div>
        </div>
        <div className="card-body">
          {advancedResults.followup ? (
            renderFollowupPlan(advancedResults.followup)
          ) : (
            <div className="text-center py-8 text-neutral-text-secondary">
              <FaCalendarAlt className="mx-auto h-12 w-12 text-gray-300 mb-3" />
              <p>
                Follow-up care plan will be generated to ensure proper patient
                monitoring and care continuity.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Drug Interactions */}
      <div className="card">
        <div className="card-header">
          <div className="flex items-center">
            <div className="bg-amber-100 p-2 rounded-lg mr-3">
              <FaCapsules className="h-5 w-5 text-amber-600" />
            </div>
            <h3 className="h3 text-neutral-text">Drug Safety Assessment</h3>
          </div>
        </div>
        <div className="card-body">
          {advancedResults.drugInteractions ? (
            renderDrugInteractions(advancedResults.drugInteractions)
          ) : (
            <div className="text-center py-8 text-neutral-text-secondary">
              <FaCapsules className="mx-auto h-12 w-12 text-gray-300 mb-3" />
              <p>
                Drug interaction and safety assessment will identify potential
                contraindications and interactions.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Specialist Recommendations */}
      <div className="card">
        <div className="card-header">
          <div className="flex items-center">
            <div className="bg-purple-100 p-2 rounded-lg mr-3">
              <FaUserMd className="h-5 w-5 text-purple-600" />
            </div>
            <h3 className="h3 text-neutral-text">Specialist Consultation</h3>
          </div>
        </div>
        <div className="card-body">
          {advancedResults.specialist ? (
            renderSpecialistRecommendations(advancedResults.specialist)
          ) : (
            <div className="text-center py-8 text-neutral-text-secondary">
              <FaUserMd className="mx-auto h-12 w-12 text-gray-300 mb-3" />
              <p>
                Specialist consultation recommendations will be provided based
                on patient complexity and conditions.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Quality Assessment */}
      <div className="card">
        <div className="card-header">
          <div className="flex items-center">
            <div className="bg-indigo-100 p-2 rounded-lg mr-3">
              <FaClipboardCheck className="h-5 w-5 text-indigo-600" />
            </div>
            <h3 className="h3 text-neutral-text">Quality Assurance Report</h3>
          </div>
        </div>
        <div className="card-body">
          {advancedResults.quality ? (
            renderQualityAssessment(advancedResults.quality)
          ) : (
            <div className="text-center py-8 text-neutral-text-secondary">
              <FaClipboardCheck className="mx-auto h-12 w-12 text-gray-300 mb-3" />
              <p>
                Quality assurance report will verify the completeness and
                consistency of all clinical recommendations.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdvancedAgentResults;
