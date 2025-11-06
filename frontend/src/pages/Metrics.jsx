import { useState, useEffect } from "react";
import {
  FaChartBar,
  FaChartPie,
  FaUsers,
  FaServer,
  FaChartLine,
} from "react-icons/fa";
import { getMetrics } from "../api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

const Metrics = () => {
  const [metrics, setMetrics] = useState([]);
  const [allMetrics, setAllMetrics] = useState({
    httpRequests: [],
    latency: [],
    other: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log('Fetching metrics...');
    getMetrics()
      .then((response) => {
        console.log('Metrics response received:', response);
        // Check if response data exists
        if (response && response.data) {
          console.log('Raw metrics data length:', response.data.length);
          console.log('Raw metrics data type:', typeof response.data);
          // Log first 2000 characters to see what we're working with
          console.log('First 2000 chars of raw data:', response.data.substring(0, 2000));
          const parsedMetrics = parsePrometheusMetrics(response.data);
          console.log('Setting metrics state with', parsedMetrics.length, 'entries');
          console.log('All metrics data:', allMetrics);
          setMetrics(parsedMetrics);
        } else {
          console.log('No response data received');
          setMetrics([]);
          setAllMetrics({
            httpRequests: [],
            latency: [],
            other: []
          });
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("Metrics error:", err);
        setError("Failed to load metrics: " + (err.message || "Unknown error"));
        setMetrics([]); // Ensure metrics is set to empty array on error
        setAllMetrics({
          httpRequests: [],
          latency: [],
          other: []
        });
        setLoading(false);
      });
  }, []);

  const parsePrometheusMetrics = (text) => {
    // Check if text exists
    if (!text) {
      console.log('No text to parse');
      return [];
    }

    const lines = text.split("\n");
    const httpRequestData = [];
    const latencyData = [];
    const otherMetrics = [];
    
    console.log(`Parsing ${lines.length} lines of metrics data`);

    // Parse all types of metrics
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      
      // Skip comments and empty lines
      if (line.startsWith("#") || line.trim() === "") continue;
      
      // Handle http_requests_total metrics
      if (line.includes("http_requests_total") && line.includes("method=") && line.includes("endpoint=") && line.includes("http_status=")) {
        try {
          // Extract everything between the braces
          const start = line.indexOf('{');
          const end = line.indexOf('}');
          if (start !== -1 && end !== -1 && end > start) {
            const labels = line.substring(start + 1, end);
            const valuePart = line.substring(end + 1).trim();
            const value = parseFloat(valuePart);
            
            // Parse the labels
            const methodMatch = labels.match(/method="([^"]+)"/);
            const endpointMatch = labels.match(/endpoint="([^"]+)"/);
            const statusMatch = labels.match(/http_status="([^"]+)"/);
            
            if (methodMatch && endpointMatch && statusMatch) {
              const method = methodMatch[1];
              const endpoint = endpointMatch[1];
              const status = statusMatch[1];
              
              console.log(`Found HTTP request metric: method=${method}, endpoint=${endpoint}, status=${status}, value=${value}`);
              
              if (!isNaN(value)) {
                httpRequestData.push({
                  endpoint: endpoint,
                  method: method,
                  status: status,
                  count: Math.floor(value),
                });
              }
            }
          }
        } catch (e) {
          console.error("Error parsing HTTP request line:", line, e);
        }
      }
      // Handle http_request_latency_seconds metrics (histogram)
      else if (line.includes("http_request_latency_seconds") && line.includes("method=") && line.includes("endpoint=")) {
        try {
          // Extract everything between the braces
          const start = line.indexOf('{');
          const end = line.indexOf('}');
          if (start !== -1 && end !== -1 && end > start) {
            const labels = line.substring(start + 1, end);
            const valuePart = line.substring(end + 1).trim();
            const value = parseFloat(valuePart);
            
            // Parse the labels
            const methodMatch = labels.match(/method="([^"]+)"/);
            const endpointMatch = labels.match(/endpoint="([^"]+)"/);
            
            if (methodMatch && endpointMatch) {
              const method = methodMatch[1];
              const endpoint = endpointMatch[1];
              
              // Check if this is a count, sum, or bucket metric
              let metricType = 'bucket';
              if (line.includes("_count{")) {
                metricType = 'count';
              } else if (line.includes("_sum{")) {
                metricType = 'sum';
              }
              
              console.log(`Found latency metric: method=${method}, endpoint=${endpoint}, type=${metricType}, value=${value}`);
              
              if (!isNaN(value)) {
                latencyData.push({
                  endpoint: endpoint,
                  method: method,
                  type: metricType,
                  value: value,
                });
              }
            }
          }
        } catch (e) {
          console.error("Error parsing latency line:", line, e);
        }
      }
      // Handle other metrics
      else if (line.includes("{") && line.includes("}") && !line.includes("http_requests_total") && !line.includes("http_request_latency_seconds")) {
        try {
          // Extract metric name and value
          const braceIndex = line.indexOf('{');
          if (braceIndex !== -1) {
            const metricName = line.substring(0, braceIndex);
            const endBraceIndex = line.indexOf('}');
            const labels = line.substring(braceIndex + 1, endBraceIndex);
            const valuePart = line.substring(endBraceIndex + 1).trim();
            const value = parseFloat(valuePart);
            
            if (!isNaN(value)) {
              otherMetrics.push({
                name: metricName,
                labels: labels,
                value: value,
              });
            }
          } else {
            // Handle metrics without labels
            const spaceIndex = line.lastIndexOf(' ');
            if (spaceIndex !== -1) {
              const metricName = line.substring(0, spaceIndex);
              const valuePart = line.substring(spaceIndex + 1).trim();
              const value = parseFloat(valuePart);
              
              if (!isNaN(value)) {
                otherMetrics.push({
                  name: metricName,
                  value: value,
                });
              }
            }
          }
        } catch (e) {
          console.error("Error parsing other metric line:", line, e);
        }
      }
    }

    console.log(`Parsed ${httpRequestData.length} HTTP request metrics`);
    console.log(`Parsed ${latencyData.length} latency metrics`);
    console.log(`Parsed ${otherMetrics.length} other metrics`);
    
    // Store all metrics in state
    setAllMetrics({
      httpRequests: httpRequestData,
      latency: latencyData,
      other: otherMetrics
    });
    
    return httpRequestData;
  };

  // Prepare data for pie chart
  const getStatusData = () => {
    if (metrics.length === 0) return [];
    
    const statusCounts = {};
    metrics.forEach((metric) => {
      const status = metric.status;
      if (status) {
        statusCounts[status] = (statusCounts[status] || 0) + metric.count;
      }
    });
    
    console.log('Status counts:', statusCounts);

    return Object.keys(statusCounts).map((status) => ({
      name: `Status ${status}`,
      value: statusCounts[status],
    }));
  };
  
  // Prepare data for endpoint chart
  const getEndpointData = () => {
    if (metrics.length === 0) return [];
    
    const endpointCounts = {};
    metrics.forEach((metric) => {
      const endpoint = metric.endpoint;
      if (endpoint) {
        endpointCounts[endpoint] = (endpointCounts[endpoint] || 0) + metric.count;
      }
    });
    
    console.log('Endpoint counts:', endpointCounts);

    return Object.keys(endpointCounts).map((endpoint) => ({
      name: endpoint,
      count: endpointCounts[endpoint],
    }));
  };
  
  // Prepare latency data for charts
  const getLatencyData = () => {
    if (!allMetrics.latency || allMetrics.latency.length === 0) return [];
    
    // Group latency data by endpoint and method
    const latencyMap = {};
    
    allMetrics.latency.forEach(metric => {
      const key = `${metric.endpoint}-${metric.method}`;
      if (!latencyMap[key]) {
        latencyMap[key] = {
          endpoint: metric.endpoint,
          method: metric.method,
          count: 0,
          sum: 0
        };
      }
      
      if (metric.type === 'count') {
        latencyMap[key].count = metric.value;
      } else if (metric.type === 'sum') {
        latencyMap[key].sum = metric.value;
      }
    });
    
    // Calculate average latency
    const result = Object.values(latencyMap).map(item => {
      const avgLatency = item.count > 0 ? (item.sum / item.count) : 0;
      return {
        name: `${item.endpoint} (${item.method})`,
        latency: avgLatency,
        count: item.count
      };
    });
    
    console.log('Latency data:', result);
    return result;
  };
  
  // Get other interesting metrics
  const getOtherMetrics = () => {
    if (!allMetrics.other || allMetrics.other.length === 0) return [];
    
    // Filter for interesting metrics (counters, gauges, etc.)
    const interestingMetrics = allMetrics.other.filter(metric => 
      metric.name.includes('total') || 
      metric.name.includes('count') || 
      metric.name.includes('active') ||
      metric.name.includes('gc') ||
      metric.name.includes('triage')
    );
    
    console.log('Other interesting metrics:', interestingMetrics);
    return interestingMetrics;
  };
  
  const COLORS = ["#2563EB", "#16A34A", "#EA580C", "#DC2626", "#8B5CF6"];

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="card">
          <div className="card-body py-12">
            <div className="flex justify-center items-center">
              <FaChartLine className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
              <span className="ml-3 body-large text-neutral-text">
                Loading metrics...
              </span>
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
  const latencyData = getLatencyData();
  const otherMetrics = getOtherMetrics();
  
  // Debug chart data
  console.log('Status data for chart:', statusData);
  console.log('Endpoint data for chart:', endpointData);
  console.log('Latency data for chart:', latencyData);
  console.log('Other metrics:', otherMetrics);

  // Calculate summary metrics
  const totalRequests = metrics.reduce((sum, m) => sum + (m.count || 0), 0);
  const uniqueEndpoints = metrics.length > 0 ? [...new Set(metrics.map((m) => m.endpoint))].length : 0;
  const uniqueStatusCodes = metrics.length > 0 ? [...new Set(metrics.map((m) => m.status))].length : 0;
  
  // Calculate latency summary
  const avgLatency = latencyData.length > 0 ? 
    latencyData.reduce((sum, m) => sum + m.latency, 0) / latencyData.length : 0;
  
  console.log('Summary metrics:', {totalRequests, uniqueEndpoints, uniqueStatusCodes, avgLatency});

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="h1 text-neutral-text">System Metrics</h1>
        <p className="body-large text-neutral-text-secondary mt-2">
          Real-time performance monitoring and analytics
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="card-body">
            <div className="flex items-center">
              <div className="bg-primary bg-opacity-10 p-3 rounded-lg mr-4">
                <FaChartBar className="h-6 w-6 text-primary" />
              </div>
              <div>
                <p className="body-small text-neutral-text-secondary">
                  Total Requests
                </p>
                <p className="text-2xl font-bold text-neutral-text">
                  {totalRequests || 0}
                </p>
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
                <p className="body-small text-neutral-text-secondary">
                  Endpoints
                </p>
                <p className="text-2xl font-bold text-neutral-text">
                  {uniqueEndpoints || 0}
                </p>
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
                <p className="body-small text-neutral-text-secondary">
                  Status Codes
                </p>
                <p className="text-2xl font-bold text-neutral-text">
                  {uniqueStatusCodes || 0}
                </p>
              </div>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="card-body">
            <div className="flex items-center">
              <div className="bg-yellow-500 bg-opacity-10 p-3 rounded-lg mr-4">
                <FaChartLine className="h-6 w-6 text-yellow-500" />
              </div>
              <div>
                <p className="body-small text-neutral-text-secondary">
                  Avg Latency
                </p>
                <p className="text-2xl font-bold text-neutral-text">
                  {avgLatency ? `${(avgLatency * 1000).toFixed(2)}ms` : '0ms'}
                </p>
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
              {endpointData.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={endpointData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                    <XAxis dataKey="name" stroke="#64748B" />
                    <YAxis stroke="#64748B" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#FFFFFF",
                        borderColor: "#E2E8F0",
                        borderRadius: "0.5rem",
                        boxShadow:
                          "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
                      }}
                    />
                    <Legend />
                    <Bar
                      dataKey="count"
                      name="Requests"
                      fill="#2563EB"
                      radius={[4, 4, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-full text-neutral-text-secondary">
                  No endpoint data available
                </div>
              )}
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
              {statusData.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={statusData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) =>
                        `${name}: ${(percent * 100).toFixed(0)}%`
                      }
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {statusData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={COLORS[index % COLORS.length]}
                        />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#FFFFFF",
                        borderColor: "#E2E8F0",
                        borderRadius: "0.5rem",
                        boxShadow:
                          "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
                      }}
                    />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-full text-neutral-text-secondary">
                  No status code data available
                </div>
              )}
            </div>
          </div>
        </div>
        
        {/* Latency by Endpoint */}
        <div className="card">
          <div className="card-header">
            <h3 className="h3 text-neutral-text">Average Latency by Endpoint</h3>
          </div>
          <div className="card-body">
            <div className="h-80">
              {latencyData.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={latencyData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                    <XAxis dataKey="name" stroke="#64748B" />
                    <YAxis 
                      stroke="#64748B" 
                      tickFormatter={(value) => `${(value * 1000).toFixed(2)}ms`}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#FFFFFF",
                        borderColor: "#E2E8F0",
                        borderRadius: "0.5rem",
                        boxShadow:
                          "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
                      }}
                      formatter={(value) => [`${(value * 1000).toFixed(2)}ms`, 'Latency']}
                    />
                    <Legend />
                    <Bar
                      dataKey="latency"
                      name="Latency (seconds)"
                      fill="#EA580C"
                      radius={[4, 4, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-full text-neutral-text-secondary">
                  No latency data available. Interact with the application to generate latency metrics.
                </div>
              )}
            </div>
          </div>
        </div>
        
        {/* Request Count by Endpoint (from latency data) */}
        <div className="card">
          <div className="card-header">
            <h3 className="h3 text-neutral-text">Request Count by Endpoint</h3>
          </div>
          <div className="card-body">
            <div className="h-80">
              {latencyData.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={latencyData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                    <XAxis dataKey="name" stroke="#64748B" />
                    <YAxis stroke="#64748B" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#FFFFFF",
                        borderColor: "#E2E8F0",
                        borderRadius: "0.5rem",
                        boxShadow:
                          "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
                      }}
                    />
                    <Legend />
                    <Bar
                      dataKey="count"
                      name="Request Count"
                      fill="#16A34A"
                      radius={[4, 4, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-full text-neutral-text-secondary">
                  No request count data available. Interact with the application to generate metrics.
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Raw Data Table */}
      <div className="card">
        <div className="card-header">
          <h3 className="h3 text-neutral-text">Detailed HTTP Metrics</h3>
        </div>
        <div className="card-body">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-neutral-border">
              <thead>
                <tr>
                  <th className="px-6 py-3 text-left body-small font-medium text-neutral-text-secondary uppercase tracking-wider">
                    Endpoint
                  </th>
                  <th className="px-6 py-3 text-left body-small font-medium text-neutral-text-secondary uppercase tracking-wider">
                    Method
                  </th>
                  <th className="px-6 py-3 text-left body-small font-medium text-neutral-text-secondary uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left body-small font-medium text-neutral-text-secondary uppercase tracking-wider">
                    Count
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-neutral-border">
                {metrics.length > 0 ? (
                  metrics.map((metric, index) => (
                    <tr key={index} className="hover:bg-neutral-background">
                      <td className="px-6 py-4 body-large text-neutral-text">
                        {metric.endpoint}
                      </td>
                      <td className="px-6 py-4 body-large text-neutral-text">
                        <span
                          className={`badge ${
                            metric.method === "GET"
                              ? "badge-info"
                              : metric.method === "POST"
                              ? "badge-success"
                              : metric.method === "PUT"
                              ? "badge-warning"
                              : "badge-error"
                          }`}
                        >
                          {metric.method}
                        </span>
                      </td>
                      <td className="px-6 py-4 body-large text-neutral-text">
                        <span
                          className={`badge ${
                            metric.status?.startsWith("2")
                              ? "badge-success"
                              : metric.status?.startsWith("4")
                              ? "badge-warning"
                              : metric.status?.startsWith("5")
                              ? "badge-error"
                              : "badge-info"
                          }`}
                        >
                          {metric.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 body-large text-neutral-text font-medium">
                        {metric.count}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td
                      colSpan="4"
                      className="px-6 py-4 text-center body-large text-neutral-text-secondary"
                    >
                      No metrics data available. Try interacting with the application to generate metrics.
                      {loading ? " Loading..." : ""}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      {/* Latency Data Table */}
      {latencyData.length > 0 && (
        <div className="card mt-8">
          <div className="card-header">
            <h3 className="h3 text-neutral-text">Latency Metrics</h3>
          </div>
          <div className="card-body">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-neutral-border">
                <thead>
                  <tr>
                    <th className="px-6 py-3 text-left body-small font-medium text-neutral-text-secondary uppercase tracking-wider">
                      Endpoint
                    </th>
                    <th className="px-6 py-3 text-left body-small font-medium text-neutral-text-secondary uppercase tracking-wider">
                      Method
                    </th>
                    <th className="px-6 py-3 text-left body-small font-medium text-neutral-text-secondary uppercase tracking-wider">
                      Request Count
                    </th>
                    <th className="px-6 py-3 text-left body-small font-medium text-neutral-text-secondary uppercase tracking-wider">
                      Average Latency
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-neutral-border">
                  {latencyData.map((metric, index) => (
                    <tr key={index} className="hover:bg-neutral-background">
                      <td className="px-6 py-4 body-large text-neutral-text">
                        {metric.name.split(' (')[0]}
                      </td>
                      <td className="px-6 py-4 body-large text-neutral-text">
                        {metric.name.split(' (')[1]?.split(')')[0] || 'N/A'}
                      </td>
                      <td className="px-6 py-4 body-large text-neutral-text">
                        {metric.count}
                      </td>
                      <td className="px-6 py-4 body-large text-neutral-text font-medium">
                        {(metric.latency * 1000).toFixed(2)}ms
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
      
      {/* Other Metrics Table */}
      {otherMetrics.length > 0 && (
        <div className="card mt-8">
          <div className="card-header">
            <h3 className="h3 text-neutral-text">Other System Metrics</h3>
          </div>
          <div className="card-body">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-neutral-border">
                <thead>
                  <tr>
                    <th className="px-6 py-3 text-left body-small font-medium text-neutral-text-secondary uppercase tracking-wider">
                      Metric Name
                    </th>
                    <th className="px-6 py-3 text-left body-small font-medium text-neutral-text-secondary uppercase tracking-wider">
                      Labels
                    </th>
                    <th className="px-6 py-3 text-left body-small font-medium text-neutral-text-secondary uppercase tracking-wider">
                      Value
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-neutral-border">
                  {otherMetrics.map((metric, index) => (
                    <tr key={index} className="hover:bg-neutral-background">
                      <td className="px-6 py-4 body-large text-neutral-text">
                        {metric.name}
                      </td>
                      <td className="px-6 py-4 body-large text-neutral-text">
                        {metric.labels || 'N/A'}
                      </td>
                      <td className="px-6 py-4 body-large text-neutral-text font-medium">
                        {metric.value}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Metrics;
