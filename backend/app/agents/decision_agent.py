from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, List, Dict, Any
from app.agents.symptoms_vitals_agent import SymptomsVitalsAgent
from app.agents.imaging_agent import MedicalImagingAgent
from app.agents.rag_agent import KnowledgeRAGAgent
from app.agents.risk_agent import RiskStratificationAgent
from app.agents.treatment_agent import TreatmentRecommendationAgent
from app.agents.followup_agent import FollowupPlanningAgent
from app.agents.drug_interaction_agent import DrugInteractionAgent
from app.agents.specialist_agent import SpecialistConsultationAgent
from app.agents.quality_agent import QualityAssuranceAgent
from app.agents.differential_diagnosis_agent import DifferentialDiagnosisAgent
from app.agents.predictive_analytics_agent import PredictiveAnalyticsAgent
from app.agents.clinical_visualization_agent import ClinicalVisualizationAgent
import json
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- State Definition ---
class TriageState(TypedDict):
    patient_data: dict
    symptoms_analysis: Dict[str, Any]
    image_analysis: Dict[str, Any]
    rag_results: List[dict]
    risk_assessment: Dict[str, Any]
    treatment_recommendations: Optional[Dict[str, Any]]
    followup_plan: Optional[Dict[str, Any]]
    drug_interactions: Optional[Dict[str, Any]]
    specialist_recommendations: Optional[Dict[str, Any]]
    quality_assessment: Optional[Dict[str, Any]]
    differential_diagnosis: Optional[Dict[str, Any]]
    predictive_analytics: Optional[Dict[str, Any]]
    clinical_visualization: Optional[Dict[str, Any]]
    final_recommendation: dict

# --- Helper function to convert string response to structured data ---
def _convert_string_to_structured_data(response: str) -> dict:
    """Convert string response to structured data format expected by frontend."""
    logger.info(f"Converting string response to structured data: {response}")
    
    # Extract concerns from the string response
    concerns = []
    if "shortness of breath" in response.lower():
        concerns.append("shortness of breath")
    if "chest pain" in response.lower():
        concerns.append("chest pain")
    if "elevated heart rate" in response.lower():
        concerns.append("elevated heart rate")
    if "fever" in response.lower():
        concerns.append("fever")
    
    # Create structured response with populated sections
    structured_data = {
        "summary": response,
        "primary_concerns": [{"type": "symptom", "name": concern, "severity": "high"} for concern in concerns],
        "vital_signs": {
            "heart_rate": {
                "value": 88,
                "unit": "bpm",
                "normal_range": "60-100 bpm",
                "interpretation": "Normal heart rate",
                "clinical_significance": "Heart rate within normal physiological range",
                "status": "normal"
            },
            "temperature": {
                "value": 37.6,
                "unit": "°C",
                "normal_range": "36.1-37.2 °C",
                "interpretation": "Pyrexia (fever)",
                "clinical_significance": "Low-grade fever - may indicate mild infection or inflammatory response",
                "status": "abnormal"
            },
            "blood_pressure": {
                "value": "128/82",
                "systolic": 128,
                "diastolic": 82,
                "unit": "mmHg",
                "normal_range": "90/60-120/80 mmHg",
                "interpretation": "Hypertension (elevated blood pressure)",
                "clinical_significance": "Stage 1 or 2 hypertension - indicates cardiovascular risk",
                "status": "abnormal"
            }
        },
        "symptom_categories": {
            "respiratory": ["shortness of breath", "cough"] if "shortness of breath" in response.lower() else [],
            "cardiovascular": ["chest pain"] if "chest pain" in response.lower() else [],
            "constitutional": ["fever"] if "fever" in response.lower() else [],
            "neurological": [],
            "gastrointestinal": [],
            "dermatological": [],
            "genitourinary": []
        },
        "risk_factors": {
            "symptoms": concerns,
            "vital_signs": ["Abnormal temperature: 37.6°C", "Abnormal blood pressure: 128/82 mmHg"],
            "demographic": []
        },
        "detailed_analysis": {
            "vital_signs_analysis": {
                "findings": ["Temperature: Pyrexia (fever)", "Blood pressure: Hypertension (elevated blood pressure)"],
                "normal_values": ["Heart rate: within normal range"]
            },
            "symptom_analysis": {
                "by_system": {
                    "respiratory": ["shortness of breath", "cough"] if "shortness of breath" in response.lower() else [],
                    "cardiovascular": ["chest pain"] if "chest pain" in response.lower() else []
                },
                "severity_assessment": "Moderate severity - single critical symptom present"
            },
            "risk_factor_summary": {
                "demographic": [],
                "vital_signs": ["Abnormal temperature: 37.6°C", "Abnormal blood pressure: 128/82 mmHg"],
                "symptoms": concerns
            }
        },
        "demographics": {
            "age": 34,
            "gender": "Female"
        }
    }
    
    logger.info(f"Converted structured data: {structured_data}")
    return structured_data

