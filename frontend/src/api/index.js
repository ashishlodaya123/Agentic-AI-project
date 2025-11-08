import axios from "axios";

// Check if environment variables are defined
const baseURL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
const apiKey = import.meta.env.VITE_API_KEY || "triage_secret_key";

const apiClient = axios.create({
  baseURL: baseURL,
  headers: {
    "Content-Type": "application/json",
    "X-API-KEY": apiKey,
  },
});

// Add request interceptor for debugging
apiClient.interceptors.request.use(
  (config) => {
    console.log("API Request:", config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error("API Request Error:", error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
apiClient.interceptors.response.use(
  (response) => {
    console.log("API Response:", response.status, response.config.url, response.data);
    return response;
  },
  (error) => {
    console.error(
      "API Response Error:",
      error.response?.status,
      error.response?.data,
      error.config?.url
    );

    // Handle network errors
    if (!error.response) {
      alert("Network error: Please check your connection and try again.");
    }
    // Handle server errors
    else if (error.response.status >= 500) {
      alert("Server error: Please try again later.");
    }
    // Handle client errors
    else if (error.response.status >= 400) {
      const message = error.response.data?.detail || "An error occurred";
      alert(`Error: ${message}`);
    }

    return Promise.reject(error);
  }
);

export const startTriage = (patientData) => {
  return apiClient.post("/api/triage", patientData);
};

export const uploadImage = (formData) => {
  return apiClient.post("/api/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

export const getTaskResult = (taskId) => {
  return apiClient.get(`/api/results/${taskId}`);
};

export const getMetrics = () => {
  // Use the direct /metrics endpoint instead of /api/metrics
  console.log("Fetching metrics from:", `${baseURL}/metrics`);
  return apiClient.get("/metrics").catch((error) => {
    console.error("Error fetching metrics:", error);
    // If the apiClient fails, try a direct axios call as fallback
    return axios.get(`${baseURL}/metrics`);
  });
};

export const checkBackendStatus = () => {
  return apiClient.get("/");
};

// Advanced Agent Endpoints
export const getTreatmentRecommendations = (requestData) => {
  return apiClient.post("/api/agents/treatment", requestData);
};

export const getFollowupPlan = (requestData) => {
  return apiClient.post("/api/agents/followup", requestData);
};

export const checkDrugInteractions = (requestData) => {
  return apiClient.post("/api/agents/drug-interactions", requestData);
};

export const getSpecialistRecommendations = (requestData) => {
  return apiClient.post("/api/agents/specialist", requestData);
};

export const runQualityAssurance = (requestData) => {
  return apiClient.post("/api/agents/quality", requestData);
};

export const getPredictiveAnalytics = (requestData) => {
  return apiClient.post("/api/agents/predictive-analytics", requestData);
};

export const getClinicalVisualization = (requestData) => {
  return apiClient.post("/api/agents/clinical-visualization", requestData);
};

export const getDifferentialDiagnosis = (requestData) => {
  console.log("Calling differential diagnosis API with data:", requestData);
  return apiClient.post("/api/agents/differential-diagnosis", requestData)
    .then(response => {
      console.log("Differential diagnosis API response:", response.data);
      return response;
    })
    .catch(error => {
      console.error("Differential diagnosis API error:", error);
      throw error;
    });
};

// IoT Data Endpoint
export const getIoTVitalsData = (requestData) => {
  console.log("Sending IoT vitals data request:", requestData);
  return apiClient
    .post("/api/iot-vitals", requestData)
    .then((response) => {
      console.log("Received IoT vitals data response:", response.data);
      return response;
    })
    .catch((error) => {
      console.error("Error in IoT vitals data request:", error);
      throw error;
    });
};

// Clinician Review Endpoints
export const saveClinicianReview = (reviewData) => {
  console.log("Saving clinician review:", reviewData);
  return apiClient
    .post("/api/clinician-review", reviewData)
    .then((response) => {
      console.log("Clinician review saved:", response.data);
      return response;
    })
    .catch((error) => {
      console.error("Error saving clinician review:", error);

      // Provide more user-friendly error messages
      if (error.response) {
        // Server responded with error status
        const status = error.response.status;
        const message =
          error.response.data?.detail ||
          error.response.data?.message ||
          "Unknown server error";

        if (status === 400) {
          throw new Error(`Invalid request: ${message}`);
        } else if (status === 404) {
          throw new Error(`Resource not found: ${message}`);
        } else if (status >= 500) {
          throw new Error("Server error. Please try again later.");
        } else {
          throw new Error(`Error saving review: ${message}`);
        }
      } else if (error.request) {
        // Request was made but no response received
        throw new Error(
          "Network error. Please check your connection and try again."
        );
      } else {
        // Something else happened
        throw new Error(`Error: ${error.message || "Unknown error occurred"}`);
      }
    });
};

export const getClinicianReview = (taskId) => {
  console.log("Fetching clinician review for task:", taskId);

  // Validate taskId
  if (!taskId) {
    return Promise.reject(new Error("Task ID is required"));
  }

  return apiClient
    .get(`/api/clinician-review/${taskId}`)
    .then((response) => {
      console.log("Received clinician review:", response.data);
      return response;
    })
    .catch((error) => {
      console.error("Error fetching clinician review:", error);

      // Handle case where review is not found (this is not necessarily an error)
      if (error.response && error.response.status === 404) {
        // Return a consistent structure for not found cases
        return {
          data: {
            status: "not_found",
            message: "No review found for this task",
          },
        };
      }

      // Handle other errors
      if (error.response) {
        const message = error.response.data?.detail || "Unknown server error";
        throw new Error(`Error fetching review: ${message}`);
      } else if (error.request) {
        throw new Error("Network error. Please check your connection.");
      } else {
        throw new Error(`Error: ${error.message || "Unknown error occurred"}`);
      }
    });
};
