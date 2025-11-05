from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from prometheus_client import make_asgi_app, Counter, Histogram, Gauge
import time
from app.core.config import settings
from app.routes import triage, metrics, database, advanced_agents
from app.core.embedding import EmbeddingModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Prometheus Metrics ---
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("http_request_latency_seconds", "HTTP Request Latency", ["method", "endpoint"])
ACTIVE_CONNECTIONS = Gauge("active_connections", "Number of active connections")

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Agentic Clinical Decision Assistant",
    description="An AI-powered system for real-time emergency triage.",
    version="1.0.0"
)

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.on_event("startup")
async def startup_event():
    # Initialize the embedding model on startup
    EmbeddingModel.get_instance()
    # Increment initial metrics to ensure there's data to display
    REQUEST_COUNT.labels(method="GET", endpoint="/", http_status="200").inc()

# --- API Key Authentication ---
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == settings.API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )

# --- Middleware ---
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    ACTIVE_CONNECTIONS.inc()
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    ACTIVE_CONNECTIONS.dec()

    endpoint = request.url.path
    method = request.method
    status_code = response.status_code

    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(process_time)
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()

    return response

# --- Routers ---
app.include_router(triage.router, prefix="/api", tags=["Triage"])  # Removed authentication dependency
app.include_router(metrics.router, prefix="/api", tags=["Metrics"])
app.include_router(database.router, prefix="/api", tags=["Database"])
app.include_router(advanced_agents.router, prefix="/api/agents", tags=["Advanced Agents"])

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Agentic Clinical Decision Assistant API"}