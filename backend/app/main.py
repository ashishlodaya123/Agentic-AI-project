from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.requests import Request
from starlette.responses import Response
from prometheus_client import make_asgi_app, Counter, Histogram
import time
from app.core.config import settings
from app.routes import triage, metrics, database
from langchain.embeddings import SentenceTransformerEmbeddings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Prometheus Metrics ---
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("http_request_latency_seconds", "HTTP Request Latency", ["method", "endpoint"])

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Agentic Clinical Decision Assistant",
    description="An AI-powered system for real-time emergency triage.",
    version="1.0.0"
)

# --- Embedding Model Singleton ---
class EmbeddingModel:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            cls._instance = SentenceTransformerEmbeddings(model_name=settings.EMBEDDING_MODEL)
            logger.info("Embedding model loaded successfully.")
        return cls._instance

@app.on_event("startup")
async def startup_event():
    # Initialize the embedding model on startup
    EmbeddingModel.get_instance()

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
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    endpoint = request.url.path
    method = request.method
    status_code = response.status_code

    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(process_time)
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()

    return response

# --- Routers ---
app.include_router(triage.router, prefix="/api", tags=["Triage"], dependencies=[Depends(get_api_key)])
app.include_router(metrics.router, prefix="/api", tags=["Metrics"])
app.include_router(database.router, prefix="/api", tags=["Database"])

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Agentic Clinical Decision Assistant API"}