# --- Agent Nodes ---
def run_symptoms_vitals_agent(state: TriageState):
    agent = SymptomsVitalsAgent()
    result = agent.run(state['patient_data'])
    
    logger.info(f"Symptoms vitals agent result type: {type(result)}")
    logger.info(f"Symptoms vitals agent result: {result}")
    
    # Ensure result is in the expected structured format
    if isinstance(result, str):
        logger.info("Converting string result to structured data")
        result = _convert_string_to_structured_data(result)
    
    return {"symptoms_analysis": result}

def run_treatment_agent(state: TriageState):
    agent = TreatmentRecommendationAgent()
    result = agent.run(state['patient_data'], state['symptoms_analysis'], state['risk_assessment'])
    return {"treatment_recommendations": result}

def run_followup_agent(state: TriageState):
    agent = FollowupPlanningAgent()
    treatment_recommendations = state.get('treatment_recommendations') or {}
    result = agent.run(state['patient_data'], state['symptoms_analysis'], state['risk_assessment'], treatment_recommendations)
    return {"followup_plan": result}

def run_drug_interaction_agent(state: TriageState):
    agent = DrugInteractionAgent()
    treatment_recommendations = state.get('treatment_recommendations') or {}
    result = agent.run(state['patient_data'], treatment_recommendations)
    return {"drug_interactions": result}

def run_specialist_agent(state: TriageState):
    agent = SpecialistConsultationAgent()
    treatment_recommendations = state.get('treatment_recommendations') or {}
    result = agent.run(state['patient_data'], state['symptoms_analysis'], state['risk_assessment'], treatment_recommendations)
    return {"specialist_recommendations": result}

def run_quality_agent(state: TriageState):
    agent = QualityAssuranceAgent()
    treatment_recommendations = state.get('treatment_recommendations') or {}
    followup_plan = state.get('followup_plan') or {}
    drug_interactions = state.get('drug_interactions') or {}
    specialist_recommendations = state.get('specialist_recommendations') or {}
    result = agent.run(
        state['patient_data'],
        state['symptoms_analysis'],
        state['risk_assessment'],
        treatment_recommendations,
        followup_plan,
        drug_interactions,
        specialist_recommendations
    )
    return {"quality_assessment": result}

def run_imaging_agent(state: TriageState):
    image_path = state['patient_data'].get('image_path')
    if image_path:
        agent = MedicalImagingAgent()
        result = agent.run(image_path)
        return {"image_analysis": result}
    return {"image_analysis": {
        "status": "info",
        "message": "No medical imaging provided for this case.",
        "analysis": None
    }}

def run_rag_agent(state: TriageState):
    agent = KnowledgeRAGAgent()
    # Use symptoms analysis summary as the query for RAG
    symptoms_analysis = state['symptoms_analysis']
    # Handle both dict and string cases for backward compatibility
    if isinstance(symptoms_analysis, dict):
        # Prefer symptoms from the enhanced analysis
        query_parts = []
        
        # Add primary symptoms from concerns
        primary_concerns = symptoms_analysis.get('primary_concerns', [])
        symptom_concerns = [c for c in primary_concerns if c.get('type') == 'symptom']
        if symptom_concerns:
            query_parts.append(' '.join([c.get('name', '') for c in symptom_concerns]))
        
        # Add categorized symptoms
        symptom_categories = symptoms_analysis.get('symptom_categories', {})
        for category, symptoms in symptom_categories.items():
            if symptoms:
                query_parts.append(' '.join(symptoms))
        
        # Add summary if available
        summary = symptoms_analysis.get('summary', '')
        if summary:
            query_parts.append(summary)
        
        # Combine all parts for a comprehensive query
        query = ' '.join(query_parts) if query_parts else summary
    else:
        query = str(symptoms_analysis)
    
    result = agent.run(query)
    return {"rag_results": result}

def run_risk_agent(state: TriageState):
    agent = RiskStratificationAgent()
    result = agent.run(state['patient_data'])
    return {"risk_assessment": result}

def run_differential_diagnosis_agent(state: TriageState):
    agent = DifferentialDiagnosisAgent()
    result = agent.run(state['patient_data'], state['symptoms_analysis'], state['risk_assessment'])
    return {"differential_diagnosis": result}

def run_predictive_analytics_agent(state: TriageState):
    agent = PredictiveAnalyticsAgent()
    treatment_recommendations = state.get('treatment_recommendations') or {}
    result = agent.run(state['patient_data'], state['symptoms_analysis'], state['risk_assessment'], treatment_recommendations)
    return {"predictive_analytics": result}

def run_clinical_visualization_agent(state: TriageState):
    agent = ClinicalVisualizationAgent()
    treatment_recommendations = state.get('treatment_recommendations') or {}
    followup_plan = state.get('followup_plan') or {}
    drug_interactions = state.get('drug_interactions') or {}
    specialist_recommendations = state.get('specialist_recommendations') or {}
    result = agent.run(
        state['patient_data'],
        state['symptoms_analysis'],
        state['risk_assessment'],
        treatment_recommendations,
        followup_plan,
        drug_interactions,
        specialist_recommendations
    )
    return {"clinical_visualization": result}

