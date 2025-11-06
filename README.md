# Agentic Clinical Decision Assistant

This project is an AI-powered, agentic healthcare decision-support system that provides real-time triage recommendations using multimodal data. It leverages a multi-agent architecture with LangChain and LangGraph to process patient symptoms, vitals, medical imaging, and clinical knowledge to generate triage recommendations.

## 🎯 Features

- **Multi-Agent Architecture:** Nine specialized agents working together to analyze patient data
- **Real-time Processing:** Asynchronous task processing with Celery and Redis
- **Clinical Knowledge Base:** ChromaDB-powered RAG (Retrieval-Augmented Generation) system with 10 detailed clinical guidelines
- **External Medical Data Integration:** Direct access to MEDLINE, CDC, and WHO data sources
- **Rule-Based Medical Logic:** Transparent clinical decision-making without black-box models
- **Agent Orchestration:** LangGraph-powered decision flow with state management
- **Advanced Diagnostic Support:** Differential diagnosis generation and predictive analytics for complications
- **Treatment Optimization:** Personalized treatment recommendations with cost-effectiveness analysis
- **Enhanced Clinical Visualizations:** Interactive charts and visual representations of clinical data with improved data accuracy
- **Comprehensive Metrics Dashboard:** Real-time system performance monitoring with latency tracking and Prometheus integration
- **IoT Data Integration:** Simulated IoT medical device data for continuous patient monitoring
- **Enterprise-Grade Medical Imaging Analysis:** Advanced image analysis with quality metrics and technical assessment
- **Human-in-the-Loop Review:** Clinician approval and modification of AI recommendations
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
5. **Treatment Recommendation Agent** - Generates evidence-based treatment recommendations
6. **Follow-up Planning Agent** - Creates comprehensive follow-up schedules
7. **Drug Interaction Agent** - Provides safety screening for prescribed medications
8. **Specialist Consultation Agent** - Recommends appropriate specialists
9. **Quality Assurance Agent** - Reviews all recommendations for consistency and completeness
10. **Differential Diagnosis Agent** - Generates ranked differential diagnoses with enhanced symptom matching
11. **Predictive Analytics Agent** - Forecasts potential complications with expanded risk factors
12. **Clinical Visualization Agent** - Generates visualization data for clinical information with improved data accuracy
13. **Decision Support Agent (Orchestrator)** - Coordinates all agents using LangGraph to compose final recommendations

## 📁 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── agents/              # Individual agent implementations
│   │   │   ├── decision_agent.py
│   │   │   ├── differential_diagnosis_agent.py
│   │   │   ├── drug_interaction_agent.py
│   │   │   ├── followup_agent.py
│   │   │   ├── imaging_agent.py
│   │   │   ├── predictive_analytics_agent.py
│   │   │   ├── quality_agent.py
│   │   │   ├── rag_agent.py
│   │   │   ├── risk_agent.py
│   │   │   ├── specialist_agent.py
│   │   │   ├── symptoms_vitals_agent.py
│   │   │   └── treatment_agent.py
│   │   ├── core/                # Core application components
│   │   │   ├── celery_worker.py
│   │   │   ├── config.py
│   │   │   └── metrics.py
│   │   ├── data/                # Clinical knowledge base
│   │   │   └── clinical_guidelines.json
│   │   ├── routes/              # API route definitions
│   │   │   ├── advanced_agents.py
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

## 🐳 Docker Setup (Alternative to Manual Setup)

For a more streamlined deployment, you can run the entire application using Docker Compose. This setup includes all necessary services (Redis, backend, worker, and frontend) in isolated containers.

### Prerequisites

- Docker Desktop 4.0+ (includes Docker Engine and Docker Compose)
- For Windows users: Ensure Docker Desktop is configured to use WSL 2 backend

### Running with Docker

1. **Build and start all services:**

   ```bash
   docker-compose up --build
   ```

   For Windows users, if you encounter issues, try:

   ```bash
   docker-compose up --build --force-recreate
   ```

2. **Access the application:**

   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Redis: localhost:6379

3. **Initialize the database:**
   After the services are running, initialize the ChromaDB with sample clinical guidelines:

   ```bash
   curl -X GET http://localhost:8000/api/initdb
   ```

4. **Stop the services:**

   ```bash
   docker-compose down
   ```

### Docker Environment Configuration

The Docker setup uses the same environment variables as the manual setup but with container-specific values. You can customize these in the `docker-compose.yml` file:

- **Backend Services**: Use `redis://redis:6379/0` as the Redis URL since Redis runs in a separate container
- **Frontend**: Connects to the backend service via `http://backend:8000` within the Docker network

To add your MEDLINE API key, uncomment and modify the environment variable in `docker-compose.yml`:

```yaml
# - MEDLINE_API_KEY=your_medline_api_key
```

### Development with Docker

For development purposes, the Docker setup includes volume mounts that allow you to modify code locally and see changes reflected in the containers:

