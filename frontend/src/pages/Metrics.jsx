import { useState, useEffect } from 'react';
import { getMetrics } from '../api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Metrics = () => {
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMetrics()
      .then(response => {
        const parsedMetrics = parsePrometheusMetrics(response.data);
        setMetrics(parsedMetrics);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  const parsePrometheusMetrics = (text) => {
    const lines = text.split('\\n');
    const data = [];
    lines.forEach(line => {
      if (line.startsWith('http_requests_total')) {
        const match = line.match(/endpoint="([^"]+)",method="([^"]+)",http_status="([^"]+)"} (\\d+)/);
        if (match) {
          data.push({
            endpoint: match[1],
            method: match[2],
            status: match[3],
            count: parseInt(match[4], 10)
          });
        }
      }
    });
    return data;
  };

  if (loading) return <p>Loading metrics...</p>;

  return (
    <div className="bg-white p-8 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">API Metrics</h2>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={metrics}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="endpoint" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Metrics;
