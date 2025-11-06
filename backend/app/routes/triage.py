from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.tasks import process_triage_request
from celery.result import AsyncResult
from prometheus_client import Counter
import os
import uuid
import asyncio
from typing import TYPE_CHECKING
from app.utils.iot_simulator import get_iot_vitals_data, stream_iot_vitals_data

if TYPE_CHECKING:
    from celery import Task

router = APIRouter()

# --- Prometheus Metrics for Triage ---
TRIAGE_REQUESTS = Counter("triage_requests_total", "Total Triage Requests", ["status"])

# --- Pydantic Models ---
class PatientData(BaseModel):
    symptoms: str
    vitals: Dict[str, Any]
    age: int
    gender: str
    image_path: Optional[str] = None

class IoTDataRequest(BaseModel):
    condition: Optional[str] = None
    duration_seconds: Optional[int] = 60

class ClinicianReview(BaseModel):
    task_id: str
    approved: bool
    notes: Optional[str] = None
    override_recommendations: Optional[bool] = False
    modified_urgency: Optional[str] = None

# In-memory storage for clinician reviews (in production, this would be a database)
clinician_reviews = {}

# --- Triage Endpoint ---
@router.post("/triage")
async def run_triage(patient_data: PatientData):
    """
    Accepts patient data and initiates the triage process.
    """
    try:
        # Using delay method for better type checking
        task = process_triage_request.delay(patient_data.dict())
        TRIAGE_REQUESTS.labels(status="started").inc()
        return {"task_id": task.id, "status": "Triage process started"}
    except Exception as e:
        TRIAGE_REQUESTS.labels(status="failed").inc()
        raise HTTPException(status_code=500, detail=str(e))

# --- IoT Data Endpoint ---
@router.post("/iot-vitals")
async def get_iot_vitals_data_endpoint(request: IoTDataRequest):
    """
    Simulates IoT vital signs data for patient monitoring.
    """
    try:
        # For the frontend pull button, we want instant response
        # Only stream if explicitly requested with duration > 0
        if request.duration_seconds and request.duration_seconds > 0:
            # Stream data over time - run in thread pool for better performance
            vitals_data = await asyncio.get_event_loop().run_in_executor(
                None, stream_iot_vitals_data, request.duration_seconds
            )
            return {"status": "success", "data": vitals_data, "message": f"Streamed {len(vitals_data)} vital signs readings"}
        else:
            # Single data point - run in thread pool for better performance
            if request.condition:
                vitals_data = await asyncio.get_event_loop().run_in_executor(
                    None, get_iot_vitals_data, request.condition
                )
            else:
                vitals_data = await asyncio.get_event_loop().run_in_executor(
                    None, get_iot_vitals_data
                )
            return {"status": "success", "data": vitals_data, "message": "Vital signs data generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Clinician Review Endpoints ---
@router.post("/clinician-review")
async def save_clinician_review(review: ClinicianReview):
    """
    Save clinician review and approval of AI recommendations.
    """
    try:
        # Validate required fields
        if not review.task_id:
            raise HTTPException(status_code=400, detail="Task ID is required")
        
        # Add timestamp to the review
        import datetime
        review_data = review.dict()
        review_data["timestamp"] = datetime.datetime.now().isoformat()
        
        # Store the review in memory (in production, this would go to a database)
        clinician_reviews[review.task_id] = review_data
        return {"status": "success", "message": "Review saved successfully", "data": review_data}
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save review: {str(e)}")

@router.get("/clinician-review/{task_id}")
async def get_clinician_review(task_id: str):
    """
    Retrieve clinician review for a specific task.
    """
    try:
        if not task_id:
            raise HTTPException(status_code=400, detail="Task ID is required")
            
        review = clinician_reviews.get(task_id)
        if review:
            return {"status": "success", "data": review}
        else:
            return {"status": "not_found", "message": "No review found for this task"}
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve review: {str(e)}")

# --- Image Upload Endpoint ---
UPLOAD_DIRECTORY = "./uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Uploads a medical image and returns the file path.
    """
    try:
        filename = file.filename or "unknown"
        file_extension = os.path.splitext(filename)[1]
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIRECTORY, file_name)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return {"file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

# --- Result Endpoint ---
@router.get("/results/{task_id}")
async def get_triage_result(task_id: str):
    """
    Retrieves the result of a triage task.
    """
    task_result = AsyncResult(task_id)

    if task_result.state == 'PENDING':
        return {"status": "Pending"}
    elif task_result.state == 'FAILURE':
        TRIAGE_REQUESTS.labels(status="failed").inc()
        return {"status": "Failed", "result": str(task_result.info)}
    else:
        TRIAGE_REQUESTS.labels(status="completed").inc()
        return {"status": "Success", "result": task_result.get()}