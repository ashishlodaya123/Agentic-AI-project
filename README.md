# Agentic Clinical Decision Assistant

This project is an AI-powered, agentic healthcare decision-support system that provides real-time triage recommendations using multimodal data. It leverages a multi-agent architecture with LangChain and LangGraph to process patient symptoms, vitals, medical imaging, and clinical knowledge to generate triage recommendations.

## 🎯 Features

- **Multi-Agent Architecture:** Five specialized agents working together to analyze patient data
- **Real-time Processing:** Asynchronous task processing with Celery and Redis
- **Clinical Knowledge Base:** ChromaDB-powered RAG (Retrieval-Augmented Generation) system
- **Rule-Based Medical Logic:** Transparent clinical decision-making without black-box models
- **Decision Visualization:** LangGraph-powered decision flow visualization
- **Monitoring & Metrics:** Prometheus endpoint for system monitoring
- **Modern UI/UX:** React-based dashboard with Tailwind CSS styling

## 🏗️ Architecture Overview

### Backend Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FastAPI Server                       │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────┐ │
│  │   Triage API     │  │   Metrics API    │  │ Database   │ │
│  │   Endpoints      │  │   Endpoints      │  │ Management │ │
│  └──────────────────┘  └──────────────────┘  └────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    Celery Task Queue                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────┐ │
│  │ Decision Support │  │ Symptom & Vitals │  │ Risk       │ │
│  │ Agent            │  │ Agent            │  │ Stratification││
│  │ (LangGraph)      │  │                  │  │ Agent      │ │
│  └──────────────────┘  └──────────────────┘  └────────────┘ │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ Knowledge-RAG    │  │ Medical Imaging  │                │
│  │ Agent            │  │ Agent            │                │
│  └──────────────────┘  └──────────────────┘                │
├─────────────────────────────────────────────────────────────┤
│  Redis (Task Queue)    ChromaDB (Knowledge)   PyTorch      │
└─────────────────────────────────────────────────────────────┘
```

### Agent System

1. **Symptom & Vitals Agent** - Parses and analyzes structured patient input using clinical rules
2. **Medical Imaging Agent** - Analyzes medical images using rule-based logic
3. **Knowledge-RAG Agent** - Retrieves relevant clinical guidelines from ChromaDB
4. **Risk Stratification Agent** - Predicts patient risk using clinical rules instead of ML models
5. **Decision Support Agent** - Orchestrates all agents using LangGraph to compose final recommendations

## 📁 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── agents/              # Individual agent implementations
│   │   │   ├── decision_agent.py
│   │   │   ├── imaging_agent.py
│   │   │   ├── rag_agent.py
│   │   │   ├── risk_agent.py
│   │   │   └── symptoms_vitals_agent.py
│   │   ├── core/                # Core application components
│   │   │   ├── celery_worker.py
│   │   │   ├── config.py
│   │   │   └── metrics.py
│   │   ├── routes/              # API route definitions
│   │   │   ├── database.py
│   │   │   ├── metrics.py
│   │   │   └── triage.py
│   │   ├── main.py              # FastAPI application entry point
│   │   └── tasks.py             # Celery task definitions
│   ├── .env                     # Environment configuration
│   ├── requirements.txt         # Python dependencies
│   └── README.md
└── frontend/
    ├── src/
    │   ├── api/                 # API client functions
    │   │   └── index.js
    │   ├── components/          # Reusable UI components
    │   ├── hooks/               # Custom React hooks
    │   ├── pages/               # Page components
    │   │   ├── Home.jsx
    │   │   ├── Metrics.jsx
    │   │   ├── Results.jsx
    │   │   └── TriageDashboard.jsx
    │   ├── App.jsx              # Main application component
    │   ├── index.css            # Global CSS styles
    │   └── main.jsx             # React application entry point
    ├── .env                     # Frontend environment configuration
    ├── package.json             # Node.js dependencies
    ├── tailwind.config.js       # Tailwind CSS configuration
    └── vite.config.js           # Vite build configuration
```

## 🚀 Setup and Execution

### Prerequisites

- Python 3.8+
- Node.js 16+
- Redis Server
- Git (for cloning the repository)

### Environment Configuration

Before running the application, you need to set up environment variables for both backend and frontend.

#### Backend Environment Variables

Create a `.env` file in the `backend/` directory with the following content:

```env
REDIS_URL=redis://localhost:6379/0
API_KEY=triage_secret_key
PROMETHEUS_PORT=9090
CHROMA_DB_PATH=./chroma_data
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
FASTAPI_PORT=8000
```

#### Frontend Environment Variables

