from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional
from app.tasks import process_triage_request
from celery.result import AsyncResult
from prometheus_client import Counter
import os
import uuid

router = APIRouter()

# --- Prometheus Metrics for Triage ---
TRIAGE_REQUESTS = Counter("triage_requests_total", "Total Triage Requests", ["status"])

# --- Pydantic Models ---
class PatientData(BaseModel):
    symptoms: str = Field(..., example="Patient complains of chest pain and shortness of breath.")
    vitals: dict = Field(..., example={"heart_rate": 110, "blood_pressure": "140/90", "temperature": 37.8})
    age: int = Field(..., example=58)
    gender: str = Field(..., example="Male")
    image_path: Optional[str] = None

# --- Triage Endpoint ---
@router.post("/triage")
async def run_triage(patient_data: PatientData):
    """
    Accepts patient data and initiates the triage process.
    """
    try:
        task = process_triage_request.delay(patient_data.dict())
        TRIAGE_REQUESTS.labels(status="started").inc()
        return {"task_id": task.id, "status": "Triage process started"}
    except Exception as e:
        TRIAGE_REQUESTS.labels(status="failed").inc()
        raise HTTPException(status_code=500, detail=str(e))

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
        file_extension = os.path.splitext(file.filename)[1]
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
    task_result = AsyncResult(task_id, app=process_triage_request.app)

    if task_result.state == 'PENDING':
        return {"status": "Pending"}
    elif task_result.state == 'FAILURE':
        TRIAGE_REQUESTS.labels(status="failed").inc()
        return {"status": "Failed", "result": str(task_result.info)}
    else:
        TRIAGE_REQUESTS.labels(status="completed").inc()
        return {"status": "Success", "result": task_result.get()}