from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.agents.treatment_agent import TreatmentRecommendationAgent
from app.agents.followup_agent import FollowupPlanningAgent
from app.agents.drug_interaction_agent import DrugInteractionAgent
from app.agents.specialist_agent import SpecialistConsultationAgent
from app.agents.quality_agent import QualityAssuranceAgent
from app.agents.differential_diagnosis_agent import DifferentialDiagnosisAgent
from app.agents.predictive_analytics_agent import PredictiveAnalyticsAgent
from app.agents.clinical_visualization_agent import ClinicalVisualizationAgent

router = APIRouter()

# Pydantic models for request/response
class AgentRequest(BaseModel):
    patient_data: dict
    symptoms_analysis: Optional[dict] = None
    risk_assessment: Optional[dict] = None
    treatment_recommendations: Optional[dict] = None
    followup_plan: Optional[dict] = None
    drug_interactions: Optional[dict] = None
    specialist_recommendations: Optional[dict] = None

class AgentResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None

# Treatment Recommendation Endpoint
@router.post("/treatment", response_model=AgentResponse)
async def get_treatment_recommendations(request: AgentRequest):
    """
    Generate treatment recommendations based on patient data and analysis.
    """
    try:
        agent = TreatmentRecommendationAgent()
        result = agent.run(
            request.patient_data,
            request.symptoms_analysis or {},
            request.risk_assessment or {}
        )
        return AgentResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Follow-up Planning Endpoint
@router.post("/followup", response_model=AgentResponse)
async def get_followup_plan(request: AgentRequest):
    """
    Generate follow-up plan based on patient data and recommendations.
    """
    try:
        agent = FollowupPlanningAgent()
        result = agent.run(
            request.patient_data,
            request.symptoms_analysis or {},
            request.risk_assessment or {},
            request.treatment_recommendations or {}
        )
        return AgentResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Drug Interaction Endpoint
@router.post("/drug-interactions", response_model=AgentResponse)
async def check_drug_interactions(request: AgentRequest):
    """
    Check for potential drug interactions and contraindications.
    """
    try:
        agent = DrugInteractionAgent()
        # Run the agent in a thread pool to avoid blocking the event loop
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        def run_agent():
            return agent.run(
                request.patient_data,
                request.treatment_recommendations or {}
            )
        
        with ThreadPoolExecutor() as executor:
            result = await asyncio.get_event_loop().run_in_executor(executor, run_agent)
        
        return AgentResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Specialist Consultation Endpoint
@router.post("/specialist", response_model=AgentResponse)
async def get_specialist_recommendations(request: AgentRequest):
    """
    Recommend appropriate specialists based on patient conditions.
    """
    try:
        agent = SpecialistConsultationAgent()
        # Run the agent in a thread pool to avoid blocking the event loop
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        def run_agent():
            return agent.run(
                request.patient_data,
                request.symptoms_analysis or {},
                request.risk_assessment or {},
                request.treatment_recommendations or {}
            )
        
        with ThreadPoolExecutor() as executor:
            result = await asyncio.get_event_loop().run_in_executor(executor, run_agent)
        
        return AgentResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Quality Assurance Endpoint
@router.post("/quality", response_model=AgentResponse)
async def run_quality_assurance(request: AgentRequest):
    """
    Review recommendations for consistency and completeness.
    """
    try:
        agent = QualityAssuranceAgent()
        # Run the agent in a thread pool to avoid blocking the event loop
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        def run_agent():
            return agent.run(
                request.patient_data,
                request.symptoms_analysis or {},
                request.risk_assessment or {},
                request.treatment_recommendations or {},
                request.followup_plan or {},
                request.drug_interactions or {},
                request.specialist_recommendations or {}
            )
        
        with ThreadPoolExecutor() as executor:
            result = await asyncio.get_event_loop().run_in_executor(executor, run_agent)
        
        return AgentResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Differential Diagnosis Endpoint
@router.post("/differential-diagnosis", response_model=AgentResponse)
async def get_differential_diagnosis(request: AgentRequest):
    """
    Generate differential diagnosis based on patient data and analysis.
    """
    try:
        agent = DifferentialDiagnosisAgent()
        # Run the agent in a thread pool to avoid blocking the event loop
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        def run_agent():
            return agent.run(
                request.patient_data,
                request.symptoms_analysis or {},
                request.risk_assessment or {}
            )
        
        with ThreadPoolExecutor() as executor:
            result = await asyncio.get_event_loop().run_in_executor(executor, run_agent)
        
        return AgentResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Predictive Analytics Endpoint
@router.post("/predictive-analytics", response_model=AgentResponse)
async def get_predictive_analytics(request: AgentRequest):
    """
    Forecast potential complications based on patient data.
    """
    try:
        agent = PredictiveAnalyticsAgent()
        # Run the agent in a thread pool to avoid blocking the event loop
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        def run_agent():
            return agent.run(
                request.patient_data,
                request.symptoms_analysis or {},
                request.risk_assessment or {},
                request.treatment_recommendations or {}
            )
        
        with ThreadPoolExecutor() as executor:
            result = await asyncio.get_event_loop().run_in_executor(executor, run_agent)
        
        return AgentResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Clinical Visualization Endpoint
@router.post("/clinical-visualization", response_model=AgentResponse)
async def get_clinical_visualization(request: AgentRequest):
    """
    Generate visualization data for clinical information.
    """
    try:
        agent = ClinicalVisualizationAgent()
        # Run the agent in a thread pool to avoid blocking the event loop
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        def run_agent():
            return agent.run(
                request.patient_data,
                request.symptoms_analysis or {},
                request.risk_assessment or {},
                request.treatment_recommendations or {},
                request.followup_plan,
                request.drug_interactions,
                request.specialist_recommendations
            )
        
        with ThreadPoolExecutor() as executor:
            result = await asyncio.get_event_loop().run_in_executor(executor, run_agent)
        
        return AgentResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))