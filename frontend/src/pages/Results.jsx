import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  FaExclamationTriangle,
  FaExclamationCircle,
  FaInfoCircle,
  FaHeartbeat,
  FaFileMedical,
  FaBookMedical,
  FaPrint,
  FaUserMd,
  FaTemperatureHigh,
  FaTint,
  FaWeight,
  FaCheck,
  FaTimes,
  FaAmbulance,
  FaStethoscope,
  FaHospital,
  FaClock,
  FaPrescription,
  FaCalendarAlt,
  FaCapsules,
  FaClipboardCheck,
  FaBrain,
  FaChartArea,
  FaEdit,
  FaSave,
  FaLock,
  FaLockOpen
} from "react-icons/fa";
import { motion } from "framer-motion";
import { getTaskResult, saveClinicianReview, getClinicianReview } from "../api";
import AdvancedAgentResults from "../components/AdvancedAgentResults";
import ClinicalVisualizations from "../components/ClinicalVisualizations";
import DifferentialDiagnosis from "../components/DifferentialDiagnosis";
import PredictiveAnalytics from "../components/PredictiveAnalytics";

const Results = () => {
  const { taskId } = useParams();
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [clinicianReview, setClinicianReview] = useState({
    approved: false,
    notes: "",
    overrideRecommendations: false,
    modifiedUrgency: ""
  });
  const [isEditing, setIsEditing] = useState(false);
  const [reviewLoading, setReviewLoading] = useState(false);

  useEffect(() => {
    // Try to load cached result first
    const cachedResult = localStorage.getItem(`triage_result_${taskId}`);
    let initialResult = null;

    if (cachedResult) {
      try {
        initialResult = JSON.parse(cachedResult);
        setResult(initialResult);
        setLoading(false);
      } catch (e) {
        console.error("Error parsing cached result:", e);
      }
    }

    const pollResult = setInterval(() => {
      getTaskResult(taskId)
        .then((response) => {
          if (response.data.status === "Success") {
            // Cache the result with timestamp
            const resultToCache = {
              ...response.data.result,
              cachedAt: new Date().toISOString(),
            };
            localStorage.setItem(
              `triage_result_${taskId}`,
              JSON.stringify(resultToCache)
            );
            setResult(response.data.result);
            setLoading(false);
            clearInterval(pollResult);
          } else if (response.data.status === "Failed") {
            setError("Triage process failed.");
            setLoading(false);
            clearInterval(pollResult);
          }
        })
        .catch((err) => {
          // If we have cached data, use it even if API fails
          if (!initialResult) {
            setError("Error fetching results.");
            setLoading(false);
          }
          clearInterval(pollResult);
        });
    }, 2000); // Poll every 2 seconds

    // Load clinician review if it exists
    loadClinicianReview();

    return () => clearInterval(pollResult);
  }, [taskId]);

  const loadClinicianReview = async () => {
    try {
      const response = await getClinicianReview(taskId);
      if (response.data.status === "success" && response.data.data) {
        const reviewData = response.data.data;
        setClinicianReview({
          approved: reviewData.approved || false,
          notes: reviewData.notes || "",
          overrideRecommendations: reviewData.override_recommendations || false,
          modifiedUrgency: reviewData.modified_urgency || ""
        });
      }
    } catch (err) {
      console.log("No existing clinician review found");
    }
  };

  const handleStartNewTriage = () => {
    navigate("/triage");
  };

  const handlePrintReport = () => {
    window.print();
  };

  const handleApproveRecommendations = () => {
    setClinicianReview(prev => ({
      ...prev,
      approved: true
    }));
  };

  const handleRejectRecommendations = () => {
    setClinicianReview(prev => ({
      ...prev,
      approved: false
    }));
  };

  const handleSaveReview = async () => {
    setReviewLoading(true);
    try {
      const reviewData = {
        task_id: taskId,
        approved: clinicianReview.approved,
        notes: clinicianReview.notes,
        override_recommendations: clinicianReview.overrideRecommendations,
        modified_urgency: clinicianReview.modifiedUrgency
      };

      const response = await saveClinicianReview(reviewData);
      
      if (response.data.status === "success") {
        setIsEditing(false);
        alert("Review saved successfully!");
      } else {
        throw new Error(response.data.message || "Failed to save review");
      }
    } catch (err) {
      console.error("Error saving clinician review:", err);
      alert("Failed to save review. Please try again.");
    } finally {
      setReviewLoading(false);
    }
  };

  const handleEditReview = () => {
    setIsEditing(true);
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
            <h2 className="h2 text-neutral-text mb-2">
              Analyzing Patient Data
            </h2>
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
  if (!result || !result.result || !result.result.final_recommendation) {
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

  const finalRecommendation = result.result.final_recommendation;
  const symptomsAnalysis = finalRecommendation.patient_analysis || {};
  const ragResults = finalRecommendation.clinical_guidelines || [];
  const imagingAnalysis = finalRecommendation.imaging_analysis || {};
  const riskAssessment = finalRecommendation.risk_assessment || {};

  const getUrgencyConfig = (urgencyLevel) => {
    switch (urgencyLevel?.toLowerCase()) {
      case "red":
      case "critical":
        return {
          color: "text-red-800",
          bg: "bg-red-100",
          badge: "badge-error",
          border: "border-red-500",
          icon: FaAmbulance,
        };
      case "orange":
      case "high":
        return {
          color: "text-orange-800",
          bg: "bg-orange-100",
          badge: "badge-warning",
          border: "border-orange-500",
          icon: FaExclamationTriangle,
        };
      case "yellow":
      case "moderate":
        return {
          color: "text-amber-800",
          bg: "bg-amber-100",
          badge: "badge-warning",
          border: "border-amber-500",
          icon: FaInfoCircle,
        };
      case "green":
      case "low":
        return {
          color: "text-green-800",
          bg: "bg-green-100",
          badge: "badge-success",
          border: "border-green-500",
          icon: FaInfoCircle,
        };
      case "blue":
      case "minimal":
        return {
          color: "text-blue-800",
          bg: "bg-blue-100",
          badge: "badge-info",
          border: "border-blue-500",
          icon: FaInfoCircle,
        };
      default:
        return {
          color: "text-blue-800",
          bg: "bg-blue-100",
          badge: "badge-info",
          border: "border-blue-500",
          icon: FaInfoCircle,
        };
    }
  };

  const urgencyConfig = getUrgencyConfig(finalRecommendation.urgency_level);
  const UrgencyIcon = urgencyConfig.icon;

  const formatVitalSign = (name, vital) => {
    if (!vital) return null;

    const statusClass =
      vital.status === "normal"
        ? "text-green-600"
        : vital.status === "abnormal"
        ? "text-red-600"
        : "text-gray-500";

    const statusText =
      vital.status === "normal"
        ? "Normal"
        : vital.status === "abnormal"
        ? "Abnormal"
        : "Invalid";

    return (
      <div
        key={name}
        className="flex items-center justify-between py-2 border-b border-neutral-border"
      >
        <span className="body-large text-neutral-text capitalize">
          {name.replace("_", " ")}
        </span>
        <div className="flex items-center">
          <span className="font-medium mr-2">
            {vital.value} {vital.unit}
          </span>
          <span className={`text-sm ${statusClass}`}>{statusText}</span>
        </div>
      </div>
    );
  };

  const renderRiskFactors = (riskFactors) => {
    // Handle case where riskFactors might be undefined or null
    if (!riskFactors || typeof riskFactors !== "object") return null;

    // Get all keys that have actual values
    const validKeys = Object.keys(riskFactors).filter((key) => {
      const value = riskFactors[key];
      return value !== undefined && value !== null && value !== "";
    });

    if (validKeys.length === 0) {
      return (
        <div className="text-neutral-text-secondary italic">
          No specific risk factors identified
        </div>
      );
    }

    return (
      <div className="space-y-3">
        {validKeys.map((key) => {
          const value = riskFactors[key];
          const displayName = key
            .replace(/_/g, " ")
            .replace(/\b\w/g, (l) => l.toUpperCase());

          // Handle different value types
          if (Array.isArray(value)) {
            if (value.length === 0) return null;
            return (
              <div key={key} className="mb-2">
                <h5 className="font-medium text-neutral-text">{displayName}</h5>
                <ul className="list-disc pl-5 mt-1 space-y-1">
                  {value.map((item, idx) => (
                    <li
                      key={idx}
                      className="body-small text-neutral-text-secondary"
                    >
                      {typeof item === "string"
                        ? item
                        : typeof item === "object"
                        ? item.symptom || item.name || JSON.stringify(item)
                        : String(item)}
                    </li>
                  ))}
                </ul>
              </div>
            );
          } else if (typeof value === "object" && value !== null) {
            // Handle nested objects
            const nestedKeys = Object.keys(value).filter(
              (nestedKey) =>
                value[nestedKey] !== undefined &&
                value[nestedKey] !== null &&
                value[nestedKey] !== ""
            );

            if (nestedKeys.length === 0) return null;

            return (
              <div key={key} className="mb-2">
                <h5 className="font-medium text-neutral-text">{displayName}</h5>
                <div className="grid grid-cols-2 gap-2 mt-1">
                  {nestedKeys.map((nestedKey) => {
                    const nestedValue = value[nestedKey];
                    const nestedDisplayName = nestedKey
                      .replace(/_/g, " ")
                      .replace(/\b\w/g, (l) => l.toUpperCase());
                    return (
                      <div key={nestedKey} className="flex justify-between">
                        <span className="body-small text-neutral-text-secondary">
                          {nestedDisplayName}
                        </span>
                        <span className="body-small text-neutral-text font-medium">
                          {typeof nestedValue === "number"
                            ? nestedValue.toFixed(2)
                            : String(nestedValue)}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          } else {
            // Handle primitive values
            if (value === 0 || value === "") return null;
            return (
              <div key={key} className="flex justify-between">
                <span className="body-small text-neutral-text-secondary">
                  {displayName}
                </span>
                <span className="body-small text-neutral-text font-medium">
                  {typeof value === "number" ? value.toFixed(2) : String(value)}
                </span>
              </div>
            );
          }
        })}
      </div>
    );
  };

  return (
    <div className="max-w-6xl mx-auto print:max-w-full">
      <div className="mb-6">
        <h1 className="h1 text-neutral-text">
          Comprehensive Clinical Triage Report
        </h1>
        <p className="body-large text-neutral-text-secondary mt-2">
          AI-powered clinical decision support with integrated medical
          literature and guidelines
        </p>
      </div>

      {/* Final Recommendation */}
      <div className="card mb-8">
        <div className="card-header">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <h2 className="h2 text-neutral-text">Clinical Decision Summary</h2>
            <span
              className={`badge ${urgencyConfig.badge} mt-2 md:mt-0 flex items-center text-lg py-2 px-4`}
            >
              <UrgencyIcon className="mr-2" />
              {finalRecommendation.urgency_level} Priority -{" "}
              {finalRecommendation.priority} Care
            </span>
          </div>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <h3 className="h3 text-neutral-text mb-4">
                Triage Recommendation
              </h3>
              <p className="body-large text-neutral-text mb-6">
                {finalRecommendation.recommended_action}
              </p>

              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-neutral-text mb-2">
                    Next Steps
                  </h4>
                  <ul className="list-disc pl-5 space-y-2">
                    {finalRecommendation.next_steps?.map((step, index) => (
                      <li
                        key={index}
                        className="body-large text-neutral-text-secondary"
                      >
                        {step}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            <div>
              <h3 className="h3 text-neutral-text mb-4">Risk Assessment</h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="body-small text-neutral-text-secondary">
                      Risk Score
                    </span>
                    <span className="font-medium text-neutral-text">
                      {(
                        riskAssessment.risk_score ||
                        finalRecommendation.risk_score ||
                        0
                      ).toFixed(3)}
                    </span>
                  </div>
                  <div className="w-full bg-neutral-border rounded-full h-2.5">
                    <div
                      className="bg-primary h-2.5 rounded-full"
                      style={{
                        width: `${
                          (riskAssessment.risk_score ||
                            finalRecommendation.risk_score) * 100
                        }%`,
                      }}
                    ></div>
                  </div>
                  <div className="flex justify-between mt-1">
                    <span className="text-xs text-neutral-text-secondary">
                      0.0
                    </span>
                    <span className="text-xs text-neutral-text-secondary">
                      1.0
                    </span>
                  </div>
                </div>

                <div className="pt-4 border-t border-neutral-border">
                  <div className="flex justify-between">
                    <span className="body-small text-neutral-text-secondary">
                      Risk Category
                    </span>
                    <span className="font-medium text-neutral-text">
                      {riskAssessment.risk_category || "Not assessed"}
                    </span>
                  </div>
                  <div className="flex justify-between mt-2">
                    <span className="body-small text-neutral-text-secondary">
                      Action Required
                    </span>
                    <span className="font-medium text-neutral-text">
                      {finalRecommendation.recommended_action}
                    </span>
                  </div>
                  <div className="flex justify-between mt-2">
                    <span className="body-small text-neutral-text-secondary">
                      Timeframe
                    </span>
                    <span className="font-medium text-neutral-text">
                      {riskAssessment.triage_recommendation?.timeframe ||
                        "As clinically indicated"}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Human-in-the-Loop Review Section */}
      <div className="card mb-8">
        <div className="card-header">
          <div className="flex items-center">
            <div className="bg-purple-100 p-2 rounded-lg mr-3">
              <FaUserMd className="h-5 w-5 text-purple-600" />
            </div>
            <h3 className="h3 text-neutral-text">Clinician Review & Approval</h3>
          </div>
        </div>
        <div className="card-body">
          {isEditing ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h4 className="font-medium text-neutral-text">
                  Review Recommendations
                </h4>
                <div className="flex space-x-2">
                  <button
                    onClick={() => setClinicianReview(prev => ({ ...prev, approved: true }))}
                    className={`btn ${clinicianReview.approved ? 'btn-success' : 'btn-outline'}`}
                  >
                    <FaCheck className="mr-2" />
                    Approve
                  </button>
                  <button
                    onClick={() => setClinicianReview(prev => ({ ...prev, approved: false }))}
                    className={`btn ${!clinicianReview.approved ? 'btn-error' : 'btn-outline'}`}
                  >
                    <FaTimes className="mr-2" />
                    Reject
                  </button>
                </div>
              </div>

              <div>
                <label className="form-label">Review Notes</label>
                <textarea
                  className="form-control"
                  rows="4"
                  value={clinicianReview.notes}
                  onChange={(e) => setClinicianReview(prev => ({ ...prev, notes: e.target.value }))}
                  placeholder="Add your clinical notes and observations here..."
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="form-label">Override Urgency Level</label>
                  <select
                    className="form-control"
                    value={clinicianReview.modifiedUrgency}
                    onChange={(e) => setClinicianReview(prev => ({ ...prev, modifiedUrgency: e.target.value }))}
                  >
                    <option value="">Keep AI Recommendation</option>
                    <option value="critical">Critical</option>
                    <option value="high">High</option>
                    <option value="moderate">Moderate</option>
                    <option value="low">Low</option>
                    <option value="minimal">Minimal</option>
                  </select>
                </div>
                <div className="flex items-end">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      className="form-checkbox"
                      checked={clinicianReview.overrideRecommendations}
                      onChange={(e) => setClinicianReview(prev => ({ ...prev, overrideRecommendations: e.target.checked }))}
                    />
                    <span className="ml-2">Override AI Recommendations</span>
                  </label>
                </div>
              </div>

              <div className="flex justify-end space-x-2 pt-4">
                <button
                  onClick={() => setIsEditing(false)}
                  className="btn btn-secondary"
                  disabled={reviewLoading}
                >
                  Cancel
                </button>
                <button
                  onClick={handleSaveReview}
                  className="btn btn-primary"
                  disabled={reviewLoading}
                >
                  {reviewLoading ? (
                    <FaSpinner className="animate-spin mr-2" />
                  ) : (
                    <FaSave className="mr-2" />
                  )}
                  Save Review
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-neutral-text">
                    Clinical Review Status
                  </h4>
                  <p className="body-small text-neutral-text-secondary">
                    Reviewed and approved by healthcare professional
                  </p>
                </div>
                <div className="flex items-center space-x-2">
                  {clinicianReview.approved ? (
                    <span className="badge badge-success flex items-center">
                      <FaLock className="mr-1" />
                      Approved
                    </span>
                  ) : (
                    <span className="badge badge-warning flex items-center">
                      <FaLockOpen className="mr-1" />
                      Pending Review
                    </span>
                  )}
                  <button
                    onClick={handleEditReview}
                    className="btn btn-secondary btn-sm"
                  >
                    <FaEdit className="mr-1" />
                    Edit Review
                  </button>
                </div>
              </div>

              {clinicianReview.notes && (
                <div className="p-4 bg-blue-50 rounded-lg">
                  <h5 className="font-medium text-neutral-text mb-2">Review Notes</h5>
                  <p className="body-small text-neutral-text-secondary">
                    {clinicianReview.notes}
                  </p>
                </div>
              )}

              {clinicianReview.modifiedUrgency && (
                <div className="p-4 bg-amber-50 rounded-lg">
                  <h5 className="font-medium text-neutral-text mb-2">Modified Urgency</h5>
                  <p className="body-small text-neutral-text-secondary">
                    Urgency level changed to: <span className="font-medium">{clinicianReview.modifiedUrgency}</span>
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Detailed Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Symptoms & Vitals Analysis */}
        <div className="card">
          <div className="card-header">
            <div className="flex items-center">
              <div className="bg-blue-100 p-2 rounded-lg mr-3">
                <FaHeartbeat className="h-5 w-5 text-primary" />
              </div>
              <h3 className="h3 text-neutral-text">
                Comprehensive Clinical Assessment
              </h3>
            </div>
          </div>
          <div className="card-body">
            {symptomsAnalysis.vital_signs &&
              Object.keys(symptomsAnalysis.vital_signs).length > 0 && (
                <div className="mb-6">
                  <h4 className="h4 text-neutral-text mb-3 flex items-center">
                    <FaHeartbeat className="mr-2" />
                    Vital Signs Analysis
                  </h4>
                  <div className="space-y-3">
                    {Object.entries(symptomsAnalysis.vital_signs).map(
                      ([name, vital]) => (
                        <div
                          key={name}
                          className="border border-neutral-border rounded-lg p-3"
                        >
                          <div className="flex justify-between items-center">
                            <span className="font-medium text-neutral-text capitalize">
                              {name.replace("_", " ")}
                            </span>
                            <span
                              className={`badge ${
                                vital.status === "normal"
                                  ? "badge-success"
                                  : "badge-error"
                              }`}
                            >
                              {vital.status}
                            </span>
                          </div>
                          <div className="mt-2">
                            <div className="flex justify-between text-sm">
                              <span className="text-neutral-text-secondary">
                                Value
                              </span>
                              <span className="font-medium">
                                {vital.value} {vital.unit}
                              </span>
                            </div>
                            <div className="flex justify-between text-sm mt-1">
                              <span className="text-neutral-text-secondary">
                                Normal Range
                              </span>
                              <span className="font-medium">
                                {vital.normal_range}
                              </span>
                            </div>
                            <div className="mt-2 text-sm">
                              <span className="text-neutral-text-secondary">
                                Interpretation:{" "}
                              </span>
                              <span className="font-medium">
                                {vital.interpretation}
                              </span>
                            </div>
                            <div className="mt-1 text-sm">
                              <span className="text-neutral-text-secondary">
                                Clinical Significance:{" "}
                              </span>
                              <span className="font-medium">
                                {vital.clinical_significance}
                              </span>
                            </div>
                          </div>
                        </div>
                      )
                    )}
                  </div>
                </div>
              )}

            {symptomsAnalysis.symptom_categories &&
              Object.keys(symptomsAnalysis.symptom_categories).length > 0 && (
                <div className="mb-6">
                  <h4 className="h4 text-neutral-text mb-3 flex items-center">
                    <FaUserMd className="mr-2" />
                    Symptom Analysis by System
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {Object.entries(symptomsAnalysis.symptom_categories).map(
                      ([category, symptoms]) => {
                        if (symptoms && symptoms.length > 0) {
                          return (
                            <div
                              key={category}
                              className="border border-neutral-border rounded-lg p-3"
                            >
                              <h5 className="font-medium text-neutral-text capitalize mb-2">
                                {category}
                              </h5>
                              <div className="flex flex-wrap gap-1">
                                {symptoms.map((symptom, index) => (
                                  <span
                                    key={index}
                                    className="badge badge-info text-xs"
                                  >
                                    {symptom}
                                  </span>
                                ))}
                              </div>
                            </div>
                          );
                        }
                        return null;
                      }
                    )}
                  </div>
                </div>
              )}

            {symptomsAnalysis.primary_concerns &&
              symptomsAnalysis.primary_concerns.length > 0 && (
                <div className="mb-6">
                  <h4 className="h4 text-neutral-text mb-3 flex items-center">
                    <FaExclamationTriangle className="mr-2 text-amber-500" />
                    Primary Clinical Concerns
                  </h4>
                  <div className="space-y-2">
                    {symptomsAnalysis.primary_concerns.map((concern, index) => (
                      <div
                        key={index}
                        className="border border-amber-200 bg-amber-50 rounded-lg p-3"
                      >
                        <div className="flex justify-between">
                          <span className="font-medium text-amber-800">
                            {concern.name || concern.type}
                          </span>
                          <span className="badge badge-warning">
                            {concern.severity || concern.type}
                          </span>
                        </div>
                        <div className="mt-1 text-sm text-amber-700">
                          {concern.interpretation || concern.significance}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
          </div>
        </div>

        {/* Clinical Guidelines and External Data */}
        <div className="card">
          <div className="card-header">
            <div className="flex items-center">
              <div className="bg-purple-100 p-2 rounded-lg mr-3">
                <FaBookMedical className="h-5 w-5 text-purple-600" />
              </div>
              <h3 className="h3 text-neutral-text">
                Evidence-Based Clinical Guidance
              </h3>
            </div>
          </div>
          <div className="card-body">
            {ragResults && ragResults.length > 0 ? (
              <div className="space-y-4">
                {ragResults.map((guideline, index) => (
                  <div
                    key={index}
                    className="border border-neutral-border rounded-lg p-4"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-neutral-text">
                        {guideline.title}
                      </h4>
                      <div className="flex flex-col items-end">
                        <span
                          className={`badge ${
                            guideline.external ? "badge-success" : "badge-info"
                          } mb-1`}
                        >
                          {guideline.external
                            ? "External Source"
                            : "Local Guidelines"}
                        </span>
                        <span className="badge badge-secondary text-xs">
                          Relevance:{" "}
                          {Math.round(guideline.relevance_score * 100)}%
                        </span>
                      </div>
                    </div>
                    <p className="body-small text-neutral-text-secondary mt-2">
                      {guideline.content}
                    </p>
                    {guideline.source && (
                      <div className="mt-2 flex items-center">
                        <span className="body-small text-neutral-text-secondary">
                          Source:{" "}
                        </span>
                        <span className="body-small font-medium text-neutral-text ml-1">
                          {guideline.source}
                        </span>
                      </div>
                    )}
                    {guideline.evidence_level && (
                      <div className="mt-1">
                        <span className="body-small text-neutral-text-secondary">
                          Evidence Level:{" "}
                        </span>
                        <span className="body-small font-medium text-neutral-text">
                          {guideline.evidence_level}
                        </span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <FaBookMedical className="h-12 w-12 text-neutral-text-secondary mx-auto mb-3" />
                <p className="body-large text-neutral-text-secondary">
                  No relevant clinical guidelines found for this case.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Risk Assessment Details */}
      <div className="card mb-8">
        <div className="card-header">
          <div className="flex items-center">
            <div className="bg-red-100 p-2 rounded-lg mr-3">
              <FaExclamationTriangle className="h-5 w-5 text-red-600" />
            </div>
            <h3 className="h3 text-neutral-text">
              Detailed Risk Stratification Analysis
            </h3>
          </div>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="border border-neutral-border rounded-lg p-4">
              <h4 className="font-medium text-neutral-text mb-3 flex items-center">
                <FaHeartbeat className="mr-2" />
                Vital Signs Risk Factors
              </h4>
              {renderRiskFactors(riskAssessment.vital_risks)}
            </div>

            <div className="border border-neutral-border rounded-lg p-4">
              <h4 className="font-medium text-neutral-text mb-3 flex items-center">
                <FaUserMd className="mr-2" />
                Symptom Risk Factors
              </h4>
              {renderRiskFactors(riskAssessment.symptom_risks)}
            </div>

            <div className="border border-neutral-border rounded-lg p-4">
              <h4 className="font-medium text-neutral-text mb-3 flex items-center">
                <FaClock className="mr-2" />
                Demographic Risk Factors
              </h4>
              {renderRiskFactors(riskAssessment.demographic_risks)}
            </div>
          </div>

          {riskAssessment.risk_explanation && (
            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="font-medium text-neutral-text mb-2">
                Risk Assessment Summary
              </h4>
              <p className="body-large text-neutral-text-secondary">
                {riskAssessment.risk_explanation}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Medical Imaging */}
      <div className="card mb-8">
        <div className="card-header">
          <div className="flex items-center">
            <div className="bg-green-100 p-2 rounded-lg mr-3">
              <FaFileMedical className="h-5 w-5 text-green-600" />
            </div>
            <h3 className="h3 text-neutral-text">Medical Imaging Analysis</h3>
          </div>
        </div>
        <div className="card-body">
          {imagingAnalysis.status === "success" ? (
            <div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="h4 text-neutral-text mb-3">
                    Image Characteristics
                  </h4>
                  <div className="space-y-2">
                    <div className="flex justify-between py-2 border-b border-neutral-border">
                      <span className="body-large text-neutral-text-secondary">
                        Type
                      </span>
                      <span className="font-medium text-neutral-text">
                        {imagingAnalysis.analysis?.imaging_type}
                      </span>
                    </div>
                    <div className="flex justify-between py-2 border-b border-neutral-border">
                      <span className="body-large text-neutral-text-secondary">
                        Dimensions
                      </span>
                      <span className="font-medium text-neutral-text">
                        {imagingAnalysis.analysis?.dimensions}
                      </span>
                    </div>
                    <div className="flex justify-between py-2 border-b border-neutral-border">
                      <span className="body-large text-neutral-text-secondary">
                        Format
                      </span>
                      <span className="font-medium text-neutral-text">
                        {imagingAnalysis.analysis?.file_format}
                      </span>
                    </div>
                    <div className="flex justify-between py-2 border-b border-neutral-border">
                      <span className="body-large text-neutral-text-secondary">
                        File Size
                      </span>
                      <span className="font-medium text-neutral-text">
                        {imagingAnalysis.analysis?.file_size}
                      </span>
                    </div>
                    <div className="flex justify-between py-2 border-b border-neutral-border">
                      <span className="body-large text-neutral-text-secondary">
                        Quality
                      </span>
                      <span className="font-medium text-neutral-text">
                        {imagingAnalysis.analysis?.technical_quality}
                      </span>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="h4 text-neutral-text mb-3">
                    Clinical Analysis
                  </h4>
                  <div className="space-y-3">
                    <div>
                      <h5 className="font-medium text-neutral-text mb-2">
                        Key Observations
                      </h5>
                      <ul className="list-disc pl-5 space-y-1">
                        {imagingAnalysis.analysis?.observations?.map(
                          (observation, index) => (
                            <li
                              key={index}
                              className="body-small text-neutral-text-secondary"
                            >
                              {observation}
                            </li>
                          )
                        )}
                      </ul>
                    </div>

                    <div>
                      <h5 className="font-medium text-neutral-text mb-2">
                        Clinical Recommendations
                      </h5>
                      <ul className="list-disc pl-5 space-y-1">
                        {imagingAnalysis.analysis?.recommendations?.map(
                          (recommendation, index) => (
                            <li
                              key={index}
                              className="body-small text-neutral-text-secondary"
                            >
                              {recommendation}
                            </li>
                          )
                        )}
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Enterprise Image Analysis */}
              {imagingAnalysis.analysis?.image_statistics && (
                <div className="mt-6 p-4 bg-purple-50 border border-purple-200 rounded-lg">
                  <h4 className="font-medium text-neutral-text mb-3">
                    Enterprise Image Analysis
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <h5 className="font-medium text-neutral-text text-sm">
                        Image Statistics
                      </h5>
                      <pre className="text-xs text-neutral-text-secondary bg-white p-2 rounded mt-1 overflow-x-auto">
                        {JSON.stringify(imagingAnalysis.analysis.image_statistics, null, 2)}
                      </pre>
                    </div>
                    <div>
                      <h5 className="font-medium text-neutral-text text-sm">
                        Quality Metrics
                      </h5>
                      <pre className="text-xs text-neutral-text-secondary bg-white p-2 rounded mt-1 overflow-x-auto">
                        {JSON.stringify(imagingAnalysis.analysis.quality_metrics, null, 2)}
                      </pre>
                    </div>
                    <div>
                      <h5 className="font-medium text-neutral-text text-sm">
                        Confidence
                      </h5>
                      <div className="mt-1">
                        <div className="flex justify-between text-sm">
                          <span className="text-neutral-text-secondary">
                            Analysis Confidence
                          </span>
                          <span className="font-medium">
                            {(imagingAnalysis.analysis.enterprise_confidence * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="prose max-w-none">
              <p className="body-large text-neutral-text">
                {imagingAnalysis.message || "No imaging analysis available"}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Advanced Agent Results */}
      <div className="mb-8">
        <div className="card-header mb-4">
          <h2 className="h2 text-neutral-text">
            Advanced Clinical Decision Support
          </h2>
          <p className="body-large text-neutral-text-secondary mt-2">
            Comprehensive treatment planning, follow-up care, and safety
            assessments
          </p>
        </div>
        <AdvancedAgentResults
          taskId={taskId}
          patientData={result?.result?.patient_data}
          symptomsAnalysis={symptomsAnalysis}
          riskAssessment={riskAssessment}
          treatmentRecommendations={
            finalRecommendation?.treatment_recommendations
          }
          followupPlan={finalRecommendation?.followup_plan}
          drugInteractions={finalRecommendation?.drug_interactions}
          specialistRecommendations={
            finalRecommendation?.specialist_recommendations
          }
          qualityAssessment={finalRecommendation?.quality_assessment}
        />
      </div>

      {/* Clinical Visualizations */}
      <div className="mb-8">
        <div className="card-header mb-4">
          <h2 className="h2 text-neutral-text">Clinical Visualizations</h2>
          <p className="body-large text-neutral-text-secondary mt-2">
            Interactive charts and visual representations of clinical data
          </p>
        </div>
        <ClinicalVisualizations
          taskId={taskId}
          patientData={result?.result?.patient_data}
          symptomsAnalysis={symptomsAnalysis}
          riskAssessment={riskAssessment}
          treatmentRecommendations={
            finalRecommendation?.treatment_recommendations
          }
          followupPlan={finalRecommendation?.followup_plan}
          drugInteractions={finalRecommendation?.drug_interactions}
          specialistRecommendations={
            finalRecommendation?.specialist_recommendations
          }
        />
      </div>

      {/* Differential Diagnosis */}
      <div className="mb-8">
        <div className="card-header mb-4">
          <h2 className="h2 text-neutral-text">Differential Diagnosis</h2>
          <p className="body-large text-neutral-text-secondary mt-2">
            AI-powered differential diagnosis with confidence scoring
          </p>
        </div>
        <DifferentialDiagnosis
          taskId={taskId}
          patientData={result?.result?.patient_data}
          symptomsAnalysis={symptomsAnalysis}
          riskAssessment={riskAssessment}
        />
      </div>

      {/* Predictive Analytics */}
      <div className="mb-8">
        <div className="card-header mb-4">
          <h2 className="h2 text-neutral-text">Predictive Analytics</h2>
          <p className="body-large text-neutral-text-secondary mt-2">
            Forecasting potential complications and risk stratification
          </p>
        </div>
        <PredictiveAnalytics
          taskId={taskId}
          patientData={result?.result?.patient_data}
          symptomsAnalysis={symptomsAnalysis}
          riskAssessment={riskAssessment}
          treatmentRecommendations={finalRecommendation?.treatment_recommendations}
        />
      </div>

      {/* Task Information */}
      <div className="card">
        <div className="card-header">
          <h2 className="h2 text-neutral-text">Clinical Report Metadata</h2>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <p className="body-small text-neutral-text-secondary">
                Report ID
              </p>
              <p className="font-mono body-large text-neutral-text">{taskId}</p>
            </div>
            <div>
              <p className="body-small text-neutral-text-secondary">
                Assessment Status
              </p>
              <span className="badge badge-success flex items-center">
                <FaCheck className="mr-1" />
                Completed
              </span>
            </div>
            <div>
              <p className="body-small text-neutral-text-secondary">
                Analysis Timestamp
              </p>
              <p className="body-large text-neutral-text">
                {new Date().toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="mt-8 flex flex-col sm:flex-row sm:justify-center gap-4 print:hidden">
        <button onClick={handleStartNewTriage} className="btn btn-primary">
          <FaUserMd className="mr-2" />
          Start New Triage Assessment
        </button>
        <button onClick={handlePrintReport} className="btn btn-secondary">
          <FaPrint className="mr-2" />
          Print Clinical Report
        </button>
      </div>
    </div>
  );
};

export default Results;