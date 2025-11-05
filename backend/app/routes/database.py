from fastapi import APIRouter, HTTPException
from app.agents.rag_agent import KnowledgeRAGAgent

router = APIRouter()

@router.get("/initdb")
async def init_database():
    """
    Initializes ChromaDB with comprehensive clinical guidelines.
    """
    rag_agent = KnowledgeRAGAgent()

    # Comprehensive clinical guidelines
    documents = [
        "For chest pain, consider acute coronary syndrome (ACS). Perform an ECG immediately. Administer aspirin unless contraindicated. Monitor vital signs closely.",
        "Shortness of breath could indicate heart failure, pulmonary embolism, or pneumonia. Assess oxygen saturation and respiratory rate. Consider chest X-ray and D-dimer test.",
        "High fever with a cough may suggest pneumonia or other respiratory infection. A chest X-ray is recommended. Start empiric antibiotic therapy based on local guidelines.",
        "Abdominal pain in the lower right quadrant could be appendicitis. A CT scan may be necessary. Monitor for signs of peritonitis.",
        "Severe headache with neck stiffness may indicate meningitis. Perform lumbar puncture if not contraindicated. Start broad-spectrum antibiotics immediately.",
        "Altered mental status requires immediate glucose check and neurological assessment. Consider CT head to rule out hemorrhage.",
        "Severe allergic reaction (anaphylaxis) requires immediate epinephrine administration. Monitor airway and provide oxygen support.",
        "Hypertensive crisis with end-organ damage requires immediate blood pressure reduction. Use IV antihypertensives and monitor closely.",
        "Severe dehydration in elderly patients requires IV fluid replacement. Monitor electrolytes and kidney function.",
        "Suspected stroke requires immediate neurology consultation. Perform CT head to rule out hemorrhage before thrombolytic therapy."
    ]
    metadatas = [
        {"source": "Cardiology Guidelines", "category": "cardiac", "urgency": "high"},
        {"source": "Pulmonology Guidelines", "category": "respiratory", "urgency": "high"},
        {"source": "Infectious Disease Guidelines", "category": "infectious", "urgency": "medium"},
        {"source": "Emergency Medicine Handbook", "category": "abdominal", "urgency": "medium"},
        {"source": "Neurology Guidelines", "category": "neurological", "urgency": "high"},
        {"source": "Emergency Medicine Handbook", "category": "neurological", "urgency": "high"},
        {"source": "Allergy Guidelines", "category": "allergic", "urgency": "high"},
        {"source": "Cardiology Guidelines", "category": "cardiac", "urgency": "high"},
        {"source": "Internal Medicine Guidelines", "category": "general", "urgency": "medium"},
        {"source": "Neurology Guidelines", "category": "neurological", "urgency": "high"}
    ]
    ids = [f"doc_{i+1}" for i in range(len(documents))]

    try:
        rag_agent.init_db(documents, metadatas, ids)
        return {"message": "ChromaDB initialized successfully with comprehensive clinical guidelines."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing ChromaDB: {str(e)}")