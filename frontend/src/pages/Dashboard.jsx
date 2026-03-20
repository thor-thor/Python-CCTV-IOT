import { useState, useEffect } from 'react';
import { dashboardAPI } from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchSummary();
  }, []);

  const fetchSummary = async () => {
    try {
      const response = await dashboardAPI.getSummary();
      setSummary(response.data);
    } catch (err) {
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <p className="subtitle">Overview of CCTV Railway Monitoring System</p>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon video-icon">🎬</div>
          <div className="stat-content">
            <h3>{summary?.total_videos_today || 0}</h3>
            <p>Videos Today</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon train-icon">🚂</div>
          <div className="stat-content">
            <h3>{summary?.total_trains_monitored || 0}</h3>
            <p>Trains Monitored</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon alert-icon">⚠️</div>
          <div className="stat-content">
            <h3>{summary?.alerts_generated || 0}</h3>
            <p>Alerts Generated</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon storage-icon">💾</div>
          <div className="stat-content">
            <h3>{summary?.storage_usage_gb?.toFixed(2) || 0} GB</h3>
            <p>Storage Used</p>
          </div>
        </div>
      </div>

      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="action-buttons">
          <a href="/videos" className="action-btn">📹 View Videos</a>
          <a href="/alerts" className="action-btn">🔔 Manage Alerts</a>
          <a href="/trains" className="action-btn">🚂 Manage Trains</a>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
