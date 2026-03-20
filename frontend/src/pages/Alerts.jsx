import { useState, useEffect } from 'react';
import { alertsAPI } from '../services/api';
import './Alerts.css';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [filters, setFilters] = useState({
    alert_type: '',
    is_resolved: '',
  });

  useEffect(() => {
    fetchAlerts();
  }, [page, filters.alert_type, filters.is_resolved]);

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      const params = { page, page_size: 10 };
      if (filters.alert_type) params.alert_type = filters.alert_type;
      if (filters.is_resolved !== '') params.is_resolved = filters.is_resolved;
      
      const response = await alertsAPI.getAlerts(params);
      setAlerts(response.data.alerts);
    } catch (err) {
      setError('Failed to load alerts');
    } finally {
      setLoading(false);
    }
  };

  const handleResolve = async (id) => {
    try {
      await alertsAPI.resolveAlert(id);
      fetchAlerts();
    } catch (err) {
      alert('Failed to resolve alert');
    }
  };

  const handleFilterChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
    setPage(1);
  };

  const getSeverityClass = (severity) => {
    switch (severity) {
      case 'high': return 'severity-high';
      case 'medium': return 'severity-medium';
      case 'low': return 'severity-low';
      default: return '';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  const getAlertTypeLabel = (type) => {
    return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <div className="alerts-page">
      <h1>Alerts</h1>
      <p className="subtitle">Monitor and manage system alerts</p>

      <div className="filters">
        <select name="alert_type" value={filters.alert_type} onChange={handleFilterChange}>
          <option value="">All Types</option>
          <option value="motion_detected">Motion Detected</option>
          <option value="object_detected">Object Detected</option>
          <option value="anomaly">Anomaly</option>
          <option value="error">Error</option>
        </select>
        <select name="is_resolved" value={filters.is_resolved} onChange={handleFilterChange}>
          <option value="">All Status</option>
          <option value="0">Unresolved</option>
          <option value="1">Resolved</option>
        </select>
        <button onClick={fetchAlerts}>Apply Filters</button>
      </div>

      {loading ? (
        <div className="loading">Loading alerts...</div>
      ) : error ? (
        <div className="error">{error}</div>
      ) : (
        <div className="alerts-list">
          {alerts.length === 0 ? (
            <div className="no-data">No alerts found</div>
          ) : (
            alerts.map((alert) => (
              <div key={alert.id} className={`alert-card ${alert.is_resolved ? 'resolved' : ''}`}>
                <div className="alert-header">
                  <span className={`alert-type ${getSeverityClass(alert.severity)}`}>
                    {getAlertTypeLabel(alert.alert_type)}
                  </span>
                  <span className={`status ${alert.is_resolved ? 'resolved' : 'pending'}`}>
                    {alert.is_resolved ? 'Resolved' : 'Pending'}
                  </span>
                </div>
                <p className="alert-message">{alert.message}</p>
                <div className="alert-meta">
                  <span>Video ID: {alert.video_id}</span>
                  <span>Created: {formatDate(alert.created_at)}</span>
                  {alert.resolved_at && <span>Resolved: {formatDate(alert.resolved_at)}</span>}
                </div>
                {!alert.is_resolved && (
                  <button 
                    className="resolve-btn"
                    onClick={() => handleResolve(alert.id)}
                  >
                    Mark as Resolved
                  </button>
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default Alerts;