Create a `.env` file in the `frontend/` directory with the following content:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_API_KEY=triage_secret_key
```

### Backend Setup

1. **Navigate to the backend directory:**

   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**

   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Start Redis Server:**

   ```bash
   # On Windows (if installed via Redis installer)
   redis-server

   # On macOS (if installed via Homebrew)
   brew services start redis

   # On Linux (Ubuntu/Debian)
   sudo systemctl start redis
   ```

5. **Start the Celery worker:**

   ```bash
   celery -A app.core.celery_worker worker --loglevel=info --pool=solo
   ```

6. **Run the FastAPI server (in a new terminal):**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

7. **Initialize the ChromaDB database:**
   Open a new terminal and run the following command:
   ```bash
   curl -X GET http://127.0.0.1:8000/api/initdb
   ```

### Frontend Setup

1. **Navigate to the frontend directory (in a new terminal):**

   ```bash
   cd frontend
   ```

2. **Install the required dependencies:**

   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:5173`.

## 🌐 API Endpoints

### Triage Endpoints

- `POST /api/triage` - Submits patient data for triage analysis

  ```json
  {
    "symptoms": "Patient complains of chest pain and shortness of breath.",
    "vitals": {
      "heart_rate": 110,
      "blood_pressure": "140/90",
      "temperature": 37.8
    },
    "age": 58,
    "gender": "Male",
    "image_path": "/path/to/image.jpg"
  }
  ```

- `POST /api/upload` - Uploads a medical image file
- `GET /api/results/{task_id}` - Retrieves the result of a triage task

### Database Endpoints

- `GET /api/initdb` - Initializes the ChromaDB with sample clinical guidelines

### Monitoring Endpoints

- `GET /metrics` - Prometheus metrics endpoint for system monitoring
- `GET /` - API root endpoint to check backend status

## 🧠 Agent Details

### Symptom & Vitals Agent

Processes patient symptoms and vital signs using clinical rules to generate a summary of key concerns.

### Medical Imaging Agent

Analyzes medical images using rule-based logic to assess image quality and provide contextual information.

### Knowledge-RAG Agent

Retrieves relevant clinical guidelines from ChromaDB using sentence-transformers embeddings with enhanced ranking.

### Risk Stratification Agent

Predicts patient risk scores using clinical rules instead of ML models for transparency and explainability.

### Decision Support Agent

Orchestrates all agents using LangGraph to generate final triage recommendations with urgency levels (Green, Yellow, Red).

## 📊 Monitoring & Metrics

The system exposes Prometheus metrics at `/metrics` endpoint including:

- HTTP request counts and latency
- Active Celery tasks
- Successful triage completions
- Average model inference time

## 🔧 Development Guidelines

### Backend Development

1. All agents are implemented in the `app/agents/` directory
2. API routes are defined in `app/routes/`
3. Celery tasks are defined in `app/tasks.py`
4. Configuration is managed through `app/core/config.py`

### Frontend Development

1. Pages are implemented in `src/pages/`
2. API calls are managed in `src/api/`
3. UI components use Tailwind CSS for styling
4. Routing is handled by React Router

### Adding New Agents

1. Create a new agent file in `app/agents/`
2. Implement the agent class with a `run()` method
3. Add the agent to the DecisionSupportAgent workflow in `app/agents/decision_agent.py`
4. Update the TriageState type definition if needed

## 🛡️ Security Considerations

- API key authentication is implemented for all triage endpoints
- Sensitive data should not be stored in logs
- File uploads are restricted to image formats
- All dependencies should be regularly updated

## 📈 Performance Optimization

- Embedding model is loaded once at startup and cached
- Heavy operations are offloaded to Celery workers
- Redis is used for task queuing and result caching
- Prometheus metrics help identify performance bottlenecks

## 🧪 Testing

To run backend tests:

```bash
cd backend
python -m pytest tests/
```

To run frontend tests:

```bash
cd frontend
npm run test
```

## 📚 Dependencies

### Backend Dependencies

- **FastAPI** - High-performance web framework
- **Celery** - Distributed task queue
- **Redis** - Message broker for Celery
- **LangChain** - LLM integration framework
- **LangGraph** - Agent workflow orchestration
- **ChromaDB** - Vector database for RAG
- **Sentence Transformers** - Embedding models
- **Pillow** - Image processing
- **Prometheus Client** - Metrics collection
- **Pydantic** - Data validation

### Frontend Dependencies

- **React** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling framework
- **Axios** - HTTP client
- **Recharts** - Data visualization
- **Framer Motion** - Animation library
- **React Router** - Client-side routing

## 🆘 Troubleshooting

### Common Issues

1. **Redis Connection Error**: Ensure Redis server is running and accessible
2. **Embedding Model Loading**: Check internet connection for first-time downloads
3. **Celery Worker Not Starting**: Verify Redis connection and Python environment
4. **Frontend Not Connecting**: Check API base URL in frontend .env file

### Logs and Debugging

- Backend logs are displayed in the terminal where FastAPI is running
- Celery worker logs show task processing information
- Frontend logs can be viewed in the browser's developer console

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For support, please open an issue on the GitHub repository.
