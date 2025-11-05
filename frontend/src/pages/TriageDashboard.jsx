import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
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
        imagePath = response.data.file_path;
      }

      const patientData = { ...formData, image_path: imagePath };
      const response = await startTriage(patientData);

      navigate(`/results/${response.data.task_id}`);

    } catch (err) {
      setError('Failed to start triage process. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Patient Intake</h2>
      <form onSubmit={handleSubmit}>
        {/* Symptoms */}
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="symptoms">Symptoms</label>
          <textarea name="symptoms" value={formData.symptoms} onChange={handleChange} className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" required />
        </div>

        {/* Vitals */}
        <div className="grid grid-cols-3 gap-4 mb-4">
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="heart_rate">Heart Rate</label>
            <input type="number" name="heart_rate" value={formData.vitals.heart_rate} onChange={handleChange} className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" required />
          </div>
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="blood_pressure">Blood Pressure</label>
            <input type="text" name="blood_pressure" value={formData.vitals.blood_pressure} onChange={handleChange} className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" required />
          </div>
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="temperature">Temperature</label>
            <input type="number" step="0.1" name="temperature" value={formData.vitals.temperature} onChange={handleChange} className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" required />
          </div>
        </div>

        {/* Age and Gender */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="age">Age</label>
            <input type="number" name="age" value={formData.age} onChange={handleChange} className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" required />
          </div>
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="gender">Gender</label>
            <input type="text" name="gender" value={formData.gender} onChange={handleChange} className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" required />
          </div>
        </div>

        {/* Image Upload */}
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="image">Medical Imaging (Optional)</label>
          <input type="file" onChange={handleFileChange} className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" />
        </div>

        {/* Submit */}
        <div className="flex items-center justify-between">
          <button type="submit" disabled={loading} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
            {loading ? 'Processing...' : 'Start Triage'}
          </button>
        </div>
        {error && <p className="text-red-500 text-xs italic mt-4">{error}</p>}
      </form>
    </div>
  );
};

export default TriageDashboard;
