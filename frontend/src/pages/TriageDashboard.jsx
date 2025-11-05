import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaUpload, FaSpinner } from 'react-icons/fa';
import { startTriage, uploadImage } from '../api';

const TriageDashboard = () => {
  const [formData, setFormData] = useState({
    symptoms: '',
    vitals: { heart_rate: '', blood_pressure: '', temperature: '' },
    age: '',
    gender: '',
    image_path: null
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name in formData.vitals) {
      setFormData(prev => ({ ...prev, vitals: { ...prev.vitals, [name]: value } }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      let imagePath = null;
      if (file) {
        const uploadData = new FormData();
        uploadData.append('file', file);
        const response = await uploadImage(uploadData);
        // Check if response exists and has data
        if (response && response.data && response.data.file_path) {
          imagePath = response.data.file_path;
        }
      }

      const patientData = { ...formData, image_path: imagePath };
      const response = await startTriage(patientData);
      
      // Check if response exists and has data
      if (response && response.data && response.data.task_id) {
        navigate(`/results/${response.data.task_id}`);
      } else {
        setError('Failed to start triage process. Invalid response from server.');
      }

    } catch (err) {
      console.error('Error starting triage:', err);
      setError('Failed to start triage process. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="h1 text-neutral-text">Patient Intake Form</h1>
        <p className="body-large text-neutral-text-secondary mt-2">
          Enter patient information for real-time triage assessment
        </p>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="h2 text-neutral-text">Patient Information</h2>
        </div>
        
        <div className="card-body">
          <form onSubmit={handleSubmit}>
            {/* Symptoms */}
            <div className="form-group">
              <label htmlFor="symptoms" className="form-label">
                Patient Symptoms
              </label>
              <textarea 
                id="symptoms"
                name="symptoms" 
                value={formData.symptoms} 
                onChange={handleChange} 
                className="form-control"
                placeholder="Describe the patient's symptoms in detail..."
                rows="4"
                required 
              />
              <p className="body-small text-neutral-text-secondary mt-2">
                Please provide a detailed description of the patient's symptoms
              </p>
            </div>

            {/* Vitals */}
            <div className="form-group">
              <h3 className="h3 text-neutral-text mb-4">Vital Signs</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label htmlFor="heart_rate" className="form-label">
                    Heart Rate (bpm)
                  </label>
                  <input 
                    type="number" 
                    id="heart_rate"
                    name="heart_rate" 
                    value={formData.vitals.heart_rate} 
                    onChange={handleChange} 
                    className="form-control"
                    placeholder="e.g., 72"
                    required 
                  />
                </div>
                <div>
                  <label htmlFor="blood_pressure" className="form-label">
                    Blood Pressure
                  </label>
                  <input 
                    type="text" 
                    id="blood_pressure"
                    name="blood_pressure" 
                    value={formData.vitals.blood_pressure} 
                    onChange={handleChange} 
                    className="form-control"
                    placeholder="e.g., 120/80"
                    required 
                  />
                </div>
                <div>
                  <label htmlFor="temperature" className="form-label">
                    Temperature (°C)
                  </label>
                  <input 
                    type="number" 
                    id="temperature"
                    step="0.1" 
                    name="temperature" 
                    value={formData.vitals.temperature} 
                    onChange={handleChange} 
                    className="form-control"
                    placeholder="e.g., 37.0"
                    required 
                  />
                </div>
              </div>
            </div>

            {/* Demographics */}
            <div className="form-group">
              <h3 className="h3 text-neutral-text mb-4">Patient Demographics</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="age" className="form-label">
                    Age
                  </label>
                  <input 
                    type="number" 
                    id="age"
                    name="age" 
                    value={formData.age} 
                    onChange={handleChange} 
                    className="form-control"
                    placeholder="e.g., 45"
                    required 
                  />
                </div>
                <div>
                  <label htmlFor="gender" className="form-label">
                    Gender
                  </label>
                  <select 
                    id="gender"
                    name="gender" 
                    value={formData.gender} 
                    onChange={handleChange} 
                    className="form-control form-select"
                    required
                  >
                    <option value="">Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                    <option value="Prefer not to say">Prefer not to say</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Image Upload */}
            <div className="form-group">
              <label className="form-label">
                Medical Imaging (Optional)
              </label>
              <div className="flex items-center justify-center w-full">
                <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-neutral-border rounded-lg cursor-pointer bg-neutral-surface hover:bg-blue-50 transition-colors duration-200">
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    <FaUpload className="w-8 h-8 text-neutral-text-secondary" />
                    <p className="body-small text-neutral-text-secondary mt-2">
                      <span className="font-semibold">Click to upload</span> or drag and drop
                    </p>
                    <p className="body-small text-neutral-text-secondary">
                      PNG, JPG, GIF up to 10MB
                    </p>
                  </div>
                  <input 
                    type="file" 
                    onChange={handleFileChange} 
                    className="hidden" 
                  />
                </label>
              </div>
              {file && (
                <p className="body-small text-neutral-text-secondary mt-2">
                  Selected file: <span className="font-medium">{file.name}</span>
                </p>
              )}
            </div>

            {/* Submit */}
            <div className="flex items-center justify-between pt-6">
              <button 
                type="submit" 
                disabled={loading} 
                className={`btn btn-primary ${loading ? 'opacity-75 cursor-not-allowed' : ''}`}
              >
                {loading ? (
                  <div className="flex items-center">
                    <FaSpinner className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" />
                    Processing...
                  </div>
                ) : (
                  <div className="flex items-center">
                    Start Triage Assessment
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
                    </svg>
                  </div>
                )}
              </button>
            </div>
            
            {error && (
              <div className="alert alert-error mt-6">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-error" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-error">Error</h3>
                    <div className="mt-2 text-sm text-error">
                      <p>{error}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
};

export default TriageDashboard;