import { useState, useEffect } from 'react';
import { trainsAPI, camerasAPI } from '../services/api';
import './Trains.css';

const Trains = () => {
  const [trains, setTrains] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAddTrain, setShowAddTrain] = useState(false);
  const [showAddCamera, setShowAddCamera] = useState(false);
  const [selectedTrain, setSelectedTrain] = useState(null);
  const [cameras, setCameras] = useState([]);
  const [newTrain, setNewTrain] = useState({ train_number: '', name: '' });
  const [newCamera, setNewCamera] = useState({ train_id: '', camera_id: '', location: '' });

  useEffect(() => {
    fetchTrains();
  }, []);

  const fetchTrains = async () => {
    try {
      setLoading(true);
      const response = await trainsAPI.getTrains();
      setTrains(response.data);
    } catch (err) {
      setError('Failed to load trains');
    } finally {
      setLoading(false);
    }
  };

  const fetchCameras = async (trainId) => {
    try {
      const response = await trainsAPI.getTrainCameras(trainId);
      setCameras(response.data);
    } catch (err) {
      console.error('Failed to load cameras');
    }
  };

  const handleTrainClick = async (train) => {
    setSelectedTrain(train);
    await fetchCameras(train.id);
  };

  const handleAddTrain = async (e) => {
    e.preventDefault();
    try {
      await trainsAPI.createTrain(newTrain);
      setShowAddTrain(false);
      setNewTrain({ train_number: '', name: '' });
      fetchTrains();
    } catch (err) {
      alert('Failed to create train');
    }
  };

  const handleAddCamera = async (e) => {
    e.preventDefault();
    try {
      await camerasAPI.createCamera(newCamera);
      setShowAddCamera(false);
      setNewCamera({ train_id: '', camera_id: '', location: '' });
      if (selectedTrain) {
        fetchCameras(selectedTrain.id);
      }
    } catch (err) {
      alert('Failed to create camera');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="trains-page">
      <div className="trains-header">
        <div>
          <h1>Trains</h1>
          <p className="subtitle">Manage trains and cameras</p>
        </div>
        <div className="header-buttons">
          <button onClick={() => setShowAddTrain(true)}>+ Add Train</button>
          <button onClick={() => setShowAddCamera(true)}>+ Add Camera</button>
        </div>
      </div>

      {showAddTrain && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Add New Train</h2>
            <form onSubmit={handleAddTrain}>
              <input
                type="text"
                placeholder="Train Number"
                value={newTrain.train_number}
                onChange={(e) => setNewTrain({ ...newTrain, train_number: e.target.value })}
                required
              />
              <input
                type="text"
                placeholder="Train Name"
                value={newTrain.name}
                onChange={(e) => setNewTrain({ ...newTrain, name: e.target.value })}
                required
              />
              <div className="modal-buttons">
                <button type="button" onClick={() => setShowAddTrain(false)}>Cancel</button>
                <button type="submit">Add Train</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {showAddCamera && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Add New Camera</h2>
            <form onSubmit={handleAddCamera}>
              <select
                value={newCamera.train_id}
                onChange={(e) => setNewCamera({ ...newCamera, train_id: parseInt(e.target.value) })}
                required
              >
                <option value="">Select Train</option>
                {trains.map((train) => (
                  <option key={train.id} value={train.id}>
                    {train.train_number} - {train.name}
                  </option>
                ))}
              </select>
              <input
                type="text"
                placeholder="Camera ID"
                value={newCamera.camera_id}
                onChange={(e) => setNewCamera({ ...newCamera, camera_id: e.target.value })}
                required
              />
              <input
                type="text"
                placeholder="Location (e.g., Engine, Coach 1)"
                value={newCamera.location}
                onChange={(e) => setNewCamera({ ...newCamera, location: e.target.value })}
              />
              <div className="modal-buttons">
                <button type="button" onClick={() => setShowAddCamera(false)}>Cancel</button>
                <button type="submit">Add Camera</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {loading ? (
        <div className="loading">Loading trains...</div>
      ) : error ? (
        <div className="error">{error}</div>
      ) : (
        <div className="trains-content">
          <div className="trains-list">
            <h2>All Trains</h2>
            {trains.length === 0 ? (
              <div className="no-data">No trains found</div>
            ) : (
              trains.map((train) => (
                <div
                  key={train.id}
                  className={`train-card ${selectedTrain?.id === train.id ? 'selected' : ''}`}
                  onClick={() => handleTrainClick(train)}
                >
                  <h3>{train.train_number}</h3>
                  <p>{train.name}</p>
                  <span className="date">Created: {formatDate(train.created_at)}</span>
                </div>
              ))
            )}
          </div>

          <div className="cameras-panel">
            <h2>Cameras {selectedTrain ? `for ${selectedTrain.train_number}` : ''}</h2>
            {selectedTrain ? (
              cameras.length === 0 ? (
                <div className="no-data">No cameras found for this train</div>
              ) : (
                <div className="cameras-list">
                  {cameras.map((camera) => (
                    <div key={camera.id} className="camera-card">
                      <div className="camera-icon">📷</div>
                      <div className="camera-info">
                        <h4>{camera.camera_id}</h4>
                        <p>{camera.location || 'No location set'}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )
            ) : (
              <div className="no-data">Select a train to view cameras</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Trains;