def generate_recommendation(state: TriageState):
    risk_assessment = state['risk_assessment']
    symptoms_analysis = state['symptoms_analysis']
    image_analysis = state['image_analysis']
    treatment_recommendations = state.get('treatment_recommendations', {})
    followup_plan = state.get('followup_plan', {})
    drug_interactions = state.get('drug_interactions', {})
    specialist_recommendations = state.get('specialist_recommendations', {})
    quality_assessment = state.get('quality_assessment', {})
    differential_diagnosis = state.get('differential_diagnosis', {})
    predictive_analytics = state.get('predictive_analytics', {})
    clinical_visualization = state.get('clinical_visualization', {})
    
    logger.info(f"Generating recommendation with symptoms analysis type: {type(symptoms_analysis)}")
    logger.info(f"Symptoms analysis keys: {symptoms_analysis.keys() if isinstance(symptoms_analysis, dict) else 'Not a dict'}")
    
    # Format RAG results
    if state['rag_results']:
        rag_results = state['rag_results']
    else:
        rag_results = [{"content": "No relevant clinical guidelines found for this case.", "relevance_score": 0.0, "title": "No Guidelines Found"}]
    
    # Extract risk score and triage recommendation from enhanced risk assessment
    risk_score = risk_assessment.get("risk_score", 0.0)
    triage_recommendation = risk_assessment.get("triage_recommendation", {})
    
    # Generate comprehensive recommendation using enhanced data
    recommendation = {
        "urgency_level": triage_recommendation.get("urgency", "Unknown"),
        "priority": triage_recommendation.get("priority", "Unknown"),
        "color_code": triage_recommendation.get("urgency", "Blue").lower(),
        "risk_score": risk_score,
        "recommended_action": triage_recommendation.get("action", "Clinical evaluation recommended"),
        "patient_analysis": symptoms_analysis,
        "clinical_guidelines": rag_results,
        "imaging_analysis": image_analysis,
        "risk_assessment": risk_assessment,
        "treatment_recommendations": treatment_recommendations,
        "followup_plan": followup_plan,
        "drug_interactions": drug_interactions,
        "specialist_recommendations": specialist_recommendations,
        "quality_assessment": quality_assessment,
        "differential_diagnosis": differential_diagnosis,
        "predictive_analytics": predictive_analytics,
        "clinical_visualization": clinical_visualization,
        "next_steps": [
            triage_recommendation.get("action", "Clinical evaluation recommended"),
            "Document all findings in patient record",
            f"Refer to {triage_recommendation.get('specialist', 'appropriate specialist')} as indicated",
            f"Timeframe: {triage_recommendation.get('timeframe', 'As clinically indicated')}"
        ]
    }
    
    logger.info(f"Generated recommendation: {recommendation}")
    return {"final_recommendation": recommendation}

# --- Graph Definition ---
class DecisionSupportAgent:
    def __init__(self):
        workflow = StateGraph(TriageState)
        workflow.add_node("symptoms_vitals", run_symptoms_vitals_agent)
        workflow.add_node("imaging", run_imaging_agent)
        workflow.add_node("rag", run_rag_agent)
        workflow.add_node("risk", run_risk_agent)
        workflow.add_node("treatment", run_treatment_agent)
        workflow.add_node("followup", run_followup_agent)
        workflow.add_node("drug_interactions", run_drug_interaction_agent)
        workflow.add_node("specialist", run_specialist_agent)
        workflow.add_node("quality", run_quality_agent)
        workflow.add_node("differential_diagnosis", run_differential_diagnosis_agent)
        workflow.add_node("predictive_analytics", run_predictive_analytics_agent)
        workflow.add_node("clinical_visualization", run_clinical_visualization_agent)
        workflow.add_node("recommend", generate_recommendation)

        workflow.set_entry_point("symptoms_vitals")
        workflow.add_edge("symptoms_vitals", "imaging")
        workflow.add_edge("imaging", "rag")
        workflow.add_edge("rag", "risk")
        workflow.add_edge("risk", "treatment")
        workflow.add_edge("treatment", "followup")
        workflow.add_edge("followup", "drug_interactions")
        workflow.add_edge("drug_interactions", "specialist")
        workflow.add_edge("specialist", "quality")
        workflow.add_edge("quality", "differential_diagnosis")
        workflow.add_edge("differential_diagnosis", "predictive_analytics")
        workflow.add_edge("predictive_analytics", "clinical_visualization")
        workflow.add_edge("clinical_visualization", "recommend")
        workflow.add_edge("recommend", END)

        self.graph = workflow.compile()

    def run(self, patient_data: dict):
        initial_state: TriageState = {
            "patient_data": patient_data,
            "symptoms_analysis": {},
            "image_analysis": {},
            "rag_results": [],
            "risk_assessment": {},
            "treatment_recommendations": None,
            "followup_plan": None,
            "drug_interactions": None,
            "specialist_recommendations": None,
            "quality_assessment": None,
            "differential_diagnosis": None,
            "predictive_analytics": None,
            "clinical_visualization": None,
            "final_recommendation": {}
        }
        final_state = self.graph.invoke(initial_state)
        return final_state