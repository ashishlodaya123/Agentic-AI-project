# Agentic Clinical Decision Assistant

This project is an AI-powered, agentic healthcare decision-support system that provides real-time triage recommendations using multimodal data.

## Features

- **Backend:** FastAPI, Celery, Redis, LangChain, LangGraph, ChromaDB
- **Frontend:** React, Vite, Tailwind CSS, Recharts
- **Agents:**
  - Symptom & Vitals Agent
  - Medical Imaging Agent
  - Knowledge-RAG Agent
  - Risk Stratification Agent
  - Decision Support Agent
- **Metrics:** Prometheus endpoint for monitoring

## Project Structure

```
.
├── backend/
│   ├── app/
│   ├── .env
│   ├── requirements.txt
│   └── README.md
└── frontend/
    ├── src/
    ├── .env
    ├── package.json
    └── README.md
```

## Setup and Execution

### Prerequisites

- Python 3.8+
- Node.js 16+
- Redis

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Start Redis:**
    ```bash
    redis-server
    ```

5.  **Start the Celery worker:**
    ```bash
    celery -A app.core.celery_worker worker --loglevel=info --pool=solo
    ```

6.  **Run the FastAPI server:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

7.  **Initialize the ChromaDB database:**
    Open a new terminal and run the following command:
    ```bash
    curl -X GET http://127.0.0.1:8000/api/initdb
    ```

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd ../frontend
    ```

2.  **Install the required dependencies:**
    ```bash
    npm install
    ```

3.  **Run the development server:**
    ```bash
    npm run dev
    ```

The application will be available at `http://localhost:5173`.

## API Endpoints

- `POST /api/triage`: Submits patient data for triage.
- `POST /api/upload`: Uploads a medical image.
- `GET /api/results/{task_id}`: Retrieves the result of a triage task.
- `GET /api/initdb`: Initializes the ChromaDB with sample data.
- `GET /metrics`: Prometheus metrics endpoint.
- `GET /`: API root, check backend status.
