import { useState, useEffect } from 'react';
import { FaChartBar, FaChartPie, FaUsers, FaServer, FaChartLine } from 'react-icons/fa';
import { getMetrics } from '../api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Metrics = () => {
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getMetrics()
      .then(response => {
        // Check if response data exists
        if (response && response.data) {
          const parsedMetrics = parsePrometheusMetrics(response.data);
          setMetrics(parsedMetrics);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error('Metrics error:', err);
        setError('Failed to load metrics: ' + (err.message || 'Unknown error'));
        setLoading(false);
      });
  }, []);

  const parsePrometheusMetrics = (text) => {
    // Check if text exists
    if (!text) return [];
    
    const lines = text.split('\n');
    const data = [];
    
    lines.forEach(line => {
      // Skip comments and empty lines
      if (line.startsWith('#') || line.trim() === '') return;
      
      // Parse http_requests_total metrics
      if (line.startsWith('http_requests_total')) {
        // Handle the Prometheus format: http_requests_total{method="GET",endpoint="/",http_status="200"} 1
        const match = line.match(/http_requests_total\{method="([^"]*)",endpoint="([^"]*)",http_status="([^"]*)"\}\s+(\d+)/);
        if (match) {
          data.push({
            endpoint: match[2],
            method: match[1],
            status: match[3],
            count: parseInt(match[4], 10)
          });
        }
      }
    });
    
    return data;
  };

  // Prepare data for pie chart
  const getStatusData = () => {
    const statusCounts = {};
    metrics.forEach(metric => {
      const status = metric.status;
      statusCounts[status] = (statusCounts[status] || 0) + metric.count;
    });
    
    return Object.keys(statusCounts).map(status => ({
      name: `Status ${status}`,
      value: statusCounts[status]
    }));
  };

  // Prepare data for endpoint chart
  const getEndpointData = () => {
    const endpointCounts = {};
    metrics.forEach(metric => {
      const endpoint = metric.endpoint;
      endpointCounts[endpoint] = (endpointCounts[endpoint] || 0) + metric.count;
    });
    
    return Object.keys(endpointCounts).map(endpoint => ({
      name: endpoint,
      count: endpointCounts[endpoint]
    }));
  };

  const COLORS = ['#2563EB', '#16A34A', '#EA580C', '#DC2626', '#8B5CF6'];

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="card">
          <div className="card-body py-12">
            <div className="flex justify-center items-center">
              <FaChartLine className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
              <span className="ml-3 body-large text-neutral-text">Loading metrics...</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="card">
          <div className="card-body text-center py-12">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
              <FaChartLine className="h-6 w-6 text-red-600" />
            </div>
            <h3 className="h3 text-neutral-text mt-4">Error</h3>
            <div className="mt-2">
              <p className="body-large text-neutral-text-secondary">{error}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const statusData = getStatusData();
  const endpointData = getEndpointData();

  // Calculate summary metrics
  const totalRequests = metrics.reduce((sum, m) => sum + m.count, 0);
  const uniqueEndpoints = [...new Set(metrics.map(m => m.endpoint))].length;
  const uniqueStatusCodes = [...new Set(metrics.map(m => m.status))].length;

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="h1 text-neutral-text">System Metrics</h1>
        <p className="body-large text-neutral-text-secondary mt-2">
          Real-time performance monitoring and analytics
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card">
          <div className="card-body">
            <div className="flex items-center">
              <div className="bg-primary bg-opacity-10 p-3 rounded-lg mr-4">
                <FaChartBar className="h-6 w-6 text-primary" />
              </div>
              <div>
                <p className="body-small text-neutral-text-secondary">Total Requests</p>
                <p className="text-2xl font-bold text-neutral-text">{totalRequests || 0}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-body">
            <div className="flex items-center">
              <div className="bg-green-500 bg-opacity-10 p-3 rounded-lg mr-4">
                <FaUsers className="h-6 w-6 text-green-500" />
              </div>
              <div>
                <p className="body-small text-neutral-text-secondary">Endpoints</p>
                <p className="text-2xl font-bold text-neutral-text">{uniqueEndpoints || 0}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-body">
            <div className="flex items-center">
              <div className="bg-purple-500 bg-opacity-10 p-3 rounded-lg mr-4">
                <FaServer className="h-6 w-6 text-purple-500" />
              </div>
              <div>
                <p className="body-small text-neutral-text-secondary">Status Codes</p>
                <p className="text-2xl font-bold text-neutral-text">{uniqueStatusCodes || 0}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Endpoint Requests */}
        <div className="card">
          <div className="card-header">
            <h3 className="h3 text-neutral-text">Requests by Endpoint</h3>
          </div>
          <div className="card-body">
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={endpointData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                  <XAxis dataKey="name" stroke="#64748B" />
                  <YAxis stroke="#64748B" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#FFFFFF', 
                      borderColor: '#E2E8F0', 
                      borderRadius: '0.5rem',
                      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
                    }}
                  />
                  <Legend />
                  <Bar dataKey="count" name="Requests" fill="#2563EB" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Status Codes */}
        <div className="card">
          <div className="card-header">
            <h3 className="h3 text-neutral-text">Requests by Status Code</h3>
          </div>
          <div className="card-body">
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={statusData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {statusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#FFFFFF', 
                      borderColor: '#E2E8F0', 
                      borderRadius: '0.5rem',
                      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
                    }}
                  />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>

      {/* Raw Data Table */}
      <div className="card">
        <div className="card-header">
          <h3 className="h3 text-neutral-text">Detailed Metrics</h3>
        </div>
        <div className="card-body">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-neutral-border">
              <thead>
                <tr>
                  <th className="px-6 py-3 text-left body-small font-medium text-neutral-text-secondary uppercase tracking-wider">Endpoint</th>
                  <th className="px-6 py-3 text-left body-small font-medium text-neutral-text-secondary uppercase tracking-wider">Method</th>
                  <th className="px-6 py-3 text-left body-small font-medium text-neutral-text-secondary uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left body-small font-medium text-neutral-text-secondary uppercase tracking-wider">Count</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-neutral-border">
                {metrics.length > 0 ? (
                  metrics.map((metric, index) => (
                    <tr key={index} className="hover:bg-neutral-background">
                      <td className="px-6 py-4 body-large text-neutral-text">{metric.endpoint}</td>
                      <td className="px-6 py-4 body-large text-neutral-text">
                        <span className={`badge ${
                          metric.method === 'GET' ? 'badge-info' : 
                          metric.method === 'POST' ? 'badge-success' : 
                          metric.method === 'PUT' ? 'badge-warning' : 
                          'badge-error'
                        }`}>
                          {metric.method}
                        </span>
                      </td>
                      <td className="px-6 py-4 body-large text-neutral-text">
                        <span className={`badge ${
                          metric.status.startsWith('2') ? 'badge-success' : 
                          metric.status.startsWith('4') ? 'badge-warning' : 
                          metric.status.startsWith('5') ? 'badge-error' : 
                          'badge-info'
                        }`}>
                          {metric.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 body-large text-neutral-text font-medium">{metric.count}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4" className="px-6 py-4 text-center body-large text-neutral-text-secondary">
                      No metrics data available. Try interacting with the application to generate metrics.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Metrics;