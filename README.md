# CCTV Railway Monitoring System

A web-based IoT dashboard for monitoring CCTV cameras on railway trains. Built with FastAPI (backend) and React + Vite (frontend).

## Features

- 🔐 **Authentication** - User login/registration with JWT tokens
- 🚂 **Train Management** - Add and manage trains
- 📷 **Camera Management** - Assign cameras to trains
- 🎬 **Video Management** - View recorded CCTV videos
- ⚠️ **Alerts System** - Motion detection and anomaly alerts
- 📊 **Dashboard** - Overview of system statistics

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database
- **JWT** - Token-based authentication
- **Bcrypt** - Password hashing

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **Axios** - HTTP client
- **React Router** - Navigation

## Project Structure

```
CCTV/
├── backend/
│   ├── core/           # Core utilities (auth, config, database)
│   ├── models/         # Database models
│   ├── repositories/   # Data access layer
│   ├── routes/         # API endpoints
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   ├── main.py         # Application entry point
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/ # Reusable components
│   │   ├── context/    # React context providers
│   │   ├── pages/      # Page components
│   │   ├── services/   # API services
│   │   └── App.jsx     # Main app component
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cctv-railway-monitoring.git
   cd cctv-railway-monitoring
   ```

2. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. **Start Backend**
   ```bash
   cd backend
   python main.py
   ```
   Backend runs at: http://localhost:8000

2. **Start Frontend** (in a new terminal)
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend runs at: http://localhost:5173

### Default Login

```
Username: admin
Password: admin123
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Register
- `GET /api/auth/me` - Get current user

### Trains
- `GET /api/trains` - List all trains
- `POST /api/trains` - Create train
- `GET /api/trains/{id}/cameras` - Get cameras for train

### Cameras
- `POST /api/cameras` - Create camera

### Videos
- `GET /api/videos` - List videos (with filters)
- `POST /api/videos` - Create video

### Alerts
- `GET /api/alerts` - List alerts
- `POST /api/alerts/{id}/resolve` - Resolve alert

## Database Schema

| Table | Description |
|-------|-------------|
| users | User accounts |
| trains | Train information |
| cameras | CCTV cameras |
| videos | Recorded videos |
| ai_detections | AI analysis results |
| alerts | System alerts |

## Screenshots

The application includes:
- Login/Register pages
- Dashboard with statistics
- Train management with camera assignment
- Video listing with filters
- Alerts management

## License

MIT License
