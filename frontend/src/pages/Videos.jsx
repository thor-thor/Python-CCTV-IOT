import { useState, useEffect } from 'react';
import { videosAPI } from '../services/api';
import './Videos.css';

const Videos = () => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [filters, setFilters] = useState({
    train_number: '',
    status: '',
  });

  useEffect(() => {
    fetchVideos();
  }, [page, filters.status]);

  const fetchVideos = async () => {
    try {
      setLoading(true);
      const params = { page, page_size: 10 };
      if (filters.train_number) params.train_number = filters.train_number;
      if (filters.status) params.status = filters.status;
      
      const response = await videosAPI.getVideos(params);
      setVideos(response.data.videos);
      setTotalPages(response.data.total_pages);
    } catch (err) {
      setError('Failed to load videos');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
    setPage(1);
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'available': return 'status-available';
      case 'processing': return 'status-processing';
      case 'failed': return 'status-failed';
      default: return '';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  const formatDuration = (seconds) => {
    if (!seconds) return 'N/A';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="videos-page">
      <h1>Videos</h1>
      <p className="subtitle">Manage and view recorded videos</p>

      <div className="filters">
        <input
          type="text"
          name="train_number"
          placeholder="Filter by train number"
          value={filters.train_number}
          onChange={handleFilterChange}
        />
        <select name="status" value={filters.status} onChange={handleFilterChange}>
          <option value="">All Status</option>
          <option value="available">Available</option>
          <option value="processing">Processing</option>
          <option value="failed">Failed</option>
        </select>
        <button onClick={fetchVideos}>Apply Filters</button>
      </div>

      {loading ? (
        <div className="loading">Loading videos...</div>
      ) : error ? (
        <div className="error">{error}</div>
      ) : (
        <>
          <div className="videos-table">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Train ID</th>
                  <th>Camera ID</th>
                  <th>Timestamp</th>
                  <th>Duration</th>
                  <th>Status</th>
                  <th>Size</th>
                </tr>
              </thead>
              <tbody>
                {videos.length === 0 ? (
                  <tr>
                    <td colSpan="7" className="no-data">No videos found</td>
                  </tr>
                ) : (
                  videos.map((video) => (
                    <tr key={video.id}>
                      <td>{video.id}</td>
                      <td>{video.train_id}</td>
                      <td>{video.camera_id}</td>
                      <td>{formatDate(video.stored_timestamp)}</td>
                      <td>{formatDuration(video.duration)}</td>
                      <td>
                        <span className={`status-badge ${getStatusClass(video.status)}`}>
                          {video.status}
                        </span>
                      </td>
                      <td>{video.file_size ? `${(video.file_size / 1024 / 1024).toFixed(2)} MB` : 'N/A'}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          <div className="pagination">
            <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>
              Previous
            </button>
            <span>Page {page} of {totalPages}</span>
            <button onClick={() => setPage(p => Math.min(totalPages, p + 1))} disabled={page === totalPages}>
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Videos;
