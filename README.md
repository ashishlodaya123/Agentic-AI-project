# Agentic Clinical Decision Assistant

This project is an AI-powered, agentic healthcare decision-support system that provides real-time triage recommendations using multimodal data. It leverages a multi-agent architecture with LangChain and LangGraph to process patient symptoms, vitals, medical imaging, and clinical knowledge to generate triage recommendations.

## 🎯 Features

- **Multi-Agent Architecture:** Five specialized agents working together to analyze patient data
- **Real-time Processing:** Asynchronous task processing with Celery and Redis
- **Clinical Knowledge Base:** ChromaDB-powered RAG (Retrieval-Augmented Generation) system with 10 detailed clinical guidelines
- **External Medical Data Integration:** Direct access to MEDLINE, CDC, and WHO data sources
- **Rule-Based Medical Logic:** Transparent clinical decision-making without black-box models
- **Agent Orchestration:** LangGraph-powered decision flow with state management
- **Monitoring & Metrics:** Prometheus endpoint for system monitoring
- **Modern UI/UX:** React-based dashboard with Tailwind CSS styling

## 🏗️ Architecture Overview

### Multi-Agent System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            FastAPI Server                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────┐  │
│  │   Triage API     │  │   Metrics API    │  │   Database Management    │  │
│  │   Endpoints      │  │   Endpoints      │  │   (ChromaDB Init)        │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────────┤
│                            Celery Task Queue                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Decision Support Agent (Orchestrator)             │   │
│  │                               │                                      │   │
│  │                    ┌──────────▼──────────┐                           │   │
│  │                    │ Symptom & Vitals    │                           │   │
│  │                    │ Analysis Agent      │                           │   │
│  │                    └──────────┬──────────┘                           │   │
│  │                               │                                      │   │
│  │                    ┌──────────▼──────────┐                           │   │
│  │                    │ Medical Imaging     │                           │   │
│  │                    │ Analysis Agent      │                           │   │
│  │                    └──────────┬──────────┘                           │   │
│  │                               │                                      │   │
│  │                    ┌──────────▼──────────┐                           │   │
│  │                    │ Knowledge-RAG       │                           │   │
│  │                    │ Retrieval Agent     │                           │   │
│  │                    └──────────┬──────────┘                           │   │
│  │                               │                                      │   │
│  │                    ┌──────────▼──────────┐                           │   │
│  │                    │ Risk Stratification │                           │   │
│  │                    │ Assessment Agent    │                           │   │
│  │                    └─────────────────────┘                           │   │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  Redis (Task Queue)    ChromaDB (Knowledge Base)   Sentence Transformers    │
│  MEDLINE API (Literature)  CDC/WHO Direct Endpoints (Public Health Data)    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Agent Coordination Workflow

1. **Symptom & Vitals Analysis Agent** - Parses and analyzes structured patient input using clinical rules
2. **Medical Imaging Analysis Agent** - Analyzes medical images using rule-based logic for quality assessment
3. **Knowledge-RAG Retrieval Agent** - Retrieves relevant clinical guidelines from ChromaDB using semantic search with external data integration
4. **Risk Stratification Assessment Agent** - Predicts patient risk using comprehensive clinical rules
5. **Decision Support Agent (Orchestrator)** - Coordinates all agents using LangGraph to compose final recommendations

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
│   │   ├── data/                # Clinical knowledge base
│   │   │   └── clinical_guidelines.json
│   │   ├── routes/              # API route definitions
│   │   │   ├── database.py
│   │   │   ├── metrics.py
│   │   │   └── triage.py
│   │   ├── utils/               # Utility functions
│   │   │   └── medical_apis.py
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
# MEDLINE API key for enhanced medical literature search
MEDLINE_API_KEY=your_medline_api_key
# CDC and WHO data sources require no API keys
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
- `GET /api/status` - Returns the current status of the database

### Monitoring Endpoints

- `GET /metrics` - Prometheus metrics endpoint for system monitoring
- `GET /` - API root endpoint to check backend status

## 🧠 Agent Details

### Symptom & Vitals Analysis Agent

Processes patient symptoms and vital signs using clinical rules to generate a structured summary of key concerns with:

- Detailed vital signs assessment (heart rate, temperature, blood pressure)
- Normal range comparisons with status indicators
- Critical symptom identification
- Demographic risk factor analysis

### Medical Imaging Analysis Agent

Analyzes medical images using rule-based logic to assess:

- Image quality and technical characteristics
- Resolution and format analysis
- Clinical imaging type identification (X-ray, CT, MRI, ultrasound)
- Quality recommendations for diagnostic use

### Knowledge-RAG Retrieval Agent

Retrieves relevant clinical guidelines from ChromaDB using sentence-transformers embeddings with:

- Semantic search for relevant medical protocols
- Relevance scoring and ranking
- Enhanced filtering for clinical applicability
- **External Data Integration**:
  - MEDLINE/PubMed literature search (with API key)
  - CDC public health guidelines (no API key required)
  - WHO international health standards (no API key required)
- Automatic fallback to local guidelines when external data is unavailable
- Automatic database initialization with 10 comprehensive guidelines

### Risk Stratification Assessment Agent

Predicts patient risk scores using comprehensive clinical rules for transparency and explainability:

- Age-based risk factors
- Vital sign abnormalities
- Symptom severity scoring
- Normalized risk score (0.0-1.0) with urgency levels

### Decision Support Agent (Orchestrator)

Orchestrates all agents using LangGraph to generate final triage recommendations:

- State management for multi-step processing
- Structured output formatting
- Comprehensive urgency level classification (Green, Yellow, Red)
- Clinical guideline integration with patient-specific data

## 📚 Clinical Knowledge Base

The system includes 10 comprehensive clinical guidelines covering:

- Acute respiratory distress management
- Acute coronary syndrome evaluation
- Infectious disease fever protocol
- Hypertensive crisis management
- Altered mental status assessment
- Acute abdominal pain evaluation
- Tachycardia management protocol
- Severe headache evaluation
- Anaphylaxis emergency treatment
- Diabetic emergency management

Each guideline includes:

- Detailed clinical protocols
- Evidence-based treatment recommendations
- Diagnostic criteria
- Management strategies

## 🔗 External Medical Data Integration

The system integrates with external medical data sources to enhance recommendations:

### MEDLINE/PubMed API

- **Access**: Requires free registration with API key
- **Benefits**: Access to recent medical literature and research
- **Usage**: Automatically integrated when API key is provided
- **Fallback**: Local guidelines used when API key is not provided

### CDC Direct Endpoints

- **Access**: Completely free, no API key required
- **Benefits**: Public health guidelines and recommendations
- **Usage**: Automatically integrated without configuration
- **Reliability**: High availability with no rate limits

### WHO Direct Endpoints

- **Access**: Free access to public health data
- **Benefits**: International health standards and guidelines
- **Usage**: Automatically integrated without configuration
- **Scope**: Global health recommendations and disease management

## 📊 Monitoring & Metrics

The system exposes Prometheus metrics at `/metrics` endpoint including:

- HTTP request counts and latency
- Active Celery tasks
- Successful triage completions
- Average model inference time
- Database query performance

## 🔧 Development Guidelines

### Backend Development

1. All agents are implemented in the `app/agents/` directory
2. API routes are defined in `app/routes/`
3. Celery tasks are defined in `app/tasks.py`
4. Configuration is managed through `app/core/config.py`
5. External API integrations are handled in `app/utils/medical_apis.py`

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
