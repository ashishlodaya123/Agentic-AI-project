import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import TriageDashboard from './pages/TriageDashboard';
import Results from './pages/Results';
import Metrics from './pages/Metrics';
import Home from './pages/Home';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow-md">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <h1 className="text-xl font-bold text-gray-800">Clinical Decision Assistant</h1>
                </div>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  <Link to="/" className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium">Home</Link>
                  <Link to="/triage" className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium">Triage</Link>
                  <Link to="/metrics" className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium">Metrics</Link>
                </div>
              </div>
            </div>
          </div>
        </nav>
        <main>
          <div className="max-w-7xl mx-auto sm:px-6 lg:px-8 py-8">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/triage" element={<TriageDashboard />} />
              <Route path="/results/:taskId" element={<Results />} />
              <Route path="/metrics" element={<Metrics />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;
