from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, List
from app.agents.symptoms_vitals_agent import SymptomsVitalsAgent
from app.agents.imaging_agent import MedicalImagingAgent
from app.agents.rag_agent import KnowledgeRAGAgent
from app.agents.risk_agent import RiskStratificationAgent

# --- State Definition ---
class TriageState(TypedDict):
    patient_data: dict
    symptoms_analysis: str
    image_analysis: Optional[str]
    rag_results: List[dict]  # Changed to dict to include metadata
    risk_score: float
    final_recommendation: str

# --- Agent Nodes ---
def run_symptoms_vitals_agent(state: TriageState):
    agent = SymptomsVitalsAgent()
    result = agent.run(state['patient_data'])
    return {"symptoms_analysis": result}

def run_imaging_agent(state: TriageState):
    if "image_path" in state['patient_data'] and state['patient_data']['image_path']:
        agent = MedicalImagingAgent()
        result = agent.run(state['patient_data']['image_path'])
        return {"image_analysis": result}
    return {"image_analysis": "No image provided."}

def run_rag_agent(state: TriageState):
    agent = KnowledgeRAGAgent()
    # Use symptoms analysis as the query for RAG
    result = agent.run(state['symptoms_analysis'])
    return {"rag_results": result}

def run_risk_agent(state: TriageState):
    agent = RiskStratificationAgent()
    result = agent.run(state['patient_data'])
    return {"risk_score": result}

def generate_recommendation(state: TriageState):
    risk_score = state['risk_score']
    symptoms_analysis = state['symptoms_analysis']
    
    # Format RAG results
    if state['rag_results']:
        rag_results = "\n- ".join([str(result) for result in state['rag_results']])
    else:
        rag_results = "No relevant clinical guidelines found."
    
    # Determine urgency level
    urgency = "Low"
    color_code = "Green"
    recommendation_text = "Routine care recommended"
    
    if risk_score > 0.7:
        urgency = "High"
        color_code = "Red"
        recommendation_text = "Immediate medical attention required"
    elif risk_score > 0.4:
        urgency = "Medium"
        color_code = "Yellow"
        recommendation_text = "Prompt medical evaluation recommended"
    
    # Generate comprehensive recommendation
    recommendation = f"""
**Triage Recommendation**
=========================

**Urgency Level:** {urgency} ({color_code})
**Risk Score:** {risk_score:.2f}
**Recommended Action:** {recommendation_text}

**Patient Analysis:**
{symptoms_analysis}

**Clinical Guidelines:**
- {rag_results}

**Imaging Analysis:**
{state['image_analysis']}

**Next Steps:**
1. {"Contact emergency services immediately" if risk_score > 0.7 else "Schedule appointment with healthcare provider" if risk_score > 0.4 else "Monitor symptoms and follow up if needed"}
2. Document all findings in patient record
3. {"Consider specialist consultation" if risk_score > 0.5 else "Routine follow-up as needed"}
"""
    
    return {"final_recommendation": recommendation.strip()}

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
        initial_state = {"patient_data": patient_data}
        final_state = self.graph.invoke(initial_state)
        return final_state