- Backend code is mounted to `/app` in the backend and worker containers
- Frontend code is mounted to `/app` in the frontend container
- Data volumes persist Redis data, ChromaDB, and uploaded files between container restarts

### Useful Docker Commands

- **View logs:**

  ```bash
  docker-compose logs -f [service_name]
  ```

- **Execute commands in a running container:**

  ```bash
  docker-compose exec backend bash
  docker-compose exec frontend sh
  ```

- **Rebuild specific services:**
  ```bash
  docker-compose build [service_name]
  ```

The Docker setup maintains full compatibility with the manual setup, so you can switch between them as needed. All data persisted in volumes will be available regardless of which setup you use.

> **Note for Windows users**: If you experience performance issues with volume mounting, consider enabling the "Use gRPC FUSE for file sharing" option in Docker Desktop settings for better performance.

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

### IoT Data Endpoints

- `POST /api/iot-vitals` - Simulates IoT vital signs data for patient monitoring

  ```json
  {
    "condition": "chest_pain", // Optional: specific medical condition to simulate
    "duration_seconds": 60 // Optional: stream data over time (0 for single reading)
  }
  ```

### Clinician Review Endpoints

- `POST /api/clinician-review` - Save clinician review and approval of AI recommendations
- `GET /api/clinician-review/{task_id}` - Retrieve clinician review for a specific task

### Database Endpoints

- `GET /api/initdb` - Initializes the ChromaDB with sample clinical guidelines
- `GET /api/status` - Returns the current status of the database

### Monitoring Endpoints

- `GET /metrics` - Prometheus metrics endpoint for system monitoring with enhanced latency tracking
- `GET /` - API root endpoint to check backend status

### Advanced Agent Endpoints

- `POST /api/agents/treatment` - Generate treatment recommendations
- `POST /api/agents/followup` - Generate follow-up care plans
- `POST /api/agents/drug-interactions` - Check for drug interactions and contraindications
- `POST /api/agents/specialist` - Get specialist consultation recommendations
- `POST /api/agents/quality` - Run quality assurance on all recommendations
- `POST /api/agents/differential-diagnosis` - Generate differential diagnoses
- `POST /api/agents/predictive-analytics` - Forecast potential complications
- `POST /api/agents/clinical-visualization` - Generate clinical visualization data

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
- Enterprise-grade image analysis with quality metrics and confidence scoring

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

### Treatment Recommendation Agent

Generates evidence-based treatment recommendations with:

- Condition-specific treatment protocols
- Contraindication checking
- Personalized recommendations based on patient demographics
- Confidence scoring for treatment suggestions

### Follow-up Planning Agent

Creates comprehensive follow-up schedules with:

- Immediate, short-term, and long-term monitoring plans
- Condition-specific follow-up protocols
- Monitoring parameter recommendations
- Special considerations based on patient complexity

### Drug Interaction Agent

Provides safety screening for prescribed medications:

- Drug-drug interaction checking
- Contraindication assessment
- Risk level classification (high, moderate, low)
- Management recommendations for identified risks

### Specialist Consultation Agent

Recommends appropriate specialists based on:

- Patient conditions and complexity
- Urgency level assessment
- Consultation timing recommendations
- Specialty-specific consultation details

### Quality Assurance Agent

Reviews all recommendations for consistency and completeness:

- Completeness checking across all agent outputs
- Consistency verification between recommendations
- Safety assessment with risk identification
- Overall quality scoring and improvement suggestions

### Differential Diagnosis Agent

Generates ranked differential diagnoses based on symptoms and vitals with enhanced accuracy:

- Expanded database of common medical conditions with symptom profiles
- Improved matching algorithm based on symptom overlap and direct symptom consideration
- Demographic adjustments for age and gender
- Medical history consideration for risk factors
- Confidence scoring for each differential

### Predictive Analytics Agent

Forecasts potential complications based on patient data with expanded coverage:

- Enhanced complication risk modeling for cardiac, respiratory, infectious, neurological, renal, and metabolic conditions
- Improved risk factor analysis based on medical history and symptoms analysis
- Vital sign indicator monitoring
- Prevention strategy recommendations
- Monitoring protocol suggestions

### Clinical Visualization Agent

Generates visualization data for clinical information with improved data accuracy:

- Enhanced vital signs charts with normal range indicators and proper data extraction
- Improved risk stratification visualizations with accurate risk factor representation
- Treatment timeline representations
- Symptom distribution charts
- Patient summary dashboards with comprehensive information

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

- HTTP request counts and latency with per-endpoint tracking
- Active Celery tasks
- Successful triage completions
- Average model inference time
- Database query performance
- System health indicators

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
5. Add API endpoints in `app/routes/advanced_agents.py`
6. Update frontend components to display agent results
7. Add agent to the main recommendation output in `generate_recommendation()`

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
