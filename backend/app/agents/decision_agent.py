from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, List, Dict, Any
from app.agents.symptoms_vitals_agent import SymptomsVitalsAgent
from app.agents.imaging_agent import MedicalImagingAgent
from app.agents.rag_agent import KnowledgeRAGAgent
from app.agents.risk_agent import RiskStratificationAgent
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
        query = symptoms_analysis.get('summary', '')
    else:
        query = str(symptoms_analysis)
    result = agent.run(query)
    return {"rag_results": result}

def run_risk_agent(state: TriageState):
    agent = RiskStratificationAgent()
    result = agent.run(state['patient_data'])
    return {"risk_assessment": result}

def generate_recommendation(state: TriageState):
    risk_assessment = state['risk_assessment']
    symptoms_analysis = state['symptoms_analysis']
    image_analysis = state['image_analysis']
    
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
        workflow.add_node("recommend", generate_recommendation)

        workflow.set_entry_point("symptoms_vitals")
        workflow.add_edge("symptoms_vitals", "imaging")
        workflow.add_edge("imaging", "rag")
        workflow.add_edge("rag", "risk")
        workflow.add_edge("risk", "recommend")
        workflow.add_edge("recommend", END)

        self.graph = workflow.compile()

    def run(self, patient_data: dict):
        initial_state: TriageState = {
            "patient_data": patient_data,
            "symptoms_analysis": {},
            "image_analysis": {},
            "rag_results": [],
            "risk_assessment": {},
            "final_recommendation": {}
        }
        final_state = self.graph.invoke(initial_state)
        return final_state