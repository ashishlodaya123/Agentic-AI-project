from fastapi import APIRouter
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY, Counter
from starlette.responses import Response

# Create a counter for metrics requests
METRICS_REQUESTS = Counter("metrics_requests_total", "Total Metrics Requests")

router = APIRouter()

@router.get("/")
async def metrics():
    """
    Expose Prometheus metrics.
    """
    # Increment the metrics request counter
    METRICS_REQUESTS.inc()
    
    # Generate the latest metrics
    latest = generate_latest(REGISTRY)
    return Response(content=latest, media_type=CONTENT_TYPE_LATEST